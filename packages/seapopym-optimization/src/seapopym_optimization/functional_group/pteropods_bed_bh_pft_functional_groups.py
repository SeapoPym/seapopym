"""This module contains the cost function used to optimize the parameters of the SeapoPym model version adapted to pteropods from Bednarsek equations, and considering Berverton Holt density dependance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from seapopym_optimization.functional_group.pteropods_bed_bh_functional_groups import PteropodBedBHFunctionalGroup

if TYPE_CHECKING:
    from seapopym_optimization.functional_group.base_functional_group import Parameter


@dataclass
class PteropodBedBHPFTFunctionalGroup(PteropodBedBHFunctionalGroup):
    """The parameters of a functional group as they are defined in the SeapoPym pteropod Bednarsek model, and considering Berverton Holt density dependance."""

    w_pico: float | Parameter
    w_nano: float | Parameter
    w_micro: float | Parameter
    ks: float | Parameter
