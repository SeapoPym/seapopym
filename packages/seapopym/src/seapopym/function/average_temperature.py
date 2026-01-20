"""An average temperature by fgroup computation wrapper. Use xarray.map_block."""

from __future__ import annotations

from typing import TYPE_CHECKING

import cf_xarray  # noqa: F401
import xarray as xr

from seapopym.core import kernel, template
from seapopym.standard.attributs import average_temperature_by_fgroup_desc
from seapopym.standard.labels import ConfigurationLabels, CoordinatesLabels, ForcingLabels

if TYPE_CHECKING:
    from seapopym.standard.types import SeapopymState


def average_temperature(state: SeapopymState) -> xr.Dataset:
    """Compute the average temperature experienced by each functional group.

    The average temperature is calculated based on the day length and the
    layer positions (day and night) of the functional groups.

    Parameters
    ----------
    state : SeapopymState
        The model state containing temperature, day length, masks and layer configuration.

    Returns
    -------
    xr.Dataset
        A dataset containing the average temperature by functional group.

    """
    temperature = state[ForcingLabels.temperature]
    day_length = state[ForcingLabels.day_length]
    mask_by_fgroup = state[ForcingLabels.mask_by_fgroup]
    day_layer = state[ConfigurationLabels.day_layer]
    night_layer = state[ConfigurationLabels.night_layer]

    average_temperature = []
    for fgroup in day_layer[CoordinatesLabels.functional_group]:
        day_temperature = temperature.sel(Z=day_layer.sel({CoordinatesLabels.functional_group: fgroup}))
        night_temperature = temperature.sel(Z=night_layer.sel({CoordinatesLabels.functional_group: fgroup}))
        mean_temperature = (day_length * day_temperature) + ((1 - day_length) * night_temperature)
        if "Z" in mean_temperature.coords:
            mean_temperature = mean_temperature.drop_vars("Z")
        mean_temperature = mean_temperature.where(mask_by_fgroup.sel({CoordinatesLabels.functional_group: fgroup}))
        average_temperature.append(mean_temperature)

    average_temperature = xr.concat(average_temperature, dim=CoordinatesLabels.functional_group.value)
    with xr.set_options(keep_attrs=True):
        average_temperature = xr.where(average_temperature >= 0, average_temperature, 0)
    return xr.Dataset({ForcingLabels.avg_temperature_by_fgroup: average_temperature})


AverageTemperatureTemplate = template.template_unit_factory(
    name=ForcingLabels.avg_temperature_by_fgroup,
    attributs=average_temperature_by_fgroup_desc,
    dims=[CoordinatesLabels.functional_group, CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
)


AverageTemperatureKernel = kernel.kernel_unit_factory(
    name="average_temperature", template=[AverageTemperatureTemplate], function=average_temperature
)
"""Kernel to compute average temperature by functional group."""

AverageTemperatureKernelLight = kernel.kernel_unit_factory(
    name="average_temperature_light",
    template=[AverageTemperatureTemplate],
    function=average_temperature,
    to_remove_from_state=[ForcingLabels.temperature, ForcingLabels.day_length, ForcingLabels.mask_by_fgroup],
)
"""Light Kernel for average temperature (removes source fields)."""
