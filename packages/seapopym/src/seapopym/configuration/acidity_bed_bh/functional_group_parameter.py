"""Functional group parameters for acidity model with Bednarsek mortality and Beverton-Holt recruitment."""

from functools import partial

import pint
from attrs import field, frozen, validators

from seapopym.configuration import acidity_bed
from seapopym.configuration.validation import verify_parameter_init
from seapopym.standard.labels import ConfigurationLabels
from seapopym.standard.units import StandardUnitsLabels


@frozen(kw_only=True)
class FunctionalTypeParameter(acidity_bed.FunctionalTypeParameter):
    """
    Functional type parameters with Bednarsek mortality and Beverton-Holt stock-recruitment.

    Extends the Bednarsek parameters with density-dependent recruitment via Beverton-Holt:
    - Stock-recruitment: R = PP * (density_dependance_parameter_a * B) / (1 + density_dependance_parameter_b * B)
    - Where B is biomass and PP is primary production
    """

    density_dependance_parameter_a: pint.Quantity = field(
        alias=ConfigurationLabels.density_dependance_parameter_a,
        converter=partial(
            verify_parameter_init,
            unit=str((1 / StandardUnitsLabels.biomass.units).units),
            parameter_name=ConfigurationLabels.density_dependance_parameter_a,
        ),
        validator=validators.ge(0),
        metadata={
            "description": "Beverton-Holt density dependence parameter numerator (a). "
            "Controls strength of density-dependent recruitment limitation."
        },
    )

    density_dependance_parameter_b: pint.Quantity = field(
        alias=ConfigurationLabels.density_dependance_parameter_b,
        converter=partial(
            verify_parameter_init,
            unit=str((1 / StandardUnitsLabels.biomass.units).units),
            parameter_name=ConfigurationLabels.density_dependance_parameter_b,
        ),
        validator=validators.ge(0),
        metadata={
            "description": "Beverton-Holt density dependence parameter denominator (b). "
            "Controls strength of density-dependent recruitment limitation."
        },
    )


@frozen(kw_only=True)
class FunctionalGroupUnit(acidity_bed.FunctionalGroupUnit):
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
class FunctionalGroupParameter(acidity_bed.FunctionalGroupParameter):
    """Store parameters for all functional groups using Bednarsek mortality and Beverton-Holt recruitment."""

    functional_group: list[FunctionalGroupUnit] = field(
        metadata={"description": "List of all functional groups with Bednarsek and Beverton-Holt parameters."}
    )
