"""The no transport model with acidity-induced mortality.

This module provides several model variations that incorporate the effects of
ocean acidification on pteropod mortality and recruitment. It builds upon
the NoTransportModel (LMTL without advection-diffusion).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from seapopym import function
from seapopym.core.kernel import kernel_factory
from seapopym.model.no_transport_model import NoTransportModel

if TYPE_CHECKING:
    from seapopym.configuration.acidity import AcidityConfiguration
    from seapopym.configuration.acidity_bed import AcidityBedConfiguration
    from seapopym.configuration.acidity_bed_bh import AcidityBedBHConfiguration

AcidityKernel = kernel_factory(
    class_name="AcidityKernel",
    kernel_unit=[
        function.TemperatureGilloolyKernel,
        function.GlobalMaskKernel,
        function.MaskByFunctionalGroupKernel,
        function.DayLengthKernel,
        function.AverageTemperatureKernel,
        function.AverageAcidityKernel,
        function.PrimaryProductionByFgroupKernel,
        function.MinTemperatureByCohortKernel,
        function.MaskTemperatureKernel,
        function.MortalityTemperatureAcidityKernel,
        function.ProductionKernel,
        function.BiomassKernel,
    ],
)


class AcidityModel(NoTransportModel):
    """A pteropod 1D model that takes into account the mortality due to ocean acidification.

    This model extends the NoTransportModel by including acidity fields and
    calculating mortality as a function of temperature and acidity (pH).
    """

    @classmethod
    def from_configuration(cls: type[AcidityModel], configuration: AcidityConfiguration) -> AcidityModel:
        """Create a model from a configuration.

        Parameters
        ----------
        configuration : AcidityConfiguration
            The configuration object containing state and parameters.

        Returns
        -------
        AcidityModel
            An initialized AcidityModel instance.

        """
        state = configuration.state
        chunk = configuration.forcing.chunk.as_dict()
        parallel = configuration.forcing.parallel
        return cls(state=state, kernel=AcidityKernel(chunk=chunk, parallel=parallel))


AcidityBedKernel = kernel_factory(
    class_name="AcidityBedKernel",
    kernel_unit=[
        function.TemperatureGilloolyKernel,
        function.GlobalMaskKernel,
        function.MaskByFunctionalGroupKernel,
        function.DayLengthKernel,
        function.AverageTemperatureKernel,
        function.AverageAcidityKernel,
        function.PrimaryProductionByFgroupKernel,
        function.MinTemperatureByCohortKernel,
        function.MaskTemperatureKernel,
        function.SurvivalRateBednarsekKernel,
        function.MortalityTemperatureAcidityBedKernel,
        function.ProductionKernel,
        function.ApplySurvivalRateToRecruitmentKernel,
        function.BiomassKernel,
    ],
)


class AcidityBedModel(NoTransportModel):
    """A pteropod 1D model using Bednarsek et al. (2022) mortality equation for ocean acidification effects.

    This model specifically uses the relationship derived by Bednarsek et al.
    to link omega/pH levels to pteropod shell dissolution and mortality.
    """

    @classmethod
    def from_configuration(cls: type[AcidityBedModel], configuration: AcidityBedConfiguration) -> AcidityBedModel:
        """Create a model from a configuration.

        Parameters
        ----------
        configuration : AcidityBedConfiguration
            The configuration object.

        Returns
        -------
        AcidityBedModel
            An initialized AcidityBedModel instance.

        """
        state = configuration.state
        chunk = configuration.forcing.chunk.as_dict()
        parallel = configuration.forcing.parallel
        return cls(state=state, kernel=AcidityBedKernel(chunk=chunk, parallel=parallel))


AcidityBedBHKernel = kernel_factory(
    class_name="AcidityBedBHKernel",
    kernel_unit=[
        function.TemperatureGilloolyKernel,
        function.GlobalMaskKernel,
        function.MaskByFunctionalGroupKernel,
        function.DayLengthKernel,
        function.AverageTemperatureKernel,
        function.AverageAcidityKernel,
        function.PrimaryProductionByFgroupKernel,
        function.MinTemperatureByCohortKernel,
        function.MaskTemperatureKernel,
        function.SurvivalRateBednarsekKernel,
        function.MortalityTemperatureAcidityBedKernel,
        function.BiomassBeverttonHoltKernel,
    ],
)


class AcidityBedBHModel(NoTransportModel):
    """A pteropod 1D model using Bednarsek mortality and Beverton-Holt density-dependent recruitment.

    This model combines the Bednarsek acidification mortality with a Beverton-Holt
    stock-recruitment relationship to simulate density dependence.
    """

    @classmethod
    def from_configuration(cls: type[AcidityBedBHModel], configuration: AcidityBedBHConfiguration) -> AcidityBedBHModel:
        """Create a model from a configuration.

        Parameters
        ----------
        configuration : AcidityBedBHConfiguration
            The configuration object.

        Returns
        -------
        AcidityBedBHModel
            An initialized AcidityBedBHModel instance.

        """
        state = configuration.state
        chunk = configuration.forcing.chunk.as_dict()
        parallel = configuration.forcing.parallel
        return cls(state=state, kernel=AcidityBedBHKernel(chunk=chunk, parallel=parallel))


AcidityBedBHSurvivalKernel = kernel_factory(
    class_name="AcidityBedBHSurvivalKernel",
    kernel_unit=[
        function.TemperatureGilloolyKernel,
        function.GlobalMaskKernel,
        function.MaskByFunctionalGroupKernel,
        function.DayLengthKernel,
        function.AverageTemperatureKernel,
        function.AverageAcidityKernel,
        function.PrimaryProductionByFgroupKernel,
        function.MinTemperatureByCohortKernel,
        function.MaskTemperatureKernel,
        function.SurvivalRateBednarsekKernel,
        function.MortalityTemperatureAcidityBedKernel,
        function.BiomassBeverttonHoltSurvivalKernel,
    ],
)


class AcidityBedBHSurvivalModel(NoTransportModel):
    """A pteropod 1D model using Bednarsek mortality, survival rate, and Beverton-Holt recruitment.

    This variation includes explicit survival rate calculation in the recruitment process.
    """

    @classmethod
    def from_configuration(
        cls: type[AcidityBedBHSurvivalModel], configuration: AcidityBedBHConfiguration
    ) -> AcidityBedBHSurvivalModel:
        """Create a model from a configuration.

        Parameters
        ----------
        configuration : AcidityBedBHConfiguration
            The configuration object.

        Returns
        -------
        AcidityBedBHSurvivalModel
            An initialized AcidityBedBHSurvivalModel instance.

        """
        state = configuration.state
        chunk = configuration.forcing.chunk.as_dict()
        parallel = configuration.forcing.parallel
        return cls(state=state, kernel=AcidityBedBHSurvivalKernel(chunk=chunk, parallel=parallel))


AcidityBedBHPFTSurvivalKernel = kernel_factory(
    class_name="AcidityBedBHPFTSurvivalKernel",
    kernel_unit=[
        function.TemperatureGilloolyKernel,
        function.GlobalMaskKernel,
        function.MaskByFunctionalGroupKernel,
        function.DayLengthKernel,
        function.AverageTemperatureKernel,
        function.AverageAcidityKernel,
        function.PrimaryProductionByFgroupKernel,
        function.FoodEfficiencyKernel,
        function.ApplyFoodEfficiencyToPrimaryProductionKernel,
        function.MinTemperatureByCohortKernel,
        function.MaskTemperatureKernel,
        function.SurvivalRateBednarsekKernel,
        function.MortalityTemperatureAcidityBedKernel,
        function.BiomassBeverttonHoltSurvivalKernel,
    ],
)


class AcidityBedBHPFTSurvivalModel(NoTransportModel):
    """A pteropod 1D model using Bednarsek mortality, survival rate, PFT and Beverton-Holt recruitment.

    PFT stands for Phytoplankton Functional Types. This model accounts for the
    different food efficiencies of various phytoplankton types (pico, nano, micro)
    when calculating energy transfer to pteropods.
    """

    @classmethod
    def from_configuration(
        cls: type[AcidityBedBHPFTSurvivalModel], configuration: AcidityBedBHConfiguration
    ) -> AcidityBedBHPFTSurvivalModel:
        """Create a model from a configuration.

        Parameters
        ----------
        configuration : AcidityBedBHConfiguration
            The configuration object.

        Returns
        -------
        AcidityBedBHPFTSurvivalModel
            An initialized AcidityBedBHPFTSurvivalModel instance.

        """
        state = configuration.state
        chunk = configuration.forcing.chunk.as_dict()
        parallel = configuration.forcing.parallel
        return cls(state=state, kernel=AcidityBedBHPFTSurvivalKernel(chunk=chunk, parallel=parallel))
