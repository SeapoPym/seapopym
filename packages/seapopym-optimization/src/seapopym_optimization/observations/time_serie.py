"""This module contains the cost function used to optimize the parameters of the SeapoPym model."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from seapopym.standard.labels import CoordinatesLabels

from seapopym_optimization.observations.observation import Observation

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class TimeSeriesObservation(Observation):
    """
    The structure used to store the observations as a time series.

    Meaning that the observation is a time series of biomass values at a given location and layer.
    """

    def __post_init__(self: TimeSeriesObservation) -> None:
        """Check that the observation data is compliant with the format of the predicted biomass."""
        super().__post_init__()

        for coord in [CoordinatesLabels.X, CoordinatesLabels.Y, CoordinatesLabels.Z]:
            if self.observation.cf.coords[coord].data.size != 1:
                msg = (
                    f"Multiple {coord} coordinates found in the observation Dataset. "
                    "The observation must be a time series with a single X, Y and Z (i.e. Seapodym layer) coordinate."
                )
                raise ValueError(msg)
