"""
Re-exports coordinate factory functions from coordinate_authority module.

This module provides backwards compatibility by re-exporting functions from
the coordinate_authority module. For new code, prefer importing directly from
seapopym.standard.coordinate_authority or using the CoordinateAuthority class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from seapopym.standard.coordinate_authority import (
    create_cohort_coordinate as new_cohort,
    create_latitude_coordinate as new_latitude,
    create_layer_coordinate as new_layer,
    create_longitude_coordinate as new_longitude,
    create_time_coordinate as new_time,
)
from seapopym.standard.labels import CoordinatesLabels

if TYPE_CHECKING:
    import xarray as xr


def reorder_dims(data: xr.Dataset | xr.DataArray) -> xr.Dataset | xr.DataArray:
    """
    Follow the standard order of dimensions for a xarray.Dataset or xarray.DataArray.

    This is a convenience wrapper around CoordinatesLabels.order_data().
    For new code, prefer using CoordinatesLabels.order_data() directly.
    """
    return CoordinatesLabels.order_data(data)


__all__ = [
    "new_latitude",
    "new_longitude",
    "new_layer",
    "new_time",
    "new_cohort",
    "reorder_dims",
]
