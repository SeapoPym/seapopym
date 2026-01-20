"""Configuration for acidity model with Bednarsek mortality and Beverton-Holt recruitment."""

from attrs import field, frozen

from seapopym.configuration import acidity_bed
from seapopym.configuration.acidity_bed_bh.functional_group_parameter import FunctionalGroupParameter


@frozen(kw_only=True)
class AcidityBedBHConfiguration(acidity_bed.AcidityBedConfiguration):
    """Configuration for acidity model using Bednarsek mortality and Beverton-Holt recruitment."""

    functional_group: FunctionalGroupParameter = field(
        metadata={
            "description": "The functional group parameters for the Bednarsek-Beverton-Holt acidity configuration."
        }
    )
