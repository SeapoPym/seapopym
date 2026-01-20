"""Protocol for constraints used in optimization algorithms."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Sequence

    from deap import tools


@runtime_checkable
class ConstraintProtocol(Protocol):
    """Protocol for constraints used in optimization algorithms."""

    def generate(self, parameter_names: Sequence[str]) -> tools.DeltaPenalty:
        """Generate the DEAP DeltaPenalty constraint for the optimization algorithm."""
        ...
