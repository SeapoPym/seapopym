"""Wrapper for the application of the transfert cooeficient to primary production. Use xarray.map_block."""

from __future__ import annotations

from typing import TYPE_CHECKING

import xarray as xr

from seapopym.core import kernel, template
from seapopym.standard.attributs import apply_coefficient_to_primary_production_desc
from seapopym.standard.labels import ConfigurationLabels, CoordinatesLabels, ForcingLabels

if TYPE_CHECKING:
    from seapopym.standard.types import SeapopymState


def apply_food_efficiency_to_primary_production(state: SeapopymState) -> xr.Dataset:
    """
    Apply food efficiency coefficient to primary production by functional group.

    This function modulates the primary production already scaled by energy transfer
    coefficients with an additional food efficiency factor based on phytoplankton
    functional types (pico, nano, micro).

    Input
    -----
    - primary_production_by_fgroup [functional_group, time, latitude, longitude]
    - food_efficiency [functional_group, time, latitude, longitude]

    Output
    ------
    - primary_production_by_fgroup [functional_group, time, latitude, longitude]
      (updated with food efficiency applied)
    """
    primary_production_by_fgroup = state[ForcingLabels.primary_production_by_fgroup]
    food_efficiency = state[ForcingLabels.food_efficiency]
    pp_with_efficiency = primary_production_by_fgroup * food_efficiency
    return xr.Dataset({ForcingLabels.primary_production_by_fgroup: pp_with_efficiency})


PrimaryProductionByFgroupTemplate = template.template_unit_factory(
    name=ForcingLabels.primary_production_by_fgroup,
    attributs=apply_coefficient_to_primary_production_desc,
    dims=[CoordinatesLabels.functional_group, CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
)


ApplyFoodEfficiencyToPrimaryProductionKernel = kernel.kernel_unit_factory(
    name="apply_food_efficiency_to_primary_production",
    template=[PrimaryProductionByFgroupTemplate],
    function=apply_food_efficiency_to_primary_production,
)
