from attrs import field, frozen

from seapopym.configuration.acidity.forcing_parameter import ForcingParameter
from seapopym.configuration.acidity.functional_group_parameter import FunctionalGroupParameter
from seapopym.configuration.no_transport import NoTransportConfiguration


@frozen(kw_only=True)
class AcidityConfiguration(NoTransportConfiguration):
    """Configuration for the AcidityModel."""

    forcing: ForcingParameter = field(metadata={"description": "The forcing parameters for the configuration."})
    functional_group: FunctionalGroupParameter = field(
        metadata={"description": "The functional group parameters for the configuration."}
    )
