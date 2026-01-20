"""This module contains the cost function used to optimize the parameters of the SeapoPym model."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum

import pandas as pd
import xarray as xr
from pandas.tseries.frequencies import to_offset
from seapopym.standard.units import StandardUnitsLabels

logger = logging.getLogger(__name__)


class DayCycle(StrEnum):
    """Enum to define the day cycle."""

    DAY = "day"
    NIGHT = "night"


@dataclass(kw_only=True)
class Observation:
    """The structure used to store an observation."""

    name: str
    observation: xr.DataArray
    observation_type: DayCycle = DayCycle.DAY
    observation_interval: pd.offsets.BaseOffset | None = "1D"

    def __post_init__(self: Observation) -> None:
        """Check that the observation data is compliant with the format of the predicted biomass."""
        logger.debug("Checking observation '%s'", self.name)

        if not isinstance(self.observation, xr.DataArray):
            msg = "Observation must be an xarray DataArray."
            raise TypeError(msg)

        for coord in ["T", "X", "Y", "Z"]:
            if coord not in self.observation.cf.coords:
                msg = f"Coordinate {coord} must be in the observation Dataset."
                raise ValueError(msg)

        try:
            self.observation = self.observation.pint.quantify().pint.to(StandardUnitsLabels.biomass).pint.dequantify()
        except Exception as e:
            msg = (
                f"At least one variable is not convertible to {StandardUnitsLabels.biomass}, which is the unit of the "
                "predicted biomass."
            )
            raise ValueError(msg) from e

        if not isinstance(self.observation_interval, (pd.offsets.BaseOffset)):
            self.observation_interval = to_offset(self.observation_interval)
