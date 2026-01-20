"""Seasonality cost function module."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass, field
from functools import partial
from typing import TYPE_CHECKING, Any

import cf_xarray  # noqa: F401
import numpy as np
import pandas as pd
from pygam import LinearGAM, l, s
from seapopym.standard.labels import ConfigurationLabels, CoordinatesLabels, ForcingLabels
from statsmodels.tsa import seasonal

from seapopym_optimization.cost_function.cost_function import (
    CostFunction,
    DayCycle,
    TimeSeriesObservation,
    aggregate_biomass_by_layer,
    root_mean_square_error,
)

if TYPE_CHECKING:
    from numbers import Number

    import xarray as xr


def _patch_pygam() -> None:
    """Since PyGam isn't compatible with python 3.13, we patch it to work with the latest version."""
    np.int = int  # noqa: NPY001

    import scipy.sparse

    scipy.sparse.csr_matrix.A = property(lambda self: self.toarray())


def decompose_gam(
    time: pd.DatetimeIndex,
    data: Sequence[Number],
    n_splines: int = 20,
    *,
    fit_intercept: bool = False,
    seasonal_cycle_length: Number = 365.25,
    log10_data: bool = True,
    **kwargs: dict,
) -> pd.DataFrame:
    """
    Decompose time series using GAM model into trend and seasonality, all the calculations are in the log10 base.

    Parameters
    ----------
    time : pd.DatetimeIndex
        Time index for the data.
    data : Sequence[Number]
        Sequence of data values to decompose.
    n_splines : int, optional
        Number of splines to use for the trend component, by default 20.
    fit_intercept : bool, optional
        Whether to fit an intercept in the GAM model, by default False.
    seasonal_cycle_length : Number, optional
        Length of the seasonal cycle in days, by default 365.25 (for 1 year seasonality).
    **kwargs : dict, optional
        Additional keyword arguments to pass to the LinearGAM constructor.

    Returns
    -------
        pd.DataFrame: DataFrame with 'time', 'trend', 'season', and 'residuals' columns

    """
    _patch_pygam()

    data = (
        pd.DataFrame({"time": time, "data": data})
        .set_index("time")
        .resample("D")
        .mean()
        .interpolate("linear")
        .reset_index()
    )

    data["day_since_start"] = np.cumsum(np.ones_like(data["time"], dtype=int))
    data["sin_doy"] = np.sin(2 * np.pi * data["day_since_start"] / seasonal_cycle_length)
    data["cos_doy"] = np.cos(2 * np.pi * data["day_since_start"] / seasonal_cycle_length)
    x = data[["day_since_start", "sin_doy", "cos_doy"]].to_numpy()
    y = data["data"].to_numpy()
    if log10_data:
        y = np.log10(np.maximum(y, np.finfo(float).eps))

    gam = LinearGAM(s(0, n_splines=n_splines) + l(1) + l(2), fit_intercept=fit_intercept, **kwargs).fit(x, y)
    trend = gam.partial_dependence(term=0, X=x)
    season = gam.partial_dependence(term=1, X=x) + gam.partial_dependence(term=2, X=x)
    residuals = y - trend - season
    return pd.DataFrame({"trend": trend, "seasonal": season, "resid": residuals}, index=data["time"])


def decompose_season_trend_loess(
    time: pd.DatetimeIndex, data: Sequence[Number], period: int = 365, **kwargs: dict
) -> pd.DataFrame:
    """
    Decompose time series using STL decomposition into trend, seasonal, and residuals components.

    Parameters.
    ----------
    time : pd.DatetimeIndex
        Time index for the data.
    data : Sequence[Number]
        Sequence of data values to decompose.
    period : int, optional
        Period of the seasonal component, by default 365 (for 1 year seasonality).
    **kwargs : dict, optional
        Additional keyword arguments to pass to the STL or MSTL constructor.

    Returns
    -------
        pd.DataFrame: DataFrame with 'trend', 'seasonal', and 'resid' columns

    """
    result = seasonal.STL(
        pd.DataFrame({"data": data}, index=time).resample("1D").mean().interpolate("linear"),
        period=period,
        **kwargs,
    ).fit()
    return pd.DataFrame({"trend": result.trend, "seasonal": result.seasonal, "resid": result.resid})


@dataclass
class SeasonalObservation(TimeSeriesObservation, ABC):
    """
    SeasonalObservation is an abstract class that represents a seasonal observation of a time series.
    It contains the trend, seasonal, and residuals components of the time series.
    """

    period: int = 365
    trend: pd.Series | None = None
    seasonal: pd.Series | None = None
    residuals: pd.Series | None = None

    @classmethod
    @abstractmethod
    def from_timeseries_observation(cls, observation: TimeSeriesObservation, period: int = 365) -> SeasonalObservation:
        """Create a SeasonalObservation from a TimeSeriesObservation."""


@dataclass(kw_only=True)
class GAMSeasonalObservation(SeasonalObservation):
    """
    GAMSeasonalObservation is a SeasonalObservation that uses GAM decomposition.
    It contains the trend, seasonal, and residuals components of the time series.
    """

    period: int = 365
    n_splines: int = 20
    fit_intercept: bool = False
    kwargs: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_timeseries_observation(
        cls: GAMSeasonalObservation,
        observation: TimeSeriesObservation,
        period: int = 365,
        *,
        n_splines: int = 20,
        fit_intercept: bool = False,
        **kwargs: dict,
    ) -> GAMSeasonalObservation:
        """Create a GAMSeasonalObservation from a TimeSeriesObservation."""
        result = decompose_gam(
            time=observation.observation.cf.indexes["T"],
            data=observation.observation.squeeze().data,
            n_splines=n_splines,
            fit_intercept=fit_intercept,
            seasonal_cycle_length=period,
            **kwargs,
        )

        return cls(
            name=observation.name,
            observation=observation.observation,
            observation_type=observation.observation_type,
            observation_interval=observation.observation_interval,
            trend=result.trend,
            seasonal=result.seasonal,
            residuals=result.resid,
            period=period,
            n_splines=n_splines,
            fit_intercept=fit_intercept,
            kwargs=kwargs,
        )


@dataclass(kw_only=True)
class STLSeasonalObservation(SeasonalObservation):
    """
    STLSeasonalObservation is a SeasonalObservation that uses MSTL decomposition.
    It contains the trend, seasonal, and residuals components of the time series.
    """

    period: int = 365
    kwargs: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_timeseries_observation(
        cls: STLSeasonalObservation,
        observation: TimeSeriesObservation,
        period: int = 365,
        **kwargs: dict,
    ) -> STLSeasonalObservation:
        """Create a STLSeasonalObservation from a TimeSeriesObservation."""
        result = decompose_season_trend_loess(
            time=observation.observation.cf.indexes["T"],
            data=observation.observation.squeeze().data,
            period=period,
            **kwargs,
        )

        return cls(
            name=observation.name,
            observation=observation.observation,
            observation_type=observation.observation_type,
            observation_interval=observation.observation_interval,
            trend=result.trend,
            seasonal=result.seasonal,
            residuals=result.resid,
            period=period,
            kwargs=kwargs,
        )


def _seasonal_rmse(
    self: CostFunction,
    prediction: xr.DataArray,
    observation: SeasonalObservation,
    *,
    root_mse: bool = True,
    centered_mse: bool = False,
    normalized_mse: bool = False,
) -> Number:
    """Helper function to compute the the seasonal RMSE between the model prediction and the observation."""
    if isinstance(observation, GAMSeasonalObservation):
        decompose_func = partial(
            decompose_gam,
            n_splines=observation.n_splines,
            fit_intercept=observation.fit_intercept,
            seasonal_cycle_length=observation.period,
            **observation.kwargs,
        )
    elif isinstance(observation, STLSeasonalObservation):
        decompose_func = partial(decompose_season_trend_loess, period=observation.period, **observation.kwargs)

    prediction = prediction.cf.sel(
        {
            CoordinatesLabels.X: observation.observation.cf.indexes[CoordinatesLabels.X][0],
            CoordinatesLabels.Y: observation.observation.cf.indexes[CoordinatesLabels.Y][0],
            CoordinatesLabels.Z: observation.observation.cf.indexes[CoordinatesLabels.Z][0],
        }
    )

    prediction_result: pd.DataFrame = decompose_func(time=prediction.cf.indexes["T"], data=prediction.squeeze().data)

    rmse_trend = root_mean_square_error(
        pred=prediction_result.trend,
        obs=observation.trend,
        root=root_mse,
        centered=centered_mse,
        normalized=normalized_mse,
    )

    rmse_seasonal = root_mean_square_error(
        pred=prediction_result.seasonal,
        obs=observation.seasonal,
        root=root_mse,
        centered=centered_mse,
        normalized=normalized_mse,
    )
    return rmse_trend * self.seasonal_weights[0] + rmse_seasonal * self.seasonal_weights[1]


@dataclass(kw_only=True)
class SeasonalityCostFunction(CostFunction, ABC):
    """Abstract class for cost functions that compare model predictions against seasonal observations."""

    seasonal_weights: Sequence[Number]
    observations: Sequence[SeasonalObservation]

    def __post_init__(self: SeasonalityCostFunction) -> None:
        """Check that the kwargs are set."""
        super().__post_init__()
        if not isinstance(self.seasonal_weights, Sequence):
            msg = "Weights must be a sequence of numbers."
            raise TypeError(msg)
        self.seasonal_weights = np.asarray(self.seasonal_weights) / np.sum(self.seasonal_weights)

    def _cost_function(self: SeasonalityCostFunction, args: np.ndarray) -> tuple:
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
            layer_coordinates=model.state.cf[CoordinatesLabels.Z].data,
        )
        biomass_night = aggregate_biomass_by_layer(
            data=predicted_biomass,
            position=model.state[ConfigurationLabels.night_layer].data,
            name=DayCycle.NIGHT,
            layer_coordinates=model.state.cf[CoordinatesLabels.Z].data,
        )

        return tuple(
            _seasonal_rmse(self, biomass_day if obs.observation_type == DayCycle.DAY else biomass_night, obs)
            for obs in self.observations
        )


@dataclass(kw_only=True)
class GAMSeasonalityCostFunction(SeasonalityCostFunction):
    """Cost function that use the GAM decomposition on both the observations and the model predictions."""

    observations: Sequence[GAMSeasonalObservation]

    def __post_init__(self) -> None:
        """Check that the observations are of the correct type."""
        super().__post_init__()
        if not all(isinstance(obs, GAMSeasonalObservation) for obs in self.observations):
            msg = "All observations must be instances of GAMSeasonalObservation."
            raise TypeError(msg)


@dataclass(kw_only=True)
class STLSeasonalityCostFunction(SeasonalityCostFunction):
    """Cost function that use the STL decomposition on both the observations and the model predictions."""

    observations: Sequence[STLSeasonalObservation]

    def __post_init__(self) -> None:
        """Check that the observations are of the correct type."""
        super().__post_init__()
        if not all(isinstance(obs, STLSeasonalObservation) for obs in self.observations):
            msg = "All observations must be instances of STLSeasonalObservation."
            raise TypeError(msg)
