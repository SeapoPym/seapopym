"""This module contains the post-production function used to compute the biomass.

They are run after the production process.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import xarray as xr

from seapopym.core import kernel, template
from seapopym.function.compiled_functions.biomass_compiled_functions import (
    biomass_euler_explicite,
    biomass_euler_implicite,
)
from seapopym.standard.attributs import biomass_desc
from seapopym.standard.labels import ConfigurationLabels, CoordinatesLabels, ForcingLabels

if TYPE_CHECKING:
    from seapopym.standard.types import SeapopymForcing, SeapopymState


def biomass(state: SeapopymState) -> xr.Dataset:
    """Wrap the biomass computation around the Numba function.

    The time-integration scheme is selected by the ``biomass_solver`` kernel
    parameter (carried in the state): 'explicit' (fully explicit Euler, as in the
    GMD publication; conditionally stable, requires daily time steps) or 'implicit'
    (semi-implicit IMEX, unconditionally stable). Defaults to 'explicit' when the
    flag is absent, preserving the published behaviour.

    Parameters
    ----------
    state : SeapopymState
        The model state containing recruited biomass and mortality.

    Returns
    -------
    xr.Dataset
        Dataset containing the computed biomass.

    Notes
    -----
    The implicit scheme treats the stiff mortality sink at t+1 and is preferred for
    large time steps or stiff (warm, high-mortality) regimes to avoid instability.

    """

    def _format_fields(forcing: SeapopymForcing) -> SeapopymForcing:
        """Format the fields to be used in the biomass computation.

        Parameters
        ----------
        forcing : SeapopymForcing
            Input forcing data.

        Returns
        -------
        SeapopymForcing
            Formatted data as numpy array (float64, NaNs replaced by 0).

        """
        return np.nan_to_num(forcing.data, 0.0).astype(np.float64)

    state = CoordinatesLabels.order_data(state)
    recruited = _format_fields(state[ForcingLabels.recruited])
    mortality = _format_fields(state[ForcingLabels.mortality_field])
    delta_time = state["timestep"]
    if ConfigurationLabels.initial_condition_biomass in state:
        initial_conditions = _format_fields(state[ConfigurationLabels.initial_condition_biomass])
    else:
        initial_conditions = None
    solver_flag = state.get(ConfigurationLabels.biomass_solver, "explicit")
    solver_flag = solver_flag.item() if hasattr(solver_flag, "item") else solver_flag
    solver = biomass_euler_implicite if str(solver_flag) == "implicit" else biomass_euler_explicite
    biomass = solver(
        recruited=recruited, mortality=mortality, initial_conditions=initial_conditions, delta_time=int(delta_time)
    )
    biomass = xr.DataArray(
        dims=state[ForcingLabels.mortality_field].dims,
        coords=state[ForcingLabels.mortality_field].coords,
        data=biomass,
    )
    return xr.Dataset({ForcingLabels.biomass: biomass})


BiomassTemplate = template.template_unit_factory(
    name=ForcingLabels.biomass,
    attributs=biomass_desc,
    dims=[CoordinatesLabels.functional_group, CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
)


BiomassKernel = kernel.kernel_unit_factory(name="biomass", template=[BiomassTemplate], function=biomass)
"""Kernel to compute biomass."""

BiomassKernelLight = kernel.kernel_unit_factory(
    name="biomass_light",
    template=[BiomassTemplate],
    function=biomass,
    to_remove_from_state=[ForcingLabels.recruited, ForcingLabels.mortality_field],
)
"""Light Kernel for biomass (removes recruited and mortality field)."""
