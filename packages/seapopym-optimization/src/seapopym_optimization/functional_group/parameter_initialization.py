"""Module for parameter initialization methods for functional groups."""

from __future__ import annotations

import math
from random import uniform
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from SALib import ProblemSpec
from scipy.stats import qmc

from seapopym_optimization.functional_group.base_functional_group import AbstractFunctionalGroup, FunctionalGroupSet

if TYPE_CHECKING:
    from collections.abc import Sequence

MAXIMUM_INIT_TRY = 1000


def random_uniform_exclusive(lower: float, upper: float) -> float:
    """Generate a random float value between `lower` and `upper` bounds, excluding the bounds themselves.

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
    saltelli: bool = True,
) -> pd.DataFrame:
    """Generate Sobol samples for the given functional group parameters.

    With ``saltelli=True`` (default) the SALib Saltelli design is used, yielding
    ``sample_number * (D + 2)`` points (or ``* (2D + 2)`` if ``calc_second_order``) — suitable
    for a Sobol sensitivity analysis. With ``saltelli=False`` a plain scrambled Sobol sequence
    of *exactly* ``sample_number`` points is returned, suitable as a space-filling initial GA
    population (``sample_number`` should be a power of 2 for the Sobol balance property);
    ``calc_second_order`` is then ignored.
    """
    if not isinstance(functional_group_parameters, FunctionalGroupSet):
        functional_group_parameters = FunctionalGroupSet(functional_group_parameters)

    name_and_bounds = functional_group_parameters.unique_functional_groups_parameters_ordered()
    bounds = [[i.lower_bound, i.upper_bound] for i in name_and_bounds.values()]
    if saltelli:
        sp = ProblemSpec({"names": name_and_bounds.keys(), "bounds": bounds})
        samples = sp.sample_sobol(sample_number, calc_second_order=calc_second_order)
        return pd.DataFrame(samples.samples, columns=name_and_bounds.keys())

    lower = np.array([b[0] for b in bounds])
    upper = np.array([b[1] for b in bounds])
    sampler = qmc.Sobol(d=len(bounds), scramble=True)
    power_of_two = round(math.log2(sample_number))
    unit = sampler.random_base2(m=power_of_two) if 2**power_of_two == sample_number else sampler.random(sample_number)
    return pd.DataFrame(qmc.scale(unit, lower, upper), columns=list(name_and_bounds.keys()))
