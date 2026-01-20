"""Functions used to generate a landmask from any forcing data."""

from __future__ import annotations

from typing import TYPE_CHECKING

import xarray as xr

from seapopym.core import kernel, template
from seapopym.standard.attributs import global_mask_desc
from seapopym.standard.labels import CoordinatesLabels, ForcingLabels

if TYPE_CHECKING:
    from seapopym.standard.types import SeapopymState


def global_mask(state: SeapopymState) -> xr.Dataset:
    """Create a global mask from temperature forcing in the state of the model.

    Parameters
    ----------
    state : SeapopymState
        The model state containing temperature forcing.

    Returns
    -------
    xr.Dataset
        Dataset containing the global mask (True for ocean, False for land).

    """
    mask = state[ForcingLabels.temperature].isel(T=0).notnull().reset_coords("T", drop=True)
    return xr.Dataset({ForcingLabels.global_mask: mask})


GlobalMaskTemplate = template.template_unit_factory(
    name=ForcingLabels.global_mask,
    attributs=global_mask_desc,
    dims=[CoordinatesLabels.Y, CoordinatesLabels.X, CoordinatesLabels.Z],
    dtype=bool,
)


GlobalMaskKernel = kernel.kernel_unit_factory(name="global_mask", template=[GlobalMaskTemplate], function=global_mask)
"""Kernel to compute global mask."""
