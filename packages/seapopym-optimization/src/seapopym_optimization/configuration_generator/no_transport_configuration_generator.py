"""Configuration generator for SeapoPym NoTransportModel."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from seapopym.configuration.no_transport import (
    ForcingParameter,
    FunctionalGroupParameter,
    FunctionalGroupUnit,
    FunctionalTypeParameter,
    KernelParameter,
    MigratoryTypeParameter,
    NoTransportConfiguration,
)
from seapopym.model import NoTransportModel

if TYPE_CHECKING:
    from collections.abc import Sequence

    from seapopym_optimization.functional_group.no_transport_functional_groups import NoTransportFunctionalGroup


def no_transport_functional_group_unit_generator(
    functional_group: NoTransportFunctionalGroup,
) -> FunctionalGroupUnit:
    """
    Allows the transformation of a functional group as defined in optimization into a functional group that can be used
    by SeapoPym.

    Based on `FunctionalGroupUnitGeneratorProtocol`.
    """
    return FunctionalGroupUnit(
        name=functional_group.name,
        energy_transfert=functional_group.energy_transfert,
        migratory_type=MigratoryTypeParameter(
            day_layer=functional_group.day_layer,
            night_layer=functional_group.night_layer,
        ),
        functional_type=FunctionalTypeParameter(
            lambda_temperature_0=functional_group.lambda_temperature_0,
            gamma_lambda_temperature=functional_group.gamma_lambda_temperature,
            tr_0=functional_group.tr_0,
            gamma_tr=functional_group.gamma_tr,
        ),
    )


@dataclass
class NoTransportConfigurationGenerator:
    """
    Generate the configuration used to create a NoTransport model in SeapoPym.

    Based on `ConfigurationGeneratorProtocol`.
    """

    model_class: type[NoTransportModel] = NoTransportModel

    def generate(
        self,
        functional_group_parameters: Sequence[NoTransportFunctionalGroup],
        forcing_parameters: ForcingParameter,
        kernel: KernelParameter | None = None,
    ) -> NoTransportConfiguration:
        """Generate a NoTransportConfiguration with the given functional groups and parameters."""
        functional_groups_converted = [
            no_transport_functional_group_unit_generator(fg) for fg in functional_group_parameters
        ]
        return NoTransportConfiguration(
            forcing=forcing_parameters,
            functional_group=FunctionalGroupParameter(functional_group=functional_groups_converted),
            kernel=KernelParameter() if kernel is None else kernel,
        )
