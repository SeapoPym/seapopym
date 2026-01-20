from __future__ import annotations

from functools import partial

from attrs import field, frozen, validators

from seapopym.configuration import acidity, no_transport
from seapopym.configuration.validation import verify_forcing_init
from seapopym.standard.labels import ForcingLabels
from seapopym.standard.units import StandardUnitsLabels


@frozen(kw_only=True)
class ForcingParameter(acidity.ForcingParameter):
    """This data class extends ForcingParameters to include an acidity forcing field."""

    chlorophyll_pico: no_transport.ForcingUnit = field(
        alias=ForcingLabels.chlorophyll_pico,
        converter=partial(
            verify_forcing_init,
            unit=StandardUnitsLabels.concentration.units,
            parameter_name=ForcingLabels.chlorophyll_pico,
        ),
        validator=validators.instance_of(no_transport.ForcingUnit),
        metadata={"description": "Path to the chlorophyll_pico field."},
    )

    chlorophyll_micro: no_transport.ForcingUnit = field(
        alias=ForcingLabels.chlorophyll_micro,
        converter=partial(
            verify_forcing_init,
            unit=StandardUnitsLabels.concentration.units,
            parameter_name=ForcingLabels.chlorophyll_micro,
        ),
        validator=validators.instance_of(no_transport.ForcingUnit),
        metadata={"description": "Path to the chlorophyll_micro field."},
    )

    chlorophyll_nano: no_transport.ForcingUnit = field(
        alias=ForcingLabels.chlorophyll_nano,
        converter=partial(
            verify_forcing_init,
            unit=StandardUnitsLabels.concentration.units,
            parameter_name=ForcingLabels.chlorophyll_nano,
        ),
        validator=validators.instance_of(no_transport.ForcingUnit),
        metadata={"description": "Path to the chlorophyll_nano field."},
    )
