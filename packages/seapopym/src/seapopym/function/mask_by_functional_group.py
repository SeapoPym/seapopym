"""Functions used to generate a landmask from any forcing data."""

from __future__ import annotations

from typing import TYPE_CHECKING

import xarray as xr

from seapopym.core import kernel, template
from seapopym.standard.attributs import mask_by_fgroup_desc
from seapopym.standard.labels import ConfigurationLabels, CoordinatesLabels, ForcingLabels

if TYPE_CHECKING:
    from seapopym.standard.types import SeapopymState


def mask_by_fgroup(state: SeapopymState) -> xr.Dataset:
    """Compute the mask for each functional group based on their day and night layers.

    The mask is True if the cell is ocean (from global mask) at both day and night depths.

    Parameters
    ----------
    state : SeapopymState
        The model state containing day/night layers and global mask.

    Returns
    -------
    xr.Dataset
        Dataset containing the mask by functional group.

    """
    day_layers = state[ConfigurationLabels.day_layer]
    night_layers = state[ConfigurationLabels.night_layer]
    global_mask = state[ForcingLabels.global_mask]

    masks = []
    for i in day_layers[CoordinatesLabels.functional_group]:
        day_pos = day_layers.sel(functional_group=i)
        night_pos = night_layers.sel(functional_group=i)

        day_mask = global_mask.sel(Z=day_pos)
        night_mask = global_mask.sel(Z=night_pos)
        masks.append(day_mask & night_mask)

    mask_by_fgroup = xr.DataArray(
        dims=(CoordinatesLabels.functional_group, global_mask["Y"].name, global_mask["X"].name),
        coords={
            CoordinatesLabels.functional_group: day_layers[CoordinatesLabels.functional_group],
            global_mask["Y"].name: global_mask["Y"],
            global_mask["X"].name: global_mask["X"],
        },
        data=masks,
    )
    return xr.Dataset({ForcingLabels.mask_by_fgroup: mask_by_fgroup})


MaskByFunctionalGroupTemplate = template.template_unit_factory(
    name=ForcingLabels.mask_by_fgroup,
    attributs=mask_by_fgroup_desc,
    dims=[CoordinatesLabels.functional_group, CoordinatesLabels.Y, CoordinatesLabels.X],
    dtype=bool,
)


MaskByFunctionalGroupKernel = kernel.kernel_unit_factory(
    name="mask_by_fgroup", template=[MaskByFunctionalGroupTemplate], function=mask_by_fgroup
)
"""Kernel to compute mask by functional group."""

MaskByFunctionalGroupKernelLight = kernel.kernel_unit_factory(
    name="mask_by_fgroup_light",
    template=[MaskByFunctionalGroupTemplate],
    function=mask_by_fgroup,
    to_remove_from_state=[ForcingLabels.global_mask],
)
"""Light Kernel for mask by functional group (removes global mask)."""
