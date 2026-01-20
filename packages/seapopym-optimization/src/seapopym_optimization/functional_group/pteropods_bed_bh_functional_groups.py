"""This module contains the cost function used to optimize the parameters of the SeapoPym model version adapted to pteropods from Bednarsek equations, and considering Berverton Holt density dependance."""

from __future__ import annotations

from dataclasses import dataclass

from seapopym_optimization.functional_group import PteropodBedFunctionalGroup

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from seapopym_optimization.functional_group.base_functional_group import Parameter


@dataclass
class PteropodBedBHFunctionalGroup(PteropodBedFunctionalGroup):
    """The parameters of a functional group as they are defined in the SeapoPym pteropod Bednarsek model, and considering Berverton Holt density dependance."""

    density_dependance_parameter_a: float | Parameter
    density_dependance_parameter_b: float | Parameter
