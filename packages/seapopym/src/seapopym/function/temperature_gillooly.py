"""Temperature transformation from Lehodey P. et al. 2010."""

from __future__ import annotations

from typing import TYPE_CHECKING

import cf_xarray  # noqa: F401
import xarray as xr

from seapopym.core import kernel, template
from seapopym.standard.attributs import temperature_gillooly_desc
from seapopym.standard.labels import CoordinatesLabels, ForcingLabels

if TYPE_CHECKING:
    from seapopym.standard.types import SeapopymState


def temperature_gillooly(state: SeapopymState) -> xr.Dataset:
    """
    Apply Gillooly et al. (2002) temperature transformation for metabolic scaling.

    This function transforms temperature to account for metabolic energy allocation
    at the cellular level, following Gillooly et al. (2002) model based on West et al. (1997, 2001).
    The transformation relates temperature to mass-corrected development time and metabolic rates.

    Input
    ------
    - temperature [time, Y, X, Z]

    Output
    ------
    - temperature [time, Y, X, Z]

    Note:
    ----
    The temperature transformation is computed as:
    - T' = T / (1 + T/273)

    Where T is the input temperature and 273 represents the conversion factor
    relating absolute temperature scale to metabolic rates.

    """
    temperature = state[ForcingLabels.temperature]

    temperature = temperature / (1 + temperature / 273)

    return xr.Dataset({ForcingLabels.temperature: temperature})


TemperatureGilloolyTemplate = template.template_unit_factory(
    name=ForcingLabels.temperature,
    attributs=temperature_gillooly_desc,
    dims=[CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X, CoordinatesLabels.Z],
)


TemperatureGilloolyKernel = kernel.kernel_unit_factory(
    name="temperature_gillooly", template=[TemperatureGilloolyTemplate], function=temperature_gillooly
)
