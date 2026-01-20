"""Define the Kernels used in the model.

This module contains the `Kernel` and `KernelUnit` classes, which are the building blocks
of the model's computation graph. It also provides factory functions to create custom
kernel classes.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

import xarray as xr

from seapopym.core.template import Template, TemplateUnit
from seapopym.standard.coordinate_authority import coordinate_authority

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from seapopym.standard.types import SeapopymForcing, SeapopymState

logger = logging.getLogger(__name__)


@dataclass
class KernelUnit:
    """The KernelUnit class is used to define a kernel function that can be applied to the model state.

    It contains the function, its template, and the arguments to be passed to the function.

    Attributes
    ----------
    name : str
        The name of the kernel unit.
    template : Template
        The template defining the expected output structure.
    function : Callable[[SeapopymState], xr.Dataset]
        The function to apply to the state.
    to_remove_from_state : list[str] | None
        List of variables to remove from the state after execution.
    parallel : bool
        Whether to run the function in parallel using Dask. Default is False.

    """

    name: str
    template: Template
    function: Callable[[SeapopymState], xr.Dataset]
    to_remove_from_state: list[str] | None = None
    parallel: bool = False

    def _run_without_dask(self: KernelUnit, state: SeapopymState) -> xr.Dataset:
        """Run the kernel function without Dask.

        Parameters
        ----------
        state : SeapopymState
            The input state.

        Returns
        -------
        xr.Dataset
            The result of the function.

        Raises
        ------
        ValueError
            If a variable defined in the template is missing from the results.

        """
        results = self.function(state)
        for template in self.template.template_unit:
            if template.name not in results:
                msg = f"Variable {template.name} is not in the results."
                raise ValueError(msg)
            results[template.name] = results[template.name].assign_attrs(template.attrs)

        # Template attributes are already validated, no need for additional validation
        return results

    def _map_block_with_dask(self: KernelUnit, state: SeapopymState) -> xr.Dataset:
        """Run the kernel function using Dask's map_blocks.

        Parameters
        ----------
        state : SeapopymState
            The input state.

        Returns
        -------
        xr.Dataset
            The lazy result using Dask.

        """
        result_template = self.template.generate(state)
        return xr.map_blocks(self.function, state, template=result_template)

    def run(self: KernelUnit, state: SeapopymState) -> SeapopymState | SeapopymForcing:
        """Execute the kernel function on the model state and return the results as Dataset.

        Parameters
        ----------
        state : SeapopymState
            The input state.

        Returns
        -------
        SeapopymState | SeapopymForcing
            The result of the kernel execution.

        """
        if self.parallel:
            return self._map_block_with_dask(state)
        return self._run_without_dask(state)


def kernel_unit_factory(
    name: str,
    function: Callable[[SeapopymState], xr.Dataset],
    template: Iterable[type[TemplateUnit]],
    to_remove_from_state: list[str] | None = None,
) -> type[KernelUnit]:
    """Create a custom kernel unit class with the specified name and function.

    Parameters
    ----------
    name : str
        The name to assign to the custom kernel unit class.
    function : Callable
        The function to be used in the kernel unit. It should accept a SeapopymState
        and return a Dataset.
    template : list of TemplateUnit
        A list of TemplateUnit classes to be used in the kernel unit. These TemplateUnits
        must be registered in the `template_unit_registry`. Be aware that **the
        order of the list matters**, as the template units will be applied in
        the order they are listed.
    to_remove_from_state : list of str, optional
        A list of variable names to be removed from the state after the kernel unit
        has been executed. If not provided, no variables will be removed.

    Returns
    -------
    KernelUnit
        A dynamically created kernel unit class with the specified name and
        function.

    Notes
    -----
    The returned class inherits from `KernelUnit` and is initialized with
    the provided function and a chunk dictionary.

    """

    class CustomKernelUnit(KernelUnit):
        def __init__(self, chunk: dict[str, int], parallel: bool = False) -> None:
            super().__init__(
                name=name,
                function=function,
                template=Template(template_unit=[template_class(chunk) for template_class in template]),
                to_remove_from_state=to_remove_from_state,
                parallel=parallel,
            )

    CustomKernelUnit.__name__ = name

    return CustomKernelUnit


class Kernel:
    """The Kernel class is used to define a kernel that can be applied to the model state.

    It contains a list of KernelUnit that will be applied in order.

    Attributes
    ----------
    kernel_unit : list[KernelUnit]
        The list of kernel units to execute.
    parallel : bool
        Whether the kernel is running in parallel mode.

    """

    def __init__(
        self: Kernel, kernel_unit: Iterable[type[KernelUnit]], chunk: dict[str, int], parallel: bool = False
    ) -> None:
        """Initialize the Kernel.

        Parameters
        ----------
        kernel_unit : Iterable[type[KernelUnit]]
            The list of kernel unit classes to instantiate.
        chunk : dict[str, int]
            Chunk sizes for Dask.
        parallel : bool, optional
            Whether to run in parallel. Default is False.

        """
        self.kernel_unit = [ku(chunk, parallel) for ku in kernel_unit]
        self.parallel = parallel

    def run(self: Kernel, state: SeapopymState) -> SeapopymState:
        """Run all kernel_unit in the kernel in order.

        Parameters
        ----------
        state : SeapopymState
            The initial state.

        Returns
        -------
        SeapopymState
            The state after applying all kernel units.

        """
        for ku in self.kernel_unit:
            results = ku.run(state)
            state = results.merge(state, compat="override")
            for var in ku.to_remove_from_state or []:
                if var in state:
                    state = state.drop_vars(var)

        # Ensure coordinate integrity once at the end (templates already validated)
        return coordinate_authority.ensure_coordinate_integrity(state)

    def template(self: Kernel, state: SeapopymState) -> SeapopymState:
        """Generate an empty Dataset that represent the state of the model at the end of execution.

        Useful forsize estimation.
        """
        return xr.merge([state] + [unit.template.generate(state) for unit in self.kernel_unit], compat="override")


def kernel_factory(class_name: str, kernel_unit: list[type[KernelUnit]]) -> Kernel:
    """Create a custom kernel class with the specified name and functions.

    Parameters
    ----------
    class_name : str
        The name to assign to the custom kernel class.
    kernel_unit : list of str
        A list of KernelUnit names to be used in the kernel. These KernelUnits
        must be registered in the `kernel_unit_registry`. Be aware that **the
        order of the list matters**, as the kernel units will be applied in
        the order they are listed.

    Returns
    -------
    Kernel
        A dynamically created kernel class with the specified name and
        kernel units.

    Notes
    -----
    The returned class inherits from `Kernel` and is initialized with
    the provided functions and a chunk dictionary.

    """

    class CustomKernel(Kernel):
        def __init__(self, chunk: dict, parallel: bool = False) -> None:
            super().__init__(kernel_unit=kernel_unit, chunk=chunk, parallel=parallel)

    CustomKernel.__name__ = class_name
    return CustomKernel
