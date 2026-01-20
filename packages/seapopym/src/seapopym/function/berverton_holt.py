"""
This module contains the function used to compute biomass with Beverton-Holt stock-recruitment.
Combines production and biomass computation in a single temporal loop.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import xarray as xr

from seapopym.core import kernel, template
from seapopym.function.compiled_functions import beverton_holt as beverton_holt_compiled
from seapopym.standard.attributs import biomass_desc
from seapopym.standard.labels import ConfigurationLabels, CoordinatesLabels, ForcingLabels

if TYPE_CHECKING:
    from collections.abc import Iterable

    from seapopym.standard.types import SeapopymDims, SeapopymForcing, SeapopymState

BIOMASS_DIMS = [CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X]


def _beverton_holt_helper_init_forcing(fgroup_data: xr.Dataset, state: SeapopymState) -> dict[str, np.ndarray]:
    """Initialize the forcing data used in the Numba function that computes biomass with Beverton-Holt."""

    def standardize_forcing(forcing: xr.DataArray, nan: object = 0.0, dtype: type = np.float64) -> np.ndarray:
        """Refer to Numba documentation about array typing."""
        return np.nan_to_num(x=forcing.data, nan=nan).astype(dtype)

    # Extract initial conditions if present
    if ConfigurationLabels.initial_condition_biomass not in fgroup_data:
        initial_condition_biomass = None
    else:
        initial_condition_biomass = standardize_forcing(fgroup_data[ConfigurationLabels.initial_condition_biomass])

    if ConfigurationLabels.initial_condition_production not in fgroup_data:
        initial_condition_recruitment = None
    else:
        initial_condition_recruitment = standardize_forcing(
            fgroup_data[ConfigurationLabels.initial_condition_production]
        )

    # Extract density dependence parameter (scalar per functional group)
    density_dependance_parameter_a = float(fgroup_data[ConfigurationLabels.density_dependance_parameter_a].data)
    density_dependance_parameter_b = float(fgroup_data[ConfigurationLabels.density_dependance_parameter_b].data)

    return {  # NOTE: the keys correspond to the parameters of the numba function
        "mortality": standardize_forcing(fgroup_data[ForcingLabels.mortality_field]),
        "primary_production": standardize_forcing(fgroup_data[ForcingLabels.primary_production_by_fgroup]),
        "mask_temperature": standardize_forcing(fgroup_data[ForcingLabels.mask_temperature]),
        "timestep_number": standardize_forcing(fgroup_data[ConfigurationLabels.timesteps_number]),
        "delta_time": int(state[ConfigurationLabels.timestep].data),
        "density_dependance_parameter_a": density_dependance_parameter_a,
        "density_dependance_parameter_b": density_dependance_parameter_b,
        "initial_conditions_biomass": initial_condition_biomass,
        "initial_conditions_recruitment": initial_condition_recruitment,
    }


def _beverton_holt_helper_format_output(
    fgroup_data: SeapopymState, dims: Iterable[SeapopymDims], data: np.ndarray
) -> SeapopymForcing:
    """Convert the output of the Numba function to a DataArray."""
    coords = {fgroup_data[dim_name].name: fgroup_data[dim_name] for dim_name in dims}
    formated_data = xr.DataArray(coords=coords, dims=coords.keys())
    formated_data = CoordinatesLabels.order_data(formated_data)
    formated_data.data = data
    return formated_data


def biomass_beverton_holt(state: SeapopymState) -> xr.Dataset:
    """Compute biomass using Beverton-Holt stock-recruitment with a numba jit function."""
    state = state.transpose(*CoordinatesLabels.ordered(), missing_dims="ignore")
    results_biomass = []

    for fgroup in state[CoordinatesLabels.functional_group]:
        fgroup_data = state.sel({CoordinatesLabels.functional_group: fgroup})
        param = _beverton_holt_helper_init_forcing(fgroup_data, state)
        output_biomass = beverton_holt_compiled.biomass_beverton_holt(**param)
        results_biomass.append(_beverton_holt_helper_format_output(fgroup_data, BIOMASS_DIMS, output_biomass))

    results = {ForcingLabels.biomass: xr.concat(results_biomass, dim=state[CoordinatesLabels.functional_group])}
    return xr.Dataset(results)


def _beverton_holt_survival_helper_init_forcing(fgroup_data: xr.Dataset, state: SeapopymState) -> dict[str, np.ndarray]:
    """Initialize the forcing data for Beverton-Holt with survival rate."""

    def standardize_forcing(forcing: xr.DataArray, nan: object = 0.0, dtype: type = np.float64) -> np.ndarray:
        """Refer to Numba documentation about array typing."""
        return np.nan_to_num(x=forcing.data, nan=nan).astype(dtype)

    # Extract initial conditions if present
    if ConfigurationLabels.initial_condition_biomass not in fgroup_data:
        initial_condition_biomass = None
    else:
        initial_condition_biomass = standardize_forcing(fgroup_data[ConfigurationLabels.initial_condition_biomass])

    if ConfigurationLabels.initial_condition_production not in fgroup_data:
        initial_condition_recruitment = None
    else:
        initial_condition_recruitment = standardize_forcing(
            fgroup_data[ConfigurationLabels.initial_condition_production]
        )

    # Extract density dependence parameter (scalar per functional group)
    density_dependance_parameter_a = float(fgroup_data[ConfigurationLabels.density_dependance_parameter_a].data)
    density_dependance_parameter_b = float(fgroup_data[ConfigurationLabels.density_dependance_parameter_b].data)

    return {  # NOTE: the keys correspond to the parameters of the numba function
        "mortality": standardize_forcing(fgroup_data[ForcingLabels.mortality_field]),
        "survival_rate": standardize_forcing(fgroup_data[ForcingLabels.survival_rate]),
        "primary_production": standardize_forcing(fgroup_data[ForcingLabels.primary_production_by_fgroup]),
        "mask_temperature": standardize_forcing(fgroup_data[ForcingLabels.mask_temperature]),
        "timestep_number": standardize_forcing(fgroup_data[ConfigurationLabels.timesteps_number]),
        "delta_time": int(state[ConfigurationLabels.timestep].data),
        "density_dependance_parameter_a": density_dependance_parameter_a,
        "density_dependance_parameter_b": density_dependance_parameter_b,
        "initial_conditions_biomass": initial_condition_biomass,
        "initial_conditions_recruitment": initial_condition_recruitment,
    }


def biomass_beverton_holt_survival(state: SeapopymState) -> xr.Dataset:
    """Compute biomass using Beverton-Holt stock-recruitment with survival rate adjustment."""
    state = state.transpose(*CoordinatesLabels.ordered(), missing_dims="ignore")
    results_biomass = []

    for fgroup in state[CoordinatesLabels.functional_group]:
        fgroup_data = state.sel({CoordinatesLabels.functional_group: fgroup})
        param = _beverton_holt_survival_helper_init_forcing(fgroup_data, state)
        output_biomass = beverton_holt_compiled.biomass_beverton_holt_with_survival_rate(**param)
        results_biomass.append(_beverton_holt_helper_format_output(fgroup_data, BIOMASS_DIMS, output_biomass))

    results = {ForcingLabels.biomass: xr.concat(results_biomass, dim=state[CoordinatesLabels.functional_group])}
    return xr.Dataset(results)


BiomassTemplate = template.template_unit_factory(
    name=ForcingLabels.biomass,
    attributs=biomass_desc,
    dims=[CoordinatesLabels.functional_group, *BIOMASS_DIMS],
)


BiomassBeverttonHoltKernel = kernel.kernel_unit_factory(
    name="biomass_beverton_holt", template=[BiomassTemplate], function=biomass_beverton_holt
)

BiomassBeverttonHoltKernelLight = kernel.kernel_unit_factory(
    name="biomass_beverton_holt_light",
    template=[BiomassTemplate],
    function=biomass_beverton_holt,
    to_remove_from_state=[ForcingLabels.mortality_field, ForcingLabels.mask_temperature],
)

BiomassBeverttonHoltSurvivalKernel = kernel.kernel_unit_factory(
    name="biomass_beverton_holt_survival", template=[BiomassTemplate], function=biomass_beverton_holt_survival
)

BiomassBeverttonHoltSurvivalKernelLight = kernel.kernel_unit_factory(
    name="biomass_beverton_holt_survival_light",
    template=[BiomassTemplate],
    function=biomass_beverton_holt_survival,
    to_remove_from_state=[ForcingLabels.mortality_field, ForcingLabels.mask_temperature, ForcingLabels.survival_rate],
)
