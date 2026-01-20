"""Protocol for observations used in cost functions."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class ObservationProtocol(Protocol):
    """Protocol for observations used in cost function evaluation.

    Any observation object used in the optimization framework must implement this protocol.
    Observations represent empirical or reference data against which model predictions are compared.

    Attributes
    ----------
    name : str
        Unique identifier or name of the observation.
    observation : object
        The observation data. The type and structure depend on the cost function processor
        (e.g., xarray.Dataset for time series or spatial data, numpy.ndarray for arrays).

    """

    name: str
    observation: object
