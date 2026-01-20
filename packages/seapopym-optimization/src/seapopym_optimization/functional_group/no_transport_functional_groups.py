"""This module contains the cost function used to optimize the parameters of the SeapoPym model."""

from __future__ import annotations

from dataclasses import dataclass

from seapopym_optimization.functional_group.base_functional_group import AbstractFunctionalGroup, Parameter


@dataclass
class NoTransportFunctionalGroup(AbstractFunctionalGroup):
    """The parameters of a functional group as they are defined in the SeapoPym NoTransport model."""

    day_layer: float | Parameter
    night_layer: float | Parameter
    energy_transfert: float | Parameter
    lambda_temperature_0: float | Parameter
    gamma_lambda_temperature: float | Parameter
    tr_0: float | Parameter
    gamma_tr: float | Parameter
