"""Store all labels used in the No Transport model."""

from __future__ import annotations

from enum import Enum, StrEnum
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    import xarray as xr


class CoordinatesLabels(StrEnum):
    """A single place to store all labels as declared in coordinates module. It follow the cf_xarray convention.

    Attributes
    ----------
    functional_group : str
        Label for functional group dimension.
    time : str
        Label for time dimension (T).
    Y : str
        Label for latitude dimension (Y).
    X : str
        Label for longitude dimension (X).
    Z : str
        Label for depth/layer dimension (Z).
    cohort : str
        Label for cohort dimension.

    """

    functional_group = "functional_group"
    time = "T"
    Y = "Y"
    X = "X"
    Z = "Z"
    cohort = "cohort"

    @classmethod
    def ordered(cls: CoordinatesLabels) -> tuple[CoordinatesLabels, ...]:
        """Return all labels in the order they should be used in a dataset. It follow the CF convention.

        Returns
        -------
        tuple[CoordinatesLabels, ...]
            Tuple of ordered coordinate labels.

        """
        return (cls.functional_group, cls.time, cls.Y, cls.X, cls.Z, cls.cohort)

    @classmethod
    def order_data(cls: CoordinatesLabels, data: xr.Dataset | xr.DataArray) -> xr.Dataset:
        """Return the dataset with the coordinates ordered as in the CF convention.

        Parameters
        ----------
        data : xr.Dataset | xr.DataArray
            The input data.

        Returns
        -------
        xr.Dataset
            The data with transposed dimensions.

        """
        return data.transpose(*cls.ordered(), missing_dims="ignore")


class SeaLayers(Enum):
    """Enumerate the sea layers.

    Attributes
    ----------
    EPI : tuple
        Epipelagic layer (depth 1).
    UPMESO : tuple
        Upper-mesopelagic layer (depth 2).
    LOWMESO : tuple
        Lower-mesopelagic layer (depth 3).

    """

    # NOTE(Jules): The following order of the layers declaration is important.
    ## Since python 3.4 this order is preserved.
    EPI = ("epipelagic", 1)
    UPMESO = ("upper-mesopelagic", 2)
    LOWMESO = ("lower-mesopelagic", 3)

    @property
    def standard_name(
        self: SeaLayers,
    ) -> Literal["epipelagic", "upper-mesopelagic", "lower-mesopelagic"]:
        """Return the standard_name of the sea layer.

        Returns
        -------
        str
            The standard name.

        """
        return self.value[0]

    @property
    def depth(self: SeaLayers) -> Literal[1, 2, 3]:
        """Return the depth of the sea layer.

        Returns
        -------
        int
            The depth index.

        """
        return self.value[1]


class ConfigurationLabels(StrEnum):
    """A single place to store all labels as declared in parameters module.

    Attributes
    ----------
    fgroup_name : str
        Name of the functional group.
    energy_transfert : str
        Energy transfer coefficient.
    lambda_temperature_0 : str
        Lambda temperature zero.
    gamma_lambda_temperature : str
        Gamma lambda temperature.
    lambda_acidity_0 : str
        Lambda acidity zero.
    gamma_lambda_acidity : str
        Gamma lambda acidity.
    tr_0 : str
        Turnover rate zero.
    gamma_tr : str
        Gamma turnover rate.
    day_layer : str
        Day layer position.
    night_layer : str
        Night layer position.
    cohort : str
        Cohort axis.
    timesteps_number : str
        Number of timesteps.
    min_timestep : str
        Minimum timestep.
    max_timestep : str
        Maximum timestep.
    mean_timestep : str
        Mean timestep.
    timestep : str
        Forcing timestep.
    resolution_latitude : str
        Latitude resolution.
    resolution_longitude : str
        Longitude resolution.
    initial_condition_production : str
        Initial condition for production.
    initial_condition_biomass : str
        Initial condition for biomass.
    angle_horizon_sun : str
        Angle of sun above horizon.
    compute_preproduction : str
        Flag to compute preproduction.
    compute_initial_conditions : str
        Flag to compute initial conditions.
    lambda_0 : str
        Bednarsek lambda zero.
    survival_rate_0 : str
        Bednarsek survival rate zero.
    gamma_survival_rate_acidity : str
        Bednarsek gamma survival rate acidity.
    gamma_survival_rate_temperature : str
        Bednarsek gamma survival rate temperature.
    density_dependance_parameter_a : str
        Beverton-Holt density dependence parameter a.
    density_dependance_parameter_b : str
        Beverton-Holt density dependence parameter b.
    w_pico : str
        Weight for pico-phytoplankton.
    w_nano : str
        Weight for nano-phytoplankton.
    w_micro : str
        Weight for micro-phytoplankton.
    ks : str
        Half-saturation constant.

    """

    # Functional group
    fgroup_name = "name"
    energy_transfert = "energy_transfert"
    lambda_temperature_0 = "lambda_temperature_0"
    gamma_lambda_temperature = "gamma_lambda_temperature"
    lambda_acidity_0 = "lambda_acidity_0"
    gamma_lambda_acidity = "gamma_lambda_acidity"
    tr_0 = "tr_0"
    gamma_tr = "gamma_tr"
    day_layer = "day_layer"
    night_layer = "night_layer"
    # Cohorts
    cohort = "cohort"  # New axis
    timesteps_number = "timesteps_number"
    min_timestep = "min_timestep"
    max_timestep = "max_timestep"
    mean_timestep = "mean_timestep"
    # Forcing
    timestep = "timestep"
    resolution_latitude = "resolution_latitude"
    resolution_longitude = "resolution_longitude"
    initial_condition_production = "initial_condition_production"
    initial_condition_biomass = "initial_condition_biomass"
    # Kernel
    angle_horizon_sun = "angle_horizon_sun"
    compute_preproduction = "compute_preproduction"
    compute_initial_conditions = "compute_initial_conditions"
    # Bednarsek
    lambda_0 = "lambda_0"
    survival_rate_0 = "survival_rate_0"
    gamma_survival_rate_acidity = "gamma_survival_rate_acidity"
    gamma_survival_rate_temperature = "gamma_survival_rate_temperature"
    # Beverton-Holt
    density_dependance_parameter_a = "density_dependance_parameter_a"
    density_dependance_parameter_b = "density_dependance_parameter_b"
    # PFT
    w_pico = "w_pico"
    w_nano = "w_nano"
    w_micro = "w_micro"
    ks = "ks"


class ForcingLabels(StrEnum):
    """A single place to store all labels as declared in forcing module.

    Attributes
    ----------
    global_mask : str
        Global land/ocean mask.
    mask_by_fgroup : str
        Mask specific to functional group.
    day_length : str
        Day length.
    avg_temperature_by_fgroup : str
        Average temperature by functional group.
    avg_acidity_by_fgroup : str
        Average acidity by functional group.
    primary_production_by_fgroup : str
        Primary production by functional group.
    min_temperature : str
        Minimum temperature.
    mask_temperature : str
        Mask based on temperature.
    cell_area : str
        Area of grid cells.
    mortality_field : str
        Mortality field.
    recruited : str
        Recruited population.
    preproduction : str
        Pre-recruitment population.
    biomass : str
        Biomass.
    survival_rate : str
        Survival rate.
    temperature : str
        Temperature forcing.
    primary_production : str
        Primary production forcing.
    acidity : str
        Acidity forcing.
    food_efficiency : str
        Food efficiency.
    chlorophyll_micro : str
        Chlorophyll micro-phytoplankton.
    chlorophyll_nano : str
        Chlorophyll nano-phytoplankton.
    chlorophyll_pico : str
        Chlorophyll pico-phytoplankton.

    """

    global_mask = "mask"
    mask_by_fgroup = "mask_fgroup"
    day_length = "day_length"
    avg_temperature_by_fgroup = "average_temperature"
    avg_acidity_by_fgroup = "average_acidity"
    primary_production_by_fgroup = "primary_production_by_fgroup"
    min_temperature = "min_temperature"
    mask_temperature = "mask_temperature"
    cell_area = "cell_area"
    mortality_field = "mortality_field"
    recruited = "recruited"
    preproduction = "preproduction"
    biomass = "biomass"
    survival_rate = "survival_rate"
    temperature = "temperature"
    primary_production = "primary_production"
    acidity = "acidity"
    food_efficiency = "food_efficiency"
    chlorophyll_micro = "chlorophyll_micro"
    chlorophyll_nano = "chlorophyll_nano"
    chlorophyll_pico = "chlorophyll_pico"
