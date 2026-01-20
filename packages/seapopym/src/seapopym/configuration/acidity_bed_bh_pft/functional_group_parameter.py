"""Functional group parameters for acidity model with Bednarsek mortality, Beverton-Holt recruitment and PFT."""

from functools import partial

import pint
from attrs import field, frozen, validators

from seapopym.configuration import acidity_bed_bh
from seapopym.configuration.validation import verify_parameter_init
from seapopym.standard.labels import ConfigurationLabels
from seapopym.standard.units import StandardUnitsLabels


@frozen(kw_only=True)
class FunctionalTypeParameter(acidity_bed_bh.FunctionalTypeParameter):
    """Functional type parameters including Phytoplankton Functional Types (PFT).

    Extends the Bednarsek and Beverton-Holt parameters with PFT-based food efficiency:
    - Weights for different phytoplankton types (pico, nano, micro)
    - Half-saturation constant (ks) for food efficiency

    Attributes
    ----------
    w_pico : pint.Quantity
        Weight of picophytoplankton (dimensionless).
    w_nano : pint.Quantity
        Weight of nanophytoplankton (dimensionless).
    w_micro : pint.Quantity
        Weight of microphytoplankton (dimensionless).
    ks : pint.Quantity
        Half-saturation constant for food efficiency (concentration units).

    """

    w_pico: pint.Quantity = field(
        alias=ConfigurationLabels.w_pico,
        converter=partial(verify_parameter_init, unit="dimensionless", parameter_name=ConfigurationLabels.w_pico),
        validator=validators.ge(0),
        metadata={
            "description": "Weight of picophytoplankton",
        },
    )
    w_nano: pint.Quantity = field(
        alias=ConfigurationLabels.w_nano,
        converter=partial(verify_parameter_init, unit="dimensionless", parameter_name=ConfigurationLabels.w_nano),
        validator=validators.ge(0),
        metadata={
            "description": "Weight of nanophytoplankton",
        },
    )
    w_micro: pint.Quantity = field(
        alias=ConfigurationLabels.w_micro,
        converter=partial(verify_parameter_init, unit="dimensionless", parameter_name=ConfigurationLabels.w_micro),
        validator=validators.ge(0),
        metadata={
            "description": "Weight of microphytoplankton",
        },
    )
    ks: pint.Quantity = field(
        alias=ConfigurationLabels.ks,
        converter=partial(
            verify_parameter_init, unit=StandardUnitsLabels.concentration.units, parameter_name=ConfigurationLabels.ks
        ),
        validator=validators.ge(0),
        metadata={
            "description": "Saturation constant for food efficiency",
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
