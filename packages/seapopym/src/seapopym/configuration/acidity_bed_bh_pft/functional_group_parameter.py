"""Functional group parameters for acidity model with Bednarsek mortality and Beverton-Holt recruitment."""

from functools import partial

import pint
from attrs import field, frozen, validators

from seapopym.configuration import acidity_bed_bh
from seapopym.configuration.validation import verify_parameter_init
from seapopym.standard.labels import ConfigurationLabels
from seapopym.standard.units import StandardUnitsLabels


@frozen(kw_only=True)
class FunctionalTypeParameter(acidity_bed_bh.FunctionalTypeParameter):
    """
    Functional type parameters with Bednarsek mortality and Beverton-Holt stock-recruitment.

    Extends the Bednarsek parameters with density-dependent recruitment via Beverton-Holt:
    - Stock-recruitment: R = PP * (density_dependance_parameter_a * B) / (1 + density_dependance_parameter_b * B)
    - Where B is biomass and PP is primary production
    """

    w_pico: pint.Quantity = field(
        validator=partial(verify_parameter_init, "dimensionless"),
        metadata={
            "description": "Weight of picophytoplankton",
            "unit": "dimensionless",
            "label": ConfigurationLabels.w_pico,
        },
    )
    w_nano: pint.Quantity = field(
        validator=partial(verify_parameter_init, "dimensionless"),
        metadata={
            "description": "Weight of nanophytoplankton",
            "unit": "dimensionless",
            "label": ConfigurationLabels.w_nano,
        },
    )
    w_micro: pint.Quantity = field(
        validator=partial(verify_parameter_init, "dimensionless"),
        metadata={
            "description": "Weight of microphytoplankton",
            "unit": "dimensionless",
            "label": ConfigurationLabels.w_micro,
        },
    )
    ks: pint.Quantity = field(
        validator=partial(verify_parameter_init, StandardUnitsLabels.concentration.units),
        metadata={
            "description": "Saturation constant for Bednarsek mortality",
            "unit": StandardUnitsLabels.concentration.units,
            "label": ConfigurationLabels.ks,
        },
    )


@frozen(kw_only=True)
class FunctionalGroupUnit(acidity_bed_bh.FunctionalGroupUnit):
    """Represent a functional group with Bednarsek and Beverton-Holt parameters."""

    functional_type: FunctionalTypeParameter = field(
        validator=validators.instance_of(FunctionalTypeParameter),
        metadata={
            "description": (
                "Parameters for temperature/acidity (Bednarsek) and density-dependent recruitment (Beverton-Holt)."
            )
        },
    )


@frozen(kw_only=True)
class FunctionalGroupParameter(acidity_bed_bh.FunctionalGroupParameter):
    """Store parameters for all functional groups using Bednarsek mortality and Beverton-Holt recruitment."""

    functional_group: list[FunctionalGroupUnit] = field(
        metadata={"description": "List of all functional groups with Bednarsek and Beverton-Holt parameters."}
    )
