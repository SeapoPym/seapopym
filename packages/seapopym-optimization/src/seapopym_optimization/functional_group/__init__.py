"""Functional groups for the optimization framework.

This module defines functional groups that specify model parameters and their optimization bounds
for different SeapoPym model variants. Each functional group represents a set of parameters
that can be jointly optimized (e.g., no-transport, acidity, pteropods bed variants).

Classes
-------
Parameter
    The definition of a parameter to optimize, including name and bounds.
FunctionalGroupSet
    Generic container for functional group instances.
NoTransportFunctionalGroup
    Functional group for no-transport model variant.
AcidityFunctionalGroup
    Functional group for acidity model variant.
PteropodBedFunctionalGroup
    Functional group for pteropods bed model variant.
PteropodBedBHFunctionalGroup
    Functional group for pteropods bed with biomass harvesting model variant.
PteropodBedBHPFTFunctionalGroup
    Functional group for pteropods bed with biomass harvesting and plant functional types model variant.

Functions
---------
random_uniform_exclusive
    Initialize parameters with random uniform distribution excluding bounds.
initialize_with_sobol_sampling
    Initialize parameters using Sobol quasi-random sampling.
"""

from .acidity_functional_groups import AcidityFunctionalGroup
from .base_functional_group import FunctionalGroupSet, Parameter
from .no_transport_functional_groups import NoTransportFunctionalGroup
from .parameter_initialization import (
    initialize_with_sobol_sampling,
    random_uniform_exclusive,
)
from .pteropods_bed_bh_functional_groups import PteropodBedBHFunctionalGroup
from .pteropods_bed_bh_pft_functional_groups import PteropodBedBHPFTFunctionalGroup
from .pteropods_bed_functional_groups import PteropodBedFunctionalGroup

__all__ = [
    "AcidityFunctionalGroup",
    "FunctionalGroupSet",
    "NoTransportFunctionalGroup",
    "Parameter",
    "PteropodBedBHFunctionalGroup",
    "PteropodBedBHPFTFunctionalGroup",
    "PteropodBedFunctionalGroup",
    "initialize_with_sobol_sampling",
    "random_uniform_exclusive",
]
