"""Defines the acidity functional group parameters for the SeapoPym Acidity model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from seapopym_optimization.functional_group.no_transport_functional_groups import NoTransportFunctionalGroup

if TYPE_CHECKING:
    from seapopym_optimization.functional_group.base_functional_group import Parameter


@dataclass
class AcidityFunctionalGroup(NoTransportFunctionalGroup):
    """The parameters of a functional group as they are defined in the SeapoPym Acidity model."""

    lambda_acidity_0: float | Parameter
    gamma_lambda_acidity: float | Parameter
