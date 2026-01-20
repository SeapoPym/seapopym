"""Compute food efficiency based on phytoplankton functional types (PFT).

This module implements food efficiency calculations based on the relative abundance
of different phytoplankton functional types (picophytoplankton, nanophytoplankton,
and microphytoplankton). The food efficiency represents the suitability of available
phytoplankton for consumption by different functional groups of zooplankton/micronekton.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import cf_xarray  # noqa: F401
import xarray as xr

from seapopym.core import kernel, template
from seapopym.standard.attributs import food_efficiency_desc
from seapopym.standard.labels import ConfigurationLabels, CoordinatesLabels, ForcingLabels

if TYPE_CHECKING:
    from seapopym.standard.types import SeapopymState


def food_efficiency(state: SeapopymState) -> xr.Dataset:
    """
    Calculate food efficiency based on phytoplankton functional types.

    This function computes the food efficiency for each functional group based on
    a weighted combination of three phytoplankton functional types (pico, nano, micro)
    using a Michaelis-Menten-like saturation relationship.

    The food efficiency is calculated as:
        food_eff = weighted_phyto / (ks + weighted_phyto)

    where weighted_phyto is:
        w_pico * chlorophyll_pico + w_nano * chlorophyll_nano + w_micro * chlorophyll_micro

    Input
    -----
    - w_pico [functional_group]: Weight for picophytoplankton (dimensionless)
    - w_nano [functional_group]: Weight for nanophytoplankton (dimensionless)
    - w_micro [functional_group]: Weight for microphytoplankton (dimensionless)
    - chlorophyll_pico [time, latitude, longitude]: Picophytoplankton concentration (g/m³)
    - chlorophyll_nano [time, latitude, longitude]: Nanophytoplankton concentration (g/m³)
    - chlorophyll_micro [time, latitude, longitude]: Microphytoplankton concentration (g/m³)
    - ks [functional_group]: Half-saturation constant (g/m³)

    Output
    ------
    - food_efficiency [functional_group, time, latitude, longitude]: Food efficiency
      coefficient (dimensionless, range 0-1)
    """
    w_pico = state[ConfigurationLabels.w_pico]
    w_nano = state[ConfigurationLabels.w_nano]
    w_micro = state[ConfigurationLabels.w_micro]
    phyto_pico = state[ForcingLabels.chlorophyll_pico]
    phyto_nano = state[ForcingLabels.chlorophyll_nano]
    phyto_micro = state[ForcingLabels.chlorophyll_micro]
    ks = state[ConfigurationLabels.ks]

    food_eff = []
    for fgroup in w_pico[CoordinatesLabels.functional_group]:
        weighted_phyto = (
            w_pico.sel({CoordinatesLabels.functional_group: fgroup}) * phyto_pico
            + w_nano.sel({CoordinatesLabels.functional_group: fgroup}) * phyto_nano
            + w_micro.sel({CoordinatesLabels.functional_group: fgroup}) * phyto_micro
        )
        ks_fgroup = ks.sel({CoordinatesLabels.functional_group: fgroup})
        food_eff.append(weighted_phyto / (ks_fgroup + weighted_phyto))

    food_eff = xr.concat(
        food_eff,
        dim=CoordinatesLabels.functional_group,
        coords=[CoordinatesLabels.functional_group.value]
    )
    food_eff = food_eff.transpose(
        CoordinatesLabels.functional_group,
        CoordinatesLabels.time,
        CoordinatesLabels.Y,
        CoordinatesLabels.X
    )

    return xr.Dataset({ForcingLabels.food_efficiency: food_eff})


FoodEfficiencyTemplate = template.template_unit_factory(
    name=ForcingLabels.food_efficiency,
    attributs=food_efficiency_desc,
    dims=[CoordinatesLabels.functional_group, CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
)

FoodEfficiencyKernel = kernel.kernel_unit_factory(
    name="food_efficiency", template=[FoodEfficiencyTemplate], function=food_efficiency
)

FoodEfficiencyKernelLight = kernel.kernel_unit_factory(
    name="food_efficiency_light",
    template=[FoodEfficiencyTemplate],
    function=food_efficiency,
    to_remove_from_state=[
        ForcingLabels.chlorophyll_pico,
        ForcingLabels.chlorophyll_nano,
        ForcingLabels.chlorophyll_micro,
    ],
)
