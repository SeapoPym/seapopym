"""Configuration parameters for the AcidityModel.

This module defines the configuration classes specifically for the model version
that includes acidity-induced mortality.
"""

from .configuration import AcidityConfiguration
from .forcing_parameter import ForcingParameter
from .functional_group_parameter import FunctionalGroupParameter, FunctionalGroupUnit, FunctionalTypeParameter

__all__ = [
    "AcidityConfiguration",
    "ForcingParameter",
    "FunctionalGroupParameter",
    "FunctionalGroupUnit",
    "FunctionalTypeParameter",
]
