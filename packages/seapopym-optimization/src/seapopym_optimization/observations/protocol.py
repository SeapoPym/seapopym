"""Protocol for observations used in cost functions."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class ObservationProtocol(Protocol):
    """Protocol for observations used in cost functions."""

    name: str
    observation: object
