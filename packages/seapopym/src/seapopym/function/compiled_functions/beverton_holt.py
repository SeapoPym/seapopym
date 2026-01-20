"""This module contains the compiled (JIT) functions used by the stock-recrutment generator."""

from __future__ import annotations

import numpy as np
from numba import jit

from seapopym.function.compiled_functions.production_compiled_functions import ageing, expand_dims


@jit
def beverton_holt(
    biomass: np.ndarray, density_dependance_parameter_a: float, density_dependance_parameter_b: float
) -> np.ndarray:
    """
    Normalized Beverton-Holt function for spawning stock biomass.

    Returns a suitability coefficient between 0 and 1 that modulates primary production
    based on spawning stock biomass (SSB).

    Formula: f(SSB) = (b * SSB) / (1 + b * SSB)
    - f(0) = 0 (no spawners, no recruitment)
    - f(∞) → 1 (asymptotic maximum)
    - f(1/b) = 0.5 (inflection point)

    Parameters
    ----------
    biomass : np.ndarray
        Spawning stock biomass (SSB)
    density_dependance_parameter_a : float
        Density dependence parameter numerator(a)
    density_dependance_parameter_b : float
        Density dependence parameter denominator(b)

    Returns
    -------
    coefficient : np.ndarray
        Suitability coefficient between 0 and 1

    """
    return (density_dependance_parameter_a * biomass) / (1 + density_dependance_parameter_b * biomass)


@jit
def biomass_beverton_holt(
    mortality: np.ndarray,
    primary_production: np.ndarray,
    mask_temperature: np.ndarray,
    timestep_number: np.ndarray,
    delta_time: np.floating | np.integer,
    density_dependance_parameter_a: float,
    density_dependance_parameter_b: float,
    initial_conditions_biomass: np.ndarray | None = None,
    initial_conditions_recruitment: np.ndarray | None = None,
) -> np.ndarray:
    """
    Compute biomass using Beverton-Holt stock-recruitment with coupled production-biomass dynamics.

    Combines production recruitment (with cohort aging) and biomass integration in a single
    temporal loop due to the time-dependent coupling via the Beverton-Holt relationship.
    The stock-recruitment function modulates primary production based on current biomass,
    creating density-dependent recruitment dynamics.

    Parameters
    ----------
    mortality : np.ndarray
        Mortality rate for biomass loss.
        Shape: [time, lat, lon]. Single functional group.
    primary_production : np.ndarray
        Input primary production for each timestep.
        Shape: [time, lat, lon]. Shared across functional groups.
    mask_temperature : np.ndarray
        Recruitment mask determining when production can be recruited.
        Shape: [time, lat, lon, cohort]. True values allow recruitment.
    timestep_number : np.ndarray
        Number of timesteps each cohort spans.
        Shape: [cohort]. Controls aging rate between cohorts.
    delta_time : np.floating | np.integer
        Time step size for numerical integration.
    density_dependance_parameter_a : float
    density_dependance_parameter_b : float
        Beverton-Holt density dependence parameter (alpha).
        Stock-recruitment: R = a / (1 + b * B). Scalar per functional group.
    initial_conditions_biomass : np.ndarray | None, default=None
        Initial biomass state for t=0.
        Shape: [lat, lon]. If None, starts with zero biomass.
    initial_conditions_recruitment : np.ndarray | None, default=None
        Pre-existing production in cohorts from previous simulation.
        Shape: [lat, lon, cohort]. If None, starts with zero recruitment state.

    Returns
    -------
    biomass : np.ndarray
        Biomass evolution over time.
        Shape: [time, lat, lon]

    Notes
    -----
    - Production and biomass must be coupled in the same loop due to time-dependent Beverton-Holt
    - At each timestep: biomass(t-1) → Beverton-Holt coefficient → recruitment(t) → biomass(t)
    - Uses implicit Euler method for biomass integration: B(t) = (B(t-1) + dt*R(t)) / (1 + dt*λ(t))

    """
    # Initialize biomass array with temporal dimension
    biomass = np.zeros(mortality.shape)

    # Initial biomass for t=0 Beverton-Holt calculation
    if initial_conditions_biomass is not None:
        biomass_prev = initial_conditions_biomass
    else:
        biomass_prev = np.zeros(mortality[0, ...].shape, dtype=np.float64)

    # Initial pre-production state
    if initial_conditions_recruitment is not None:
        next_preproduction = initial_conditions_recruitment
    else:
        next_preproduction = np.zeros((*mortality[0, ...].shape, timestep_number.size), dtype=np.float64)

    for timestep in range(primary_production.shape[0]):
        # Apply Beverton-Holt to previous biomass
        beverton_holt_coefficient = beverton_holt(
            biomass_prev, density_dependance_parameter_a, density_dependance_parameter_b
        )

        # Production at age 0 with Beverton-Holt modulation
        # Broadcasting: (lat, lon) * (lat, lon) -> (lat, lon)
        production_age_0 = expand_dims(beverton_holt_coefficient * primary_production[timestep], timestep_number.size)
        pre_production = production_age_0 + next_preproduction

        # Age non-recruited production for next timestep
        if timestep < primary_production.shape[0] - 1:
            not_recruited = np.where(np.logical_not(mask_temperature[timestep]), pre_production, 0)
            next_preproduction = ageing(not_recruited, timestep_number)

        # Recruited production (sum over cohorts)
        recruited = np.sum(np.where(mask_temperature[timestep], pre_production, 0), axis=-1)

        # Euler implicit integration for biomass
        biomass[timestep, ...] = (biomass_prev + delta_time * recruited) / (1 + delta_time * mortality[timestep, ...])

        # Update previous biomass for next iteration
        biomass_prev = biomass[timestep, ...]

    return biomass


@jit
def biomass_beverton_holt_with_survival_rate(
    mortality: np.ndarray,
    survival_rate: np.ndarray,
    primary_production: np.ndarray,
    mask_temperature: np.ndarray,
    timestep_number: np.ndarray,
    delta_time: np.floating | np.integer,
    density_dependance_parameter_a: float,
    density_dependance_parameter_b: float,
    initial_conditions_biomass: np.ndarray | None = None,
    initial_conditions_recruitment: np.ndarray | None = None,
) -> np.ndarray:
    """
    Compute biomass using Beverton-Holt stock-recruitment with survival rate adjustment.

    Extends the basic Beverton-Holt implementation by applying a survival rate
    to the recruited biomass before integration. This accounts for mortality effects
    from ocean acidification and temperature using the Bednarsek equation.

    Parameters
    ----------
    mortality : np.ndarray
        Mortality rate for biomass loss.
        Shape: [time, lat, lon]. Single functional group.
    survival_rate : np.ndarray
        Survival rate coefficient from Bednarsek equation.
        Shape: [time, lat, lon]. Applied to recruited biomass.
    primary_production : np.ndarray
        Input primary production for each timestep.
        Shape: [time, lat, lon]. Shared across functional groups.
    mask_temperature : np.ndarray
        Recruitment mask determining when production can be recruited.
        Shape: [time, lat, lon, cohort]. True values allow recruitment.
    timestep_number : np.ndarray
        Number of timesteps each cohort spans.
        Shape: [cohort]. Controls aging rate between cohorts.
    delta_time : np.floating | np.integer
        Time step size for numerical integration.
    density_dependance_parameter_a : float
    density_dependance_parameter_b : float
        Beverton-Holt density dependence parameters.
        Stock-recruitment: R = a / (1 + b * B). Scalar per functional group.
    initial_conditions_biomass : np.ndarray | None, default=None
        Initial biomass state for t=0.
        Shape: [lat, lon]. If None, starts with zero biomass.
    initial_conditions_recruitment : np.ndarray | None, default=None
        Pre-existing production in cohorts from previous simulation.
        Shape: [lat, lon, cohort]. If None, starts with zero recruitment state.

    Returns
    -------
    biomass : np.ndarray
        Biomass evolution over time.
        Shape: [time, lat, lon]

    Notes
    -----
    - Survival rate is applied AFTER recruitment calculation but BEFORE biomass integration
    - Flow: biomass(t-1) → BH coefficient → recruitment → survival rate → biomass(t)
    - Uses implicit Euler method for biomass integration: B(t) = (B(t-1) + dt*R*S) / (1 + dt*λ(t))
      where S is the survival rate

    """
    # Initialize biomass array with temporal dimension
    biomass = np.zeros(mortality.shape)

    # Initial biomass for t=0 Beverton-Holt calculation
    if initial_conditions_biomass is not None:
        biomass_prev = initial_conditions_biomass
    else:
        biomass_prev = np.zeros(mortality[0, ...].shape, dtype=np.float64)

    # Initial pre-production state
    if initial_conditions_recruitment is not None:
        next_preproduction = initial_conditions_recruitment
    else:
        next_preproduction = np.zeros((*mortality[0, ...].shape, timestep_number.size), dtype=np.float64)

    for timestep in range(primary_production.shape[0]):
        # Apply Beverton-Holt to previous biomass
        beverton_holt_coefficient = beverton_holt(
            biomass_prev, density_dependance_parameter_a, density_dependance_parameter_b
        )

        # Production at age 0 with Beverton-Holt modulation
        production_age_0 = expand_dims(beverton_holt_coefficient * primary_production[timestep], timestep_number.size)
        pre_production = production_age_0 + next_preproduction

        # Age non-recruited production for next timestep
        if timestep < primary_production.shape[0] - 1:
            not_recruited = np.where(np.logical_not(mask_temperature[timestep]), pre_production, 0)
            next_preproduction = ageing(not_recruited, timestep_number)

        # Recruited production (sum over cohorts)
        recruited = np.sum(np.where(mask_temperature[timestep], pre_production, 0), axis=-1)

        # Apply survival rate to recruited biomass
        recruited_with_survival = recruited * survival_rate[timestep, ...]

        # Euler implicit integration for biomass with survival-adjusted recruitment
        biomass[timestep, ...] = (biomass_prev + delta_time * recruited_with_survival) / (
            1 + delta_time * mortality[timestep, ...]
        )

        # Update previous biomass for next iteration
        biomass_prev = biomass[timestep, ...]

    return biomass
