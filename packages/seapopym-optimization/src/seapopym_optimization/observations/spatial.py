"""This module contains the cost function used to optimize the parameters of the SeapoPym model."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from seapopym.standard.labels import CoordinatesLabels

from seapopym_optimization.observations.observation import Observation

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class SpatialObservation(Observation):
    """
    The structure used to store the observations as a spatial dataset.

    Meaning that the observation is a set of biomass values at given locations and times.
    The observation data must be an xarray.DataArray with a single dimension (e.g. "index" or "obs_id")
    and coordinates for time, latitude, and longitude.
    """

    def __post_init__(self: SpatialObservation) -> None:
        """Check that the observation data is compliant with the format of the predicted biomass."""
        super().__post_init__()

        # Check for required coordinates
        required_coords = [CoordinatesLabels.time, CoordinatesLabels.X, CoordinatesLabels.Y, CoordinatesLabels.Z]
        for coord in required_coords:
            if coord not in self.observation.coords:
                msg = f"Coordinate {coord} must be in the observation DataArray."
                raise ValueError(msg)
