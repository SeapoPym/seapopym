"""All the constraints (as penalty functions) used by the DEAP library to contraint parameters initialization."""

from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from typing import TYPE_CHECKING, Callable

import numpy as np
from deap import tools

if TYPE_CHECKING:
    from collections.abc import Sequence


@dataclass
class EnergyCoefficientConstraint:
    """
    Constraint to ensure that the sum of all energy transfert coefficients is within a specified range.
    This constraint is used to apply a penalty if the sum of the coefficients is greater than `max_energy_coef_value`
    or less than `min_energy_coef_value`.
    Attributes.
    ----------
        parameters_name: Sequence[str]
            The names of the parameters that are involved in the constraint, typically the energy transfert
            coefficients.
        min_energy_coef_value: float
            The minimum allowed value for the sum of the energy transfert coefficients.
        max_energy_coef_value: float
            The maximum allowed value for the sum of the energy transfert coefficients.
    """

    parameters_name: Sequence[str]
    min_energy_coef_value: float
    max_energy_coef_value: float

    def _feasible(self, selected_index: list[int]) -> Callable[[Sequence[float]], bool]:
        """
        The penalty when the sum of all energy transfert coefficients are greater than `max_energy_coef_value` or less
        than `min_energy_coef_value`.
        """

        def feasible(individual: Sequence[float], min_coef: float, max_coef: float) -> bool:
            total_coef = sum([individual[i] for i in selected_index])
            return min_coef <= total_coef <= max_coef

        return partial(feasible, min_coef=self.min_energy_coef_value, max_coef=self.max_energy_coef_value)

    def generate(self, parameter_names: list[str]) -> tools.DeltaPenalty:
        """
        Generate the DeltaPenalty object used by the DEAP library to apply the penalty on individuals that do not
        satisfy the constraint.
        """

        def generate_index(ordered_names: list[str]) -> list[int]:
            """
            List the index of the `parameters_name` in the `ordered_names` sequence. This should be used by the feasible
            function to retrive the position of the selected parameters.
            """
            return [ordered_names.index(param) for param in self.parameters_name]

        feasible = self._feasible(selected_index=generate_index(parameter_names))
        return tools.DeltaPenalty(feasibility=feasible, delta=np.inf)
