"""Module for parameter initialization methods for functional groups."""

from __future__ import annotations

from random import uniform
from typing import TYPE_CHECKING

import pandas as pd
from SALib import ProblemSpec

from seapopym_optimization.functional_group.base_functional_group import AbstractFunctionalGroup, FunctionalGroupSet

if TYPE_CHECKING:
    from collections.abc import Sequence

MAXIMUM_INIT_TRY = 1000


def random_uniform_exclusive(lower: float, upper: float) -> float:
    """
    Generate a random float value between `lower` and `upper` bounds, excluding the bounds themselves.
    If the random value equals either bound, it will retry until a valid value is found or the maximum number of tries
    is reached.

    Parameters
    ----------
    lower: float
        The lower bound of the range.
    upper: float
        The upper bound of the range.

    Returns
    -------
    float
        A random float value between `lower` and `upper`, excluding the bounds.

    Raises
    ------
    ValueError
        If the maximum number of tries is reached without finding a valid value.

    """
    count = 0
    while count < MAXIMUM_INIT_TRY:
        value = uniform(lower, upper)  # noqa: S311
        if value not in (lower, upper):
            return value
        count += 1
    msg = "Random parameter initialization reach maximum try."
    raise ValueError(msg)


def initialize_with_sobol_sampling(
    functional_group_parameters: Sequence[AbstractFunctionalGroup] | FunctionalGroupSet,
    sample_number: int,
    *,
    calc_second_order: bool = False,
) -> pd.DataFrame:
    """
    Generate Sobol samples for the given functional group parameters.
    This function uses the SALib library to generate samples based on the specified functional group parameters.
    """
    if not isinstance(functional_group_parameters, FunctionalGroupSet):
        functional_group_parameters = FunctionalGroupSet(functional_group_parameters)

    name_and_bounds = functional_group_parameters.unique_functional_groups_parameters_ordered()
    bounds = [[i.lower_bound, i.upper_bound] for i in name_and_bounds.values()]
    sp = ProblemSpec({"names": name_and_bounds.keys(), "bounds": bounds})
    samples = sp.sample_sobol(sample_number, calc_second_order=calc_second_order)
    return pd.DataFrame(samples.samples, columns=name_and_bounds.keys())
