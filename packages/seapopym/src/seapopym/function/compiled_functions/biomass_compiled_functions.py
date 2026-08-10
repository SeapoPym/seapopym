"""This module contains the compiled (JIT) functions used by the biomass generator."""

from __future__ import annotations

import numpy as np
from numba import jit


@jit()
def biomass_euler_explicite(
    recruited: np.ndarray,
    mortality: np.ndarray,
    initial_conditions: np.ndarray | None,
    delta_time: np.floating | np.integer,
) -> np.ndarray:
    """Explicit Euler scheme for dB/dt = R - lambda*B.

    The mortality term is evaluated with the biomass of the previous step, which is
    what makes the scheme explicit.

    Discretization: B(n+1) = B(n) + dt*(R(n+1) - lambda(n+1)*B(n))

    WARNING: This scheme is conditionally stable and requires small time steps
    (dt < 2/lambda_max) to avoid numerical instability and negative biomass values.
    Use biomass_euler_implicite for large time steps or stiff mortality rates.

    Parameters
    ----------
    recruited : np.ndarray
        Recruited biomass [functional_group, time, Y, X].
    mortality : np.ndarray
        Mortality coefficient [functional_group, time, Y, X].
    initial_conditions : np.ndarray | None
        Initial biomass conditions [functional_group, Y, X]. If None, assumed 0.
    delta_time : float | int
        Time step size in days.

    Returns
    -------
    np.ndarray
        Computed biomass [functional_group, time, Y, X].

    Notes
    -----
    This scheme is NOT recommended for production use due to stability issues.
    Prefer biomass_euler_implicite which is unconditionally stable.

    """
    initial_conditions = (
        np.zeros(recruited[:, 0, ...].shape, dtype=np.float64) if initial_conditions is None else initial_conditions
    )
    biomass = np.zeros(recruited.shape)
    biomass[:, 0, ...] = (
        initial_conditions + delta_time * recruited[:, 0, ...] - delta_time * mortality[:, 0, ...] * initial_conditions
    )

    for timestep in range(1, recruited.shape[1]):
        biomass[:, timestep, ...] = (
            biomass[:, timestep - 1, ...]
            + delta_time * recruited[:, timestep, ...]
            - delta_time * mortality[:, timestep, ...] * biomass[:, timestep - 1, ...]
        )
    return biomass


@jit()
def biomass_euler_implicite(
    recruited: np.ndarray,
    mortality: np.ndarray,
    initial_conditions: np.ndarray | None,
    delta_time: np.floating | np.integer,
) -> np.ndarray:
    """Implicit (backward Euler) scheme for dB/dt = R - lambda*B.

    The right-hand side is evaluated at the new time step, so the mortality term uses
    the biomass being solved for. The update is linear in B and therefore inverts in
    closed form, with no iteration.

    Discretization: B(n+1) = (B(n) + dt*R(n+1)) / (1 + dt*lambda(n+1))

    This scheme is unconditionally stable (no timestep restriction) due to the
    implicit treatment of the mortality term, which is the stiff component. This is
    the scheme described in the model paper (Lehodey et al., GMD).

    Parameters
    ----------
    recruited : np.ndarray
        Recruited biomass [functional_group, time, Y, X].
    mortality : np.ndarray
        Mortality coefficient [functional_group, time, Y, X].
    initial_conditions : np.ndarray | None
        Initial biomass conditions [functional_group, Y, X]. If None, assumed 0.
    delta_time : float | int
        Time step size in days.

    Returns
    -------
    np.ndarray
        Computed biomass [functional_group, time, Y, X].

    Notes
    -----
    This scheme is preferred over explicit Euler (biomass_euler_explicite) for
    stability, especially with large time steps (e.g., weekly instead of daily).

    """
    initial_conditions = (
        np.zeros(recruited[:, 0, ...].shape, dtype=np.float64) if initial_conditions is None else initial_conditions
    )
    biomass = np.zeros(recruited.shape)
    biomass[:, 0, ...] = (initial_conditions + delta_time * recruited[:, 0, ...]) / (
        1 + delta_time * mortality[:, 0, ...]
    )

    for timestep in range(1, recruited.shape[1]):
        biomass[:, timestep, ...] = (biomass[:, timestep - 1, ...] + delta_time * recruited[:, timestep, ...]) / (
            1 + delta_time * mortality[:, timestep, ...]
        )
    return biomass
