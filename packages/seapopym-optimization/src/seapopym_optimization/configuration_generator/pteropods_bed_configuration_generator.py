"""Configuration generator for SeapoPym pteropods from Bednarsek equations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from seapopym.configuration.acidity import (
    ForcingParameter,
)
from seapopym.configuration.acidity_bed import (
    AcidityBedConfiguration,
    FunctionalGroupParameter,
    FunctionalGroupUnit,
    FunctionalTypeParameter,
)
from seapopym.configuration.no_transport import (
    KernelParameter,
    MigratoryTypeParameter,
)
from seapopym.model import AcidityBedModel

if TYPE_CHECKING:
    from collections.abc import Sequence

    from seapopym_optimization.functional_group.pteropods_bed_functional_groups import PteropodBedFunctionalGroup


def pteropod_bed_functional_group_unit_generator(
    functional_group: PteropodBedFunctionalGroup,
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
            lambda_0=functional_group.lambda_0,
            gamma_lambda_temperature=functional_group.gamma_lambda_temperature,
            gamma_lambda_acidity=functional_group.gamma_lambda_acidity,
            tr_0=functional_group.tr_0,
            gamma_tr=functional_group.gamma_tr,
            gamma_survival_rate_temperature=functional_group.gamma_survival_rate_temperature,
            gamma_survival_rate_acidity=functional_group.gamma_survival_rate_acidity,
            survival_rate_0=functional_group.survival_rate_0,
        ),
    )


@dataclass
class PteropodsBedConfigurationGenerator:
    """
    Generate the configuration used to create a Pteropod model in SeapoPym based on Bednarsek equations.

    Based on `ConfigurationGeneratorProtocol`.
    """

    model_class: type[AcidityBedModel] = AcidityBedModel

    def generate(
        self,
        functional_group_parameters: Sequence[PteropodBedFunctionalGroup],
        forcing_parameters: ForcingParameter,
        kernel: KernelParameter | None = None,
    ) -> AcidityBedConfiguration:
        """Generate a AcidityBedConfiguration with the given functional groups and parameters."""
        functional_groups_converted = [
            pteropod_bed_functional_group_unit_generator(fg) for fg in functional_group_parameters
        ]
        return AcidityBedConfiguration(
            forcing=forcing_parameters,
            functional_group=FunctionalGroupParameter(functional_group=functional_groups_converted),
            kernel=KernelParameter() if kernel is None else kernel,
        )
