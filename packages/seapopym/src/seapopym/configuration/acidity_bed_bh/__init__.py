"""Configuration for acidity model with Bednarsek mortality and Beverton-Holt recruitment."""

from seapopym.configuration.acidity_bed_bh.configuration import AcidityBedBHConfiguration
from seapopym.configuration.acidity_bed_bh.functional_group_parameter import (
    FunctionalGroupParameter,
    FunctionalGroupUnit,
    FunctionalTypeParameter,
)

__all__ = [
    "AcidityBedBHConfiguration",
    "FunctionalGroupParameter",
    "FunctionalGroupUnit",
    "FunctionalTypeParameter",
]
