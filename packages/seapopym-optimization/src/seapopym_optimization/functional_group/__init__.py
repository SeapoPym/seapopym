"""Functional groups for the optimization framework.

This module defines functional groups that specify model parameters and their optimization bounds
for different SeapoPym model variants. Each functional group represents a set of parameters
that can be jointly optimized.

Classes
-------
Parameter
    The definition of a parameter to optimize, including name and bounds.
FunctionalGroupSet
    Generic container for functional group instances.
NoTransportFunctionalGroup
    Functional group for no-transport model variant.

Functions
---------
random_uniform_exclusive
    Initialize parameters with random uniform distribution excluding bounds.
initialize_with_sobol_sampling
    Initialize parameters using Sobol quasi-random sampling.
"""

from .base_functional_group import FunctionalGroupSet, Parameter
from .no_transport_functional_groups import NoTransportFunctionalGroup
from .parameter_initialization import (
    initialize_with_sobol_sampling,
    random_uniform_exclusive,
)

__all__ = [
    "FunctionalGroupSet",
    "NoTransportFunctionalGroup",
    "Parameter",
    "initialize_with_sobol_sampling",
    "random_uniform_exclusive",
]
