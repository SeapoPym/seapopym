"""Error weighted cost function module. Apply a weight to each observation error."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
import xarray as xr
from seapopym.standard.labels import ConfigurationLabels, CoordinatesLabels, ForcingLabels

from seapopym_optimization.cost_function.cost_function import (
    CostFunction,
    DayCycle,
    TimeSeriesObservation,
    aggregate_biomass_by_layer,
)

if TYPE_CHECKING:
    from collections.abc import Sequence


def error_weighted_root_mean_square_error(
    pred: xr.DataArray,
    obs: xr.DataArray,
    error_weight: xr.DataArray,
    *,
    root: bool,
    centered: bool,
    normalized: bool,
) -> float:
    """Error weighted mean square error applied to xr.DataArray."""
    if centered:
        pred = pred - pred.mean()
        obs = obs - obs.mean()
    cost = (pred - obs) / error_weight
    cost = float((cost**2).mean())
    if root:
        cost = np.sqrt(cost)
    if normalized:
        cost /= float(obs.std())
    if not np.isfinite(cost):
        msg = (
            "Nan value in cost function. The observation cannot be compared to the prediction. Verify that "
            "coordinates are fitting both in space and time."
        )
        raise ValueError(msg)
    return cost


@dataclass(kw_only=True)
class ErrorWeightedObservation(TimeSeriesObservation):
    """An observation with an error weight."""

    error_weight: xr.DataArray | None = None

    def __post_init__(self: ErrorWeightedObservation) -> None:
        """Check that the observation data is complient with the format of the predicted biomass."""
        super().__post_init__()
        if not isinstance(self.error_weight, xr.DataArray):
            msg = "Errors weight must be an xarray DataArray."
            raise TypeError(msg)

        if self.error_weight.sum() != self.error_weight.count():
            coef = self.error_weight.count() / self.error_weight.sum()
            self.error_weight = self.error_weight * coef

        if self.error_weight.count() != self.observation.count():
            msg = (
                "The error weight must have the same number of elements as the observation. "
                f"Got {self.error_weight.count()} for the error weight and {self.observation.count()} for the "
                "observation."
            )
            raise ValueError(msg)


@dataclass(kw_only=True)
class ErrorWeightedRMSECostFunction(CostFunction):
    """A cost function that computes the error weighted root mean square error (RMSE) for a SeapoPym model."""

    observations: Sequence[ErrorWeightedObservation]

    def _cost_function(self: ErrorWeightedRMSECostFunction, args: np.ndarray) -> tuple:
        model = self.configuration_generator.generate(
            functional_group_names=self.functional_groups.functional_groups_name(),
            functional_group_parameters=self.functional_groups.generate(args),
        )

        model.run()

        predicted_biomass = model.state[ForcingLabels.biomass]

        biomass_day = aggregate_biomass_by_layer(
            data=predicted_biomass,
            position=model.state[ConfigurationLabels.day_layer].data,
            name=DayCycle.DAY,
            layer_coordinates=model.state.cf[CoordinatesLabels.Z].data,  # TODO(Jules): layer_coordinates ?
        )
        biomass_night = aggregate_biomass_by_layer(
            data=predicted_biomass,
            position=model.state[ConfigurationLabels.night_layer].data,
            name=DayCycle.NIGHT,
            layer_coordinates=model.state.cf[CoordinatesLabels.Z].data,
        )

        return tuple(
            error_weighted_root_mean_square_error(
                pred=obs.resample_data_by_observation_interval(
                    biomass_day if obs.observation_type == DayCycle.DAY else biomass_night
                ),
                obs=obs.observation,
                error_weight=obs.error_weight,
                root=self.root_mse,
                centered=self.centered_mse,
                normalized=self.normalized_mse,
            )
            for obs in self.observations
        )
