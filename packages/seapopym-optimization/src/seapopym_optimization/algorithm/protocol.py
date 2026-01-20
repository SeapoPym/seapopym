"""Protocols for optimization algorithms and their parameters."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Sequence

    from deap import base

    from seapopym_optimization.algorithm.genetic_algorithm.logbook import OptimizationLog
    from seapopym_optimization.constraint.protocol import ConstraintProtocol
    from seapopym_optimization.cost_function.protocol import CostFunctionProtocol
    from seapopym_optimization.functional_group.no_transport_functional_groups import Parameter


@runtime_checkable
class OptimizationParametersProtocol(Protocol):
    """Protocol for parameters of an optimization algorithm."""

    def generate_toolbox(self, parameters: Sequence[Parameter]) -> base.Toolbox:
        """Return a DEAP toolbox configured with the necessary optimization algorithm functions."""
        ...


@runtime_checkable
class OptimizationAlgorithmProtocol(Protocol):
    """Protocol for an optimization algorithm implementation."""

    cost_function: CostFunctionProtocol
    constraint: Sequence[ConstraintProtocol] | None

    def optimize(self) -> OptimizationLog:
        """Run the optimization algorithm and return the optimization results as an OptimizationLog."""
        ...
