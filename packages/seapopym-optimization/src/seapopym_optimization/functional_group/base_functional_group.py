"""
A module that contains the base class for functional groups declaration and parameter management in optimization
process.
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, fields
from itertools import chain
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


@dataclass
class Parameter:
    """
    The definition of a parameter to optimize.

    Parameters
    ----------
    name: str
        The name of the parameter.
    lower_bound: float
        The lower bound of the parameter.
    upper_bound: float
        The upper bound of the parameter.
    init_method: Callable[[float, float], float], optional
        The method used to get the initial value of a parameter. Default is a random uniform distribution that exclude
        the bounds values.

    """

    name: str
    lower_bound: float
    upper_bound: float
    init_method: Callable[[float, float], float]

    def __post_init__(self: Parameter) -> None:
        """Check that the parameter is correctly defined."""
        if self.lower_bound >= self.upper_bound:
            msg = f"Lower bounds ({self.lower_bound}) must be <= to upper bound ({self.upper_bound})."
            raise ValueError(msg)


@dataclass
class AbstractFunctionalGroup(ABC):
    """The Generic structure used to store the parameters of a functional group as used in SeapoPym."""

    name: str

    @property
    def parameters(self: AbstractFunctionalGroup) -> tuple:
        """Return the parameters representing the functional group. Order of declaration is preserved."""
        excluded = ("name",)
        return tuple(getattr(self, field.name) for field in fields(self) if field.name not in excluded)

    def as_dict(self: AbstractFunctionalGroup) -> dict:
        """Return the functional group as a dictionary with parameter names as keys (without functional group name)."""
        return {field.name: getattr(self, field.name) for field in fields(self) if field.name != "name"}

    def get_parameters_to_optimize(self: AbstractFunctionalGroup) -> Sequence[Parameter]:
        """Return the parameters to optimize as a sequence of `Parameter`."""
        return tuple(param for param in self.parameters if isinstance(param, Parameter))


@dataclass
class FunctionalGroupSet[T: AbstractFunctionalGroup]:
    """The structure used to generate the matrix of all parameters for all functional groups."""

    functional_groups: Sequence[T]

    def __post_init__(self: FunctionalGroupSet) -> None:
        """Check that the functional groups are correctly typed."""
        if not all(isinstance(group, AbstractFunctionalGroup) for group in self.functional_groups):
            msg = "All functional groups must be instances of AbstractFunctionalGroup."
            raise TypeError(msg)

    def functional_groups_name(self: FunctionalGroupSet) -> Sequence[str]:
        """Return the ordered list of the functional groups name."""
        return tuple(group.name for group in self.functional_groups)

    def unique_functional_groups_parameters_ordered(self: FunctionalGroupSet) -> dict[str, Parameter]:
        """
        Return the unique optimized parameters of all functional groups in the order of declaration.

        Used to setup toolbox for optimization algorithms.
        """
        all_param = tuple(chain.from_iterable(group.get_parameters_to_optimize() for group in self.functional_groups))
        unique_params = {}
        for param in all_param:
            if param.name not in unique_params:
                unique_params[param.name] = param
        return unique_params

    def generate(self: FunctionalGroupSet, x: Sequence[float]) -> list[T]:
        """
        Generate a list of dictionaries representing the functional groups with their parameters values.
        The order of the parameters is defined by the `unique_functional_groups_parameters_ordered` method.
        The input `x` should match the order of the parameters returned by that method.
        It is used by the `configuration_generator` to generate the model.

        Parameters
        ----------
        x: Sequence[float]
            A sequence of float values representing the parameters to set for each functional group.

        Returns
        -------
        list[AbstractFunctionalGroup]
            A list of functional groups with their parameters and their corresponding values.

        """
        keys = list(self.unique_functional_groups_parameters_ordered().keys())

        try:
            parameters_values = dict(zip(keys, x, strict=True))
        except ValueError as e:
            msg = (
                f"Cost function parameters {x} do not match the expected parameters {keys}. "
                "Please check your parameters definition."
            )
            raise ValueError(msg) from e

        result = []
        for group in self.functional_groups:
            param_names = list(group.as_dict().keys())
            param_values = [
                parameters_values.get(param.name, np.nan) if isinstance(param, Parameter) else param
                for param in group.parameters
            ]
            # Create dictionary with updated parameter values and preserve the name
            group_dict = dict(zip(param_names, param_values, strict=True))
            group_dict["name"] = group.name
            # Use type(group) instead of T to instantiate the concrete class
            result.append(type(group)(**group_dict))
        return result
