"""Protocols and implementations for metrics to compare model outputs with observations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

import numpy as np

if TYPE_CHECKING:
    from numbers import Number

    from numpy.typing import ArrayLike


@runtime_checkable
class MetricProtocol[U, V](Protocol):
    """
    Protocol for comparing prediction data with observations.

    All future metric functions should follow this protocol.
    """

    def __call__(self, prediction: U, observation: V) -> Number:
        """Compare prediction to observation and return a score."""
        ...


def rmse_comparator(prediction: ArrayLike, observation: ArrayLike) -> Number:
    """Calculate RMSE between prediction and observation."""
    return np.sqrt(np.mean((prediction - observation) ** 2))


def nrmse_std_comparator(prediction: ArrayLike, observation: ArrayLike) -> Number:
    """Calculate Normalized (std) RMSE between prediction and observation."""
    return rmse_comparator(prediction, observation) / observation.std()
