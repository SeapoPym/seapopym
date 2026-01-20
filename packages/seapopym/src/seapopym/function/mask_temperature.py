"""A temperature mask computation wrapper. Use xarray.map_block."""

from __future__ import annotations

from typing import TYPE_CHECKING

import xarray as xr

from seapopym.core import kernel, template
from seapopym.standard.attributs import mask_temperature_desc
from seapopym.standard.labels import CoordinatesLabels, ForcingLabels

if TYPE_CHECKING:
    from seapopym.standard.types import SeapopymState


def mask_temperature(state: SeapopymState) -> xr.Dataset:
    """Compute the temperature mask based on minimum temperature requirements.

    The mask indicates where the average temperature experienced by the functional
    group is greater than or equal to the minimum temperature required for the
    cohort.

    Parameters
    ----------
    state : SeapopymState
        The model state containing average temperature by functional group and minimum temperature by cohort.

    Returns
    -------
    xr.Dataset
        Dataset containing the temperature mask.

    Notes
    -----
    This function involves a comparison between functional group average temperatures and
    cohort-specific minimum temperatures, resulting in a potentially large boolean array.

    """
    average_temperature = state[ForcingLabels.avg_temperature_by_fgroup]
    min_temperature = state[ForcingLabels.min_temperature]
    mask_temperature = average_temperature >= min_temperature
    return xr.Dataset({ForcingLabels.mask_temperature: mask_temperature})


MaskTemperatureTemplate = template.template_unit_factory(
    name=ForcingLabels.mask_temperature,
    attributs=mask_temperature_desc,
    dims=[
        CoordinatesLabels.functional_group,
        CoordinatesLabels.time,
        CoordinatesLabels.Y,
        CoordinatesLabels.X,
        CoordinatesLabels.cohort,
    ],
    dtype=bool,
)


MaskTemperatureKernel = kernel.kernel_unit_factory(
    name="mask_temperature", template=[MaskTemperatureTemplate], function=mask_temperature
)
"""Kernel to compute temperature mask."""

MaskTemperatureKernelLight = kernel.kernel_unit_factory(
    name="mask_temperature_light",
    template=[MaskTemperatureTemplate],
    function=mask_temperature,
    to_remove_from_state=[ForcingLabels.min_temperature],
)
"""Light Kernel for temperature mask (removes min temperature)."""
