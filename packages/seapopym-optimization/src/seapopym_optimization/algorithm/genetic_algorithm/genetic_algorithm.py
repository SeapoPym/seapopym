"""This module contains the main genetic algorithm functions that can be used to optimize the model."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Literal

import numpy as np
from deap import algorithms, base, tools

from seapopym_optimization.algorithm.genetic_algorithm.logbook import Logbook, LogbookCategory, LogbookIndex

if TYPE_CHECKING:
    from collections.abc import Sequence
    from numbers import Number

    from pandas._typing import FilePath, WriteBuffer

    from seapopym_optimization.algorithm.genetic_algorithm.evaluation_strategies import AbstractEvaluationStrategy
    from seapopym_optimization.constraint.protocol import ConstraintProtocol
    from seapopym_optimization.cost_function.protocol import CostFunctionProtocol
    from seapopym_optimization.functional_group.no_transport_functional_groups import Parameter


logger = logging.getLogger(__name__)


def individual_creator(cost_function_weight: tuple[Number]) -> type:
    """Create a custom individual class for DEAP genetic algorithms.

    This individual class inherits from `list` and includes a fitness attribute. It is redefined to work with the
    Dask framework, which does not support the default DEAP individual structure created with `deap.creator.create`.
    """

    class Fitness(base.Fitness):
        """Fitness class to store the fitness of an individual."""

        weights = cost_function_weight

    class Individual(list):
        """Individual class to store the parameters of an individual."""

        def __init__(self: Individual, iterator: Sequence, values: Sequence[Number] = ()) -> None:
            super().__init__(iterator)
            self.fitness = Fitness(values=values)

    return Individual


@dataclass
class GeneticAlgorithmParameters:
    """The structure used to store the genetic algorithm parameters.

    Can generate the toolbox with default parameters.
    parameters.

    Parameters
    ----------
    MUTPB: float
        Represents the probability of mutating an individual. It is recommended to use a value between 0.001 and 0.1.
    ETA: float
        Crowding degree of the mutation. A high eta will produce a mutant resembling its parent, while a small eta will
        produce a solution much more different. It is recommended to use a value between 1 and 20.
    INDPB: float
        Represents the individual probability of mutation for each attribute of the individual. It is recommended to use
        a value between 0.0 and 0.1. If you have a lot of parameters, you can use a 1/len(parameters) value.
    CXPB: float
        Represents the probability of mating two individuals. It is recommended to use a value between 0.5 and 1.0.
    NGEN: int
        Represents the number of generations.
    POP_SIZE: int
        Represents the size of the population.
    cost_function_weight: tuple | float = (-1.0,)
        The weight of the cost function. The default value is (-1.0,) to minimize the cost function.

    """

    ETA: float
    INDPB: float
    CXPB: float
    MUTPB: float
    NGEN: int
    POP_SIZE: int
    TOURNSIZE: int = field(default=3)
    cost_function_weight: tuple[Number] = (-1.0,)

    def __post_init__(self: GeneticAlgorithmParameters) -> None:
        """Check parameters and set default functions for selection, mating, mutation and variation."""
        self.select = tools.selTournament
        self.mate = tools.cxTwoPoint  # NOTE(Jules): We should test this method `tools.cxSimulatedBinary``
        self.mutate = tools.mutPolynomialBounded
        self.variation = algorithms.varAnd
        self.cost_function_weight = tuple(
            np.asarray(self.cost_function_weight) / np.sum(np.absolute(self.cost_function_weight))
        )

    def generate_toolbox(self: GeneticAlgorithmParameters, parameters: Sequence[Parameter]) -> base.Toolbox:
        """Generate a DEAP toolbox with the necessary functions for the genetic algorithm."""
        toolbox = base.Toolbox()
        Individual = individual_creator(self.cost_function_weight)  # noqa: N806
        toolbox.register("Individual", Individual)

        for param in parameters:
            toolbox.register(param.name, param.init_method, param.lower_bound, param.upper_bound)

        def individual() -> list:
            return Individual([param.init_method(param.lower_bound, param.upper_bound) for param in parameters])

        toolbox.register("population", tools.initRepeat, list, individual)
        # Note: Evaluation is now handled by evaluation strategies, not the toolbox
        toolbox.register("mate", self.mate)
        low_boundaries = [param.lower_bound for param in parameters]
        up_boundaries = [param.upper_bound for param in parameters]
        toolbox.register("mutate", self.mutate, eta=self.ETA, indpb=self.INDPB, low=low_boundaries, up=up_boundaries)
        toolbox.register("select", self.select, tournsize=self.TOURNSIZE)
        return toolbox


@dataclass
class GeneticAlgorithm:
    """Genetic algorithm for optimizing SeapoPym models.

    By default, the process order is SCM: Select, Cross, Mutate.

    Uses the Strategy pattern for individual evaluation, allowing
    easy switching between sequential and hybrid modes as needed.

    Examples
    --------
    >>> from seapopym_optimization.algorithm.genetic_algorithm import GeneticAlgorithmFactory
    >>> ga = GeneticAlgorithmFactory.create_sequential(meta_params, cost_function)
    >>> results = ga.optimize()

    Attributes
    ----------
    meta_parameter: GeneticAlgorithmParameters
        The parameters of the genetic algorithm.
    cost_function: CostFunctionProtocol
        The cost function to optimize.
    evaluation_strategy: AbstractEvaluationStrategy
        Strategy pattern for evaluating individuals.
    constraint: Sequence[ConstraintProtocol] | None
        The constraints to apply to the individuals. If None, no constraints are applied.
    save: PathLike | None
        The path to save the logbook (in Parquet format). If None, the logbook is not saved.

    """

    meta_parameter: GeneticAlgorithmParameters
    cost_function: CostFunctionProtocol
    evaluation_strategy: AbstractEvaluationStrategy
    constraint: Sequence[ConstraintProtocol] | None = None

    save: FilePath | WriteBuffer[bytes] | None = None
    logbook: Logbook | None = field(default=None, repr=False)
    toolbox: base.Toolbox | None = field(default=None, init=False, repr=False)

    def __post_init__(self: GeneticAlgorithm) -> None:
        """Check parameters and initialize the evaluation strategy."""
        # Logbook configuration
        if self.logbook is not None and not isinstance(self.logbook, Logbook):
            self.logbook = Logbook(self.logbook)
        if self.save is not None:
            self.save = Path(self.save)
            if self.save.exists():
                warning_msg = f"Logbook file {self.save} already exists. It will be overwritten."
                logger.warning(warning_msg)

        # Toolbox generation
        ordered_parameters = self.cost_function.functional_groups.unique_functional_groups_parameters_ordered()
        self.toolbox = self.meta_parameter.generate_toolbox(ordered_parameters.values())

        # Application des contraintes
        if self.constraint is not None:
            for constraint in self.constraint:
                self.toolbox.decorate("evaluate", constraint.generate(list(ordered_parameters.keys())))

        # Validation des poids
        if len(self.meta_parameter.cost_function_weight) != len(self.cost_function.observations):
            msg = (
                "The cost function weight must have the same length as the number of observations. "
                f"Got {len(self.meta_parameter.cost_function_weight)} and {len(self.cost_function.observations)}."
            )
            raise ValueError(msg)

    def update_logbook(self: GeneticAlgorithm, logbook: Logbook) -> None:
        """Update the logbook with the new data and save to disk if a path is provided."""
        if not isinstance(logbook, Logbook):
            logbook = Logbook(logbook)

        if self.logbook is None:
            self.logbook = logbook
        else:
            # Append new generation using Pandas concat
            self.logbook = self.logbook.append_new_generation(logbook)

        if self.save is not None:
            self.logbook.to_parquet(self.save)

    def _evaluate(self: GeneticAlgorithm, individuals: Sequence, generation: int) -> Logbook:
        """Evaluate individuals by delegating to the evaluation strategy.

        Creates and returns a Logbook for the current generation.
        """

        def update_fitness(individuals: list) -> list:
            known = [ind.fitness.valid for ind in individuals]
            invalid_ind = [ind for ind in individuals if not ind.fitness.valid]

            if invalid_ind:
                # Delegation to the evaluation strategy
                fitnesses = self.evaluation_strategy.evaluate(invalid_ind)

                for ind, fit in zip(invalid_ind, fitnesses, strict=True):
                    ind.fitness.values = fit

            return known

        known = update_fitness(individuals)

        # Extract parameter names and fitness names
        parameter_names = list(
            self.cost_function.functional_groups.unique_functional_groups_parameters_ordered().keys()
        )
        fitness_names = list(self.cost_function.observations.keys())

        # Create Logbook from individuals (fitness is automatically extracted)
        return Logbook.from_individual(
            generation=generation,
            is_from_previous_generation=known,
            individual=individuals,
            parameter_names=parameter_names,
            fitness_names=fitness_names,
        )

    def _initialization(self: GeneticAlgorithm) -> tuple[int, list[list]]:
        """Initialize the genetic algorithm. If a logbook is provided, it will load the last generation."""

        def create_first_generation() -> tuple[Literal[1], list[list]]:
            """Create the first generation (i.e. generation `0`) of individuals."""
            new_generation = 0
            population = self.toolbox.population(n=self.meta_parameter.POP_SIZE)
            logbook = self._evaluate(individuals=population, generation=new_generation)
            self.update_logbook(logbook)
            next_generation = new_generation + 1
            return next_generation, population

        def create_population_from_logbook(population_unprocessed: pd.DataFrame) -> list[list]:
            """Create a population from the logbook DataFrame."""
            individuals = population_unprocessed.loc[:, [LogbookCategory.PARAMETER]].to_numpy()
            fitness = list(population_unprocessed.loc[:, [LogbookCategory.FITNESS]].itertuples(index=False, name=None))
            fitness = [() if any(np.isnan(fit)) else fit for fit in fitness]
            return [
                self.toolbox.Individual(iterator=iterator, values=values)
                for iterator, values in zip(individuals, fitness, strict=True)
            ]

        if self.logbook is None:
            return create_first_generation()

        logger.info("Logbook found. Loading last generation.")

        last_computed_generation = self.logbook.index.get_level_values(LogbookIndex.GENERATION).max()
        population_unprocessed = self.logbook.loc[last_computed_generation]

        population = create_population_from_logbook(population_unprocessed)

        if population_unprocessed.loc[:, LogbookCategory.FITNESS].isna().any(axis=None):
            logger.warning("Some individuals in the logbook have no fitness values. Re-evaluating the population.")
            logbook = self._evaluate(population, last_computed_generation)
            self.logbook = None
            self.update_logbook(logbook)

        return last_computed_generation + 1, population

    def optimize(self: GeneticAlgorithm) -> Logbook:
        """This is the main function. Use it to optimize your model."""
        generation_start, population = self._initialization()

        for gen in range(generation_start, self.meta_parameter.NGEN):
            log_message = f"Generation {gen} / {self.meta_parameter.NGEN}."
            logger.info(log_message)
            offspring = self.toolbox.select(population, self.meta_parameter.POP_SIZE)
            offspring = self.meta_parameter.variation(
                offspring, self.toolbox, self.meta_parameter.CXPB, self.meta_parameter.MUTPB
            )
            logbook = self._evaluate(offspring, gen)

            self.update_logbook(logbook)
            population[:] = offspring

        return self.logbook.copy()
