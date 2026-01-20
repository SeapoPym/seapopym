"""
Protocols for SeapoPym optimization algorithms and components. You must follow instructions in this module if you want
to implement a new component for optimization.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Sequence

    from seapopym.standard.protocols import (
        ConfigurationProtocol,
        ForcingParameterProtocol,
        FunctionalGroupUnitProtocol,
        KernelParameterProtocol,
        ModelProtocol,
    )

    from seapopym_optimization.functional_group.base_functional_group import AbstractFunctionalGroup


class FunctionalGroupUnitGeneratorProtocol[T: AbstractFunctionalGroup, U: FunctionalGroupUnitProtocol](Protocol):
    """Protocol for functional group unit generators used in model generation."""

    def __call__(self, functional_group: T) -> U:
        """Generate a FunctionalGroupUnit from the given functional group."""
        ...


@runtime_checkable
class ConfigurationGeneratorProtocol[T: AbstractFunctionalGroup, V: ConfigurationProtocol](Protocol):
    """
    Protocol for configuration generators in SeapoPym optimization.

    It start from the functional group in optimization format (type T), generates the corresponding functional group in
    SeapoPym format, and then generates a SeapoPym configuration (type V) using the generated functional groups
    along with forcing and kernel parameters.
    """

    model_class: type[ModelProtocol]

    def generate(
        self,
        functional_group_parameters: Sequence[T],
        forcing_parameters: ForcingParameterProtocol,
        kernel: KernelParameterProtocol | None = None,
    ) -> V:
        """Generate a SeapoPym configuration with the given parameters."""
        ...
