"""Observation processing components for cost function evaluation."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Literal

import numpy as np
import xarray as xr
from seapopym.standard.labels import ConfigurationLabels, CoordinatesLabels, ForcingLabels

from seapopym_optimization.observations.observation import DayCycle

if TYPE_CHECKING:
    from collections.abc import Sequence
    from numbers import Number

    import pandas as pd
    from seapopym.standard import SeapopymState

    from seapopym_optimization.cost_function.metric import MetricProtocol
    from seapopym_optimization.observations.protocol import ObservationProtocol
    from seapopym_optimization.observations.spatial import SpatialObservation
    from seapopym_optimization.observations.time_serie import TimeSeriesObservation

logger = logging.getLogger(__name__)


# NOTE(Jules): This function will be used in the future to aggregate biomass by layer so we can compute score for
# spatial observations.
def aggregate_biomass_by_layer(
    data: xr.DataArray,
    position: Sequence[int],
    name: str,
    layer_coordinates: Sequence[int],
    layer_coordinates_name: str = "layer",
) -> xr.DataArray:
    """Aggregate biomass data by layer coordinates."""
    layer_coord = xr.DataArray(
        np.asarray(position),
        dims=[CoordinatesLabels.functional_group],
        coords={CoordinatesLabels.functional_group: data[CoordinatesLabels.functional_group].data},
        name=layer_coordinates_name,
        attrs={"axis": "Z"},
    )
    return (
        data.assign_coords({layer_coordinates_name: layer_coord})
        .groupby(layer_coordinates_name)
        .sum(dim=CoordinatesLabels.functional_group)
        .reindex({layer_coordinates_name: layer_coordinates})
        .fillna(0)
        .rename(name)
    )


class AbstractScoreProcessor(ABC):
    """Abstract class for processing model state and observations to return a score."""

    def __init__(self, comparator: MetricProtocol[xr.DataArray, ObservationProtocol]) -> None:
        """Initialize with a comparator metric."""
        self.comparator = comparator

    @abstractmethod
    def process(self, state: SeapopymState, observation: ObservationProtocol) -> Number:
        """Process model state and observation to return a score."""


class TimeSeriesScoreProcessor(AbstractScoreProcessor):
    """Processes observations in time series format by applying preprocessing and comparison metrics."""

    def __init__(
        self,
        comparator: MetricProtocol[xr.DataArray, ObservationProtocol],
        preprocess: None | Literal["resample", "interpolate"] = None,
    ) -> None:
        """Initialize with a comparator metric."""
        super().__init__(comparator)
        self.preprocess = preprocess

    def _extract_observation_type(
        self: TimeSeriesScoreProcessor, state: SeapopymState, observation_type: DayCycle
    ) -> Sequence[int]:
        """Extract functional group positions based on observation type."""
        if observation_type is DayCycle.DAY:
            return state[ConfigurationLabels.day_layer]
        if observation_type is DayCycle.NIGHT:
            return state[ConfigurationLabels.night_layer]
        msg = f"Unknown observation type: {observation_type}"
        raise ValueError(msg)

    def _format_prediction(
        self: TimeSeriesScoreProcessor,
        prediction: xr.DataArray,
        observation: TimeSeriesObservation,
        fg_positions: Sequence[int],
    ) -> xr.DataArray:
        """Ensure prediction has the correct dimensions."""
        if self.preprocess in ["resample", "interpolate"]:
            prediction = prediction.resample({CoordinatesLabels.time: observation.observation_interval}).mean()
            msg = "Prediction resampled to match observation interval."
            logger.debug(msg)

        if self.preprocess == "interpolate":
            """Interpolate prediction outputs to match observation interval"""
            prediction = prediction.interpolate_na(dim=CoordinatesLabels.time)
            msg = "Interpolate prediction interval to match observation interval."
            logger.info(msg)

        return prediction.sel(
            {
                CoordinatesLabels.functional_group: fg_positions,
                CoordinatesLabels.time: observation.observation[CoordinatesLabels.time],
                CoordinatesLabels.X: observation.observation[CoordinatesLabels.X],
                CoordinatesLabels.Y: observation.observation[CoordinatesLabels.Y],
            },
        )

    def _pre_process_prediction(self, state: SeapopymState, observation: TimeSeriesObservation) -> xr.DataArray:
        """Pre-process prediction to match observation dimensions."""
        fg_positions = self._extract_observation_type(state, observation.observation_type)
        prediction = state[ForcingLabels.biomass]
        prediction = prediction.pint.quantify().pint.to(observation.observation.units).pint.dequantify()
        prediction = self._format_prediction(prediction, observation, fg_positions)

        # Sum over functional_group dimension, squeeze size-1 dimensions
        summed = prediction.sum(CoordinatesLabels.functional_group)
        return summed.squeeze()

    def process(self, state: SeapopymState, observation: TimeSeriesObservation) -> Number:
        """Compare prediction with observation by applying the comparator. Can pre-process data if needed."""
        prediction = self._pre_process_prediction(state, observation)
        return self.comparator(prediction, observation.observation)


class LogTimeSeriesScoreProcessor(TimeSeriesScoreProcessor):
    """Processes observations in time series format by applying log preprocessing and comparison metrics."""

    """Log(1 + biomass) applied to avoid negative values. Observation values must be in mgC/m2."""

    def process(self, state: SeapopymState, observation: TimeSeriesObservation) -> Number:
        """Compare log prediction with log observation by applying the comparator. Can pre-process data if needed."""
        prediction = self._pre_process_prediction(state, observation)
        return self.comparator(xr.ufuncs.log10(1 + prediction), xr.ufuncs.log10(1 + observation.observation))


class SpatialScoreProcessor(AbstractScoreProcessor):
    """Processes observations in spatial format by applying comparison metrics."""

    def _extract_observation_type(
        self: SpatialScoreProcessor, state: SeapopymState, observation_type: DayCycle
    ) -> Sequence[int]:
        """Extract functional group positions based on observation type."""
        if observation_type is DayCycle.DAY:
            return state[ConfigurationLabels.day_layer]
        if observation_type is DayCycle.NIGHT:
            return state[ConfigurationLabels.night_layer]
        msg = f"Unknown observation type: {observation_type}"
        raise ValueError(msg)

    def _pre_process_prediction(self, state: SeapopymState, observation: SpatialObservation) -> xr.DataArray:
        """Pre-process prediction to match observation dimensions."""
        fg_positions = self._extract_observation_type(state, observation.observation_type)
        prediction = state[ForcingLabels.biomass]
        prediction = prediction.pint.quantify().pint.to(observation.observation.units).pint.dequantify()

        # Select the points corresponding to the observation
        # We assume observation has coordinates time, X, Y
        sel_dict = {
            CoordinatesLabels.functional_group: fg_positions,
            CoordinatesLabels.time: observation.observation[CoordinatesLabels.time],
            CoordinatesLabels.X: observation.observation[CoordinatesLabels.X],
            CoordinatesLabels.Y: observation.observation[CoordinatesLabels.Y],
        }
        prediction = prediction.sel(sel_dict, method="nearest")

        # Sum over functional_group dimension, squeeze size-1 dimensions
        summed = prediction.sum(CoordinatesLabels.functional_group)
        return summed.squeeze()

    def process(self, state: SeapopymState, observation: SpatialObservation) -> Number:
        """Compare prediction with observation by applying the comparator."""
        prediction = self._pre_process_prediction(state, observation)
        return self.comparator(prediction, observation.observation)
