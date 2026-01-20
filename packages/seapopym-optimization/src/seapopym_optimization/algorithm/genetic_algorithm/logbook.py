"""Pandas-based Logbook with Pandera validation."""

from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
import pandera.pandas as pa
from pandera.typing import DataFrame

from seapopym_optimization.functional_group.parameter_initialization import initialize_with_sobol_sampling

if TYPE_CHECKING:
    from collections.abc import Sequence

    from seapopym_optimization.functional_group.base_functional_group import FunctionalGroupSet


class LogbookCategory(StrEnum):
    """Enumeration of the logbook categories for the genetic algorithm."""

    PARAMETER = "Parametre"
    FITNESS = "Fitness"
    WEIGHTED_FITNESS = "Weighted_fitness"


class LogbookIndex(StrEnum):
    """Enumeration of the logbook index for the genetic algorithm."""

    GENERATION = "Generation"
    PREVIOUS_GENERATION = "Is_From_Previous_Generation"
    INDIVIDUAL = "Individual"

    def get_index(self: LogbookIndex) -> str:
        """Get the index for the logbook category."""
        return list(LogbookIndex).index(self)


parameter_column_schema = pa.Column(regex=True, nullable=False)
fitness_column_schema = pa.Column(regex=True, nullable=True)
weighted_fitness_column_schema = pa.Column(regex=True, nullable=True)


multiple_index_schema = pa.MultiIndex(
    [
        pa.Index(
            pa.Int,
            name=LogbookIndex.GENERATION,
            nullable=False,
            checks=pa.Check(lambda x: x >= 0, error="Generation index must be non-negative."),
        ),
        pa.Index(
            pa.Bool,
            name=LogbookIndex.PREVIOUS_GENERATION,
            nullable=False,
        ),
        pa.Index(
            pa.Int,
            name=LogbookIndex.INDIVIDUAL,
            nullable=False,
            checks=pa.Check(lambda x: x >= 0, error="Individual index must be non-negative."),
        ),
    ],
    coerce=True,
)


logbook_schema = pa.DataFrameSchema(
    columns={
        (LogbookCategory.PARAMETER, ".*"): parameter_column_schema,
        (LogbookCategory.FITNESS, ".*"): fitness_column_schema,
        (LogbookCategory.WEIGHTED_FITNESS, LogbookCategory.WEIGHTED_FITNESS): weighted_fitness_column_schema,
    },
    index=multiple_index_schema,
    strict=True,
)


class Logbook(DataFrame[logbook_schema]):
    """
    Pandas-based logbook for tracking genetic algorithm optimization.

    Uses Pandera for strict validation.

    Structure:
    - Index: MultiIndex (Generation, Is_From_Previous_Generation, Individual)
    - Columns: MultiIndex (Category, Name)
        - Parametre: parameter values
        - Fitness: raw fitness values (nullable)
        - Weighted_fitness: weighted sum of fitness (nullable)

    Serialization:
    Use standard Pandas methods:
        logbook.to_parquet("file.parquet")
        df = pd.read_parquet("file.parquet")
        logbook = Logbook(df)
    """

    @classmethod
    def from_individual(
        cls: type[Logbook],
        generation: int,
        is_from_previous_generation: list[bool],
        individual: list[list],
        parameter_names: list[str],
        fitness_names: list[str],
    ) -> Logbook:
        """
        Create a Logbook from a list of DEAP individuals.

        Parameters
        ----------
        generation : int
            Generation number
        is_from_previous_generation : list[bool]
            Whether each individual comes from previous generation
        individual : list[list]
            List of DEAP individuals with fitness attributes
        parameter_names : list[str]
            Names of parameters
        fitness_names : list[str]
            Names of fitness objectives

        Returns
        -------
        Logbook
            Validated logbook instance

        """
        index = pd.MultiIndex.from_arrays(
            [[generation] * len(individual), is_from_previous_generation, range(len(individual))],
            names=[LogbookIndex.GENERATION, LogbookIndex.PREVIOUS_GENERATION, LogbookIndex.INDIVIDUAL],
        )
        columns = pd.MultiIndex.from_tuples(
            [(LogbookCategory.PARAMETER.value, name) for name in parameter_names]
            + [(LogbookCategory.FITNESS.value, name) for name in fitness_names]
            + [(LogbookCategory.WEIGHTED_FITNESS.value, LogbookCategory.WEIGHTED_FITNESS.value)],
            names=["category", "name"],
        )

        data = np.asarray([indiv + list(indiv.fitness.values) + [sum(indiv.fitness.wvalues)] for indiv in individual])

        return cls(data=data, index=index, columns=columns)

    @classmethod
    def from_array(
        cls: type[Logbook],
        generation: Sequence[int],
        is_from_previous_generation: Sequence[bool],
        individual: Sequence[Sequence[float]],
        parameter_names: Sequence[str],
        fitness_names: Sequence[str],
        fitness_values: Sequence[Sequence[float]] | None = None,
        weighted_fitness: Sequence[float] | None = None,
    ) -> Logbook:
        """
        Create a Logbook from arrays.

        Parameters
        ----------
        generation : Sequence[int]
            Generation numbers for each individual
        is_from_previous_generation : Sequence[bool]
            Whether each individual comes from previous generation
        individual : Sequence[Sequence[float]]
            Parameter values for each individual
        parameter_names : Sequence[str]
            Names of parameters
        fitness_names : Sequence[str]
            Names of fitness objectives
        fitness_values : Sequence[Sequence[float]], optional
            Fitness values (NaN if not provided)
        weighted_fitness : Sequence[float], optional
            Weighted fitness values (NaN if not provided)

        Returns
        -------
        Logbook
            Validated logbook instance

        """
        index = pd.MultiIndex.from_arrays(
            [generation, is_from_previous_generation, range(len(individual))],
            names=[LogbookIndex.GENERATION, LogbookIndex.PREVIOUS_GENERATION, LogbookIndex.INDIVIDUAL],
        )
        columns = pd.MultiIndex.from_tuples(
            [(LogbookCategory.PARAMETER, name) for name in parameter_names]
            + [(LogbookCategory.FITNESS, name) for name in fitness_names]
            + [(LogbookCategory.WEIGHTED_FITNESS, LogbookCategory.WEIGHTED_FITNESS)],
            names=["category", "name"],
        )
        fitness_values = fitness_values or np.full((len(individual), len(fitness_names)), np.nan)

        weighted_fitness = weighted_fitness or np.full((len(individual), 1), np.nan)
        data = np.concatenate(
            [
                np.asarray(individual),
                np.asarray(fitness_values).reshape(len(individual), len(fitness_names)),
                np.asarray(weighted_fitness).reshape(len(individual), 1),
            ],
            axis=1,
        )
        return cls(data=data, index=index, columns=columns)

    @classmethod
    def from_sobol_samples(
        cls: type[Logbook],
        functional_group_parameters: Sequence | FunctionalGroupSet,
        sample_number: int,
        fitness_names: list[str],
    ) -> Logbook:
        """
        Create a Logbook from Sobol samples.

        Parameters
        ----------
        functional_group_parameters : Sequence | FunctionalGroupSet
            Functional group parameters for sampling
        sample_number : int
            N parameter for SALib sample_sobol. Total samples = N * (D + 2)
        fitness_names : list[str]
            Names of fitness objectives

        Returns
        -------
        Logbook
            Logbook with Sobol-sampled parameters and NaN fitness

        """
        samples = initialize_with_sobol_sampling(functional_group_parameters, sample_number)

        return cls.from_array(
            generation=[0] * len(samples),
            is_from_previous_generation=[False] * len(samples),
            individual=samples.to_numpy(),
            parameter_names=samples.columns.tolist(),
            fitness_names=fitness_names,
        )

    def append_new_generation(self: Logbook, new_generation: Logbook) -> Logbook:
        """
        Append a new generation to the logbook.

        Parameters
        ----------
        new_generation : Logbook
            New generation to append

        Returns
        -------
        Logbook
            Combined logbook with validation

        """
        if not isinstance(new_generation, Logbook):
            msg = "new_generation must be a Logbook instance."
            raise TypeError(msg)

        return Logbook(pd.concat([self, new_generation]))

    @property
    def generations(self: Logbook) -> list[int]:
        """Get list of generation numbers."""
        return self.index.get_level_values(LogbookIndex.GENERATION).unique().sort_values().tolist()

    def copy(self: Logbook) -> Logbook:
        """Create a validated copy of the logbook."""
        return Logbook(pd.DataFrame.copy(self))
