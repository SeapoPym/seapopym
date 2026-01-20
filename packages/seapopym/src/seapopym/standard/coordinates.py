"""Re-exports coordinate factory functions from coordinate_authority module.

This module provides backwards compatibility by re-exporting functions from
the coordinate_authority module. For new code, prefer importing directly from
seapopym.standard.coordinate_authority or using the CoordinateAuthority class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from seapopym.standard.coordinate_authority import (
    create_cohort_coordinate as new_cohort,
)
from seapopym.standard.coordinate_authority import (
    create_latitude_coordinate as new_latitude,
)
from seapopym.standard.coordinate_authority import (
    create_layer_coordinate as new_layer,
)
from seapopym.standard.coordinate_authority import (
    create_longitude_coordinate as new_longitude,
)
from seapopym.standard.coordinate_authority import (
    create_time_coordinate as new_time,
)
from seapopym.standard.labels import CoordinatesLabels

if TYPE_CHECKING:
    import xarray as xr


def reorder_dims(data: xr.Dataset | xr.DataArray) -> xr.Dataset | xr.DataArray:
    """Follow the standard order of dimensions for a xarray.Dataset or xarray.DataArray.

    This is a convenience wrapper around CoordinatesLabels.order_data().
    For new code, prefer using CoordinatesLabels.order_data() directly.

    Parameters
    ----------
    data : xr.Dataset | xr.DataArray
        The input data to reorder.

    Returns
    -------
    xr.Dataset | xr.DataArray
        The reordered data.

    """
    return CoordinatesLabels.order_data(data)


__all__ = [
    "new_cohort",
    "new_latitude",
    "new_layer",
    "new_longitude",
    "new_time",
    "reorder_dims",
]
