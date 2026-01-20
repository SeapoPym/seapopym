"""Configuration for acidity model with Bednarsek mortality, Beverton-Holt recruitment and PFT."""

from attrs import field, frozen

from seapopym.configuration import acidity_bed_bh
from seapopym.configuration.acidity_bed_bh_pft.functional_group_parameter import FunctionalGroupParameter


@frozen(kw_only=True)
class AcidityBedBHPFTConfiguration(acidity_bed_bh.AcidityBedBHConfiguration):
    """Configuration for acidity model using Bednarsek mortality, Beverton-Holt recruitment and PFT."""

    functional_group: FunctionalGroupParameter = field(
        metadata={
            "description": "The functional group parameters for the Bednarsek-Beverton-Holt-PFT-Acidity configuration."
        }
    )
