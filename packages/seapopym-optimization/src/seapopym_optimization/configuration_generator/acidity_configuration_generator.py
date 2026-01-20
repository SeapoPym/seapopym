"""Configuration generator for SeapoPym AcidityModel."""

from __future__ import annotations

from typing import TYPE_CHECKING

from seapopym.configuration.acidity import (
    AcidityConfiguration,
    ForcingParameter,
    FunctionalGroupParameter,
    FunctionalGroupUnit,
    FunctionalTypeParameter,
)
from seapopym.configuration.no_transport import (
    KernelParameter,
    MigratoryTypeParameter,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from seapopym_optimization.functional_group.acidity_functional_groups import AcidityFunctionalGroup


def acidity_functional_group_unit_generator(
    functional_group: AcidityFunctionalGroup,
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
            lambda_acidity_0=functional_group.lambda_acidity_0,
            gamma_lambda_acidity=functional_group.gamma_lambda_acidity,
        ),
    )


class AcidityConfigurationGenerator:
    """
    Generate the configuration used to create a Acidity model in SeapoPym.

    Based on `ConfigurationGeneratorProtocol`.
    """

    def generate(
        self,
        functional_groups: Sequence[AcidityFunctionalGroup],
        forcing_parameters: ForcingParameter,
        kernel: KernelParameter | None = None,
    ) -> AcidityConfiguration:
        """Generate a AcidityConfiguration with the given functional groups and parameters."""
        functional_groups_converted = [
            acidity_functional_group_unit_generator(fg) for fg in functional_groups.functional_groups
        ]
        return AcidityConfiguration(
            forcing=forcing_parameters,
            functional_group=FunctionalGroupParameter(functional_group=functional_groups_converted),
            kernel=KernelParameter() if kernel is None else kernel,
        )
