"""Tests for Beverton-Holt stock-recruitment functions."""

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from seapopym.function.compiled_functions.beverton_holt import beverton_holt, biomass_beverton_holt
from seapopym.standard.coordinates import new_latitude, new_longitude, new_time


@pytest.mark.scientific
class TestBevertonHoltCompiled:
    """Test class for compiled Beverton-Holt functions."""

    def test_beverton_holt_basic(self):
        """Test basic Beverton-Holt function with scalar inputs."""
        biomass = np.array([[1.0, 2.0], [3.0, 4.0]])
        alpha = 0.5

        result = beverton_holt(biomass, alpha)

        # Expected: (alpha * biomass) / (1 + alpha * biomass)
        expected = (alpha * biomass) / (1 + alpha * biomass)

        np.testing.assert_array_almost_equal(result, expected)

    def test_beverton_holt_zero_biomass(self):
        """Test Beverton-Holt with zero biomass."""
        biomass = np.zeros((5, 5))
        alpha = 0.5

        result = beverton_holt(biomass, alpha)

        # With zero biomass, result should be zero
        np.testing.assert_array_equal(result, np.zeros((5, 5)))

    def test_beverton_holt_zero_alpha(self):
        """Test Beverton-Holt with zero density dependence."""
        biomass = np.array([[1.0, 2.0], [3.0, 4.0]])
        alpha = 0.0

        result = beverton_holt(biomass, alpha)

        # With alpha=0, result should be zero (no density dependence = no recruitment)
        np.testing.assert_array_almost_equal(result, np.zeros_like(biomass))

    def test_beverton_holt_high_alpha(self):
        """Test Beverton-Holt with strong density dependence."""
        biomass = np.array([[10.0, 20.0], [30.0, 40.0]])
        alpha = 10.0

        result = beverton_holt(biomass, alpha)

        # With high alpha and high biomass, coefficient should approach 1 (asymptote)
        # For large biomass: (alpha * B) / (1 + alpha * B) → 1
        assert np.all(result > 0.9)  # Should be close to 1
        assert np.all(result <= 1.0)  # But never exceed 1

        # At inflection point (biomass = 1/alpha), coefficient should be 0.5
        biomass_inflection = 1.0 / alpha
        result_inflection = beverton_holt(np.array([[biomass_inflection]]), alpha)
        np.testing.assert_almost_equal(result_inflection[0, 0], 0.5)

    def test_biomass_beverton_holt_basic(self):
        """Test basic biomass_beverton_holt function."""
        # Create simple inputs
        n_time = 5
        n_lat = 3
        n_lon = 3
        n_cohort = 2

        mortality = np.full((n_time, n_lat, n_lon), 0.1)
        primary_production = np.full((n_time, n_lat, n_lon), 1.0)
        mask_temperature = np.ones((n_time, n_lat, n_lon, n_cohort), dtype=bool)
        timestep_number = np.array([1.0, 1.0])
        delta_time = 1.0
        alpha = 0.1

        result = biomass_beverton_holt(
            mortality=mortality,
            primary_production=primary_production,
            mask_temperature=mask_temperature,
            timestep_number=timestep_number,
            delta_time=delta_time,
            density_dependance_parameter=alpha,
        )

        # Check output shape
        assert result.shape == (n_time, n_lat, n_lon)

        # Biomass should be non-negative
        assert np.all(result >= 0)

        # Biomass should increase over time with constant production
        assert np.all(result[1:, ...] >= result[:-1, ...])

    def test_biomass_beverton_holt_with_initial_conditions(self):
        """Test biomass_beverton_holt with initial conditions."""
        n_time = 3
        n_lat = 2
        n_lon = 2
        n_cohort = 2

        mortality = np.full((n_time, n_lat, n_lon), 0.1)
        primary_production = np.full((n_time, n_lat, n_lon), 1.0)
        mask_temperature = np.ones((n_time, n_lat, n_lon, n_cohort), dtype=bool)
        timestep_number = np.array([1.0, 1.0])
        delta_time = 1.0
        alpha = 0.1

        # Initial conditions
        initial_biomass = np.full((n_lat, n_lon), 5.0)
        initial_recruitment = np.full((n_lat, n_lon, n_cohort), 0.5)

        result = biomass_beverton_holt(
            mortality=mortality,
            primary_production=primary_production,
            mask_temperature=mask_temperature,
            timestep_number=timestep_number,
            delta_time=delta_time,
            density_dependance_parameter=alpha,
            initial_conditions_biomass=initial_biomass,
            initial_conditions_recruitment=initial_recruitment,
        )

        # Check that initial biomass affects the result
        assert result.shape == (n_time, n_lat, n_lon)
        # First timestep should be influenced by initial conditions
        assert np.all(result[0, ...] > 0)

    def test_biomass_beverton_holt_density_dependence_effect(self):
        """Test that density dependence parameter affects biomass growth."""
        n_time = 10
        n_lat = 2
        n_lon = 2
        n_cohort = 2

        mortality = np.full((n_time, n_lat, n_lon), 0.05)
        primary_production = np.full((n_time, n_lat, n_lon), 2.0)
        mask_temperature = np.ones((n_time, n_lat, n_lon, n_cohort), dtype=bool)
        timestep_number = np.array([2.0, 3.0])
        delta_time = 1.0

        # Need initial biomass to kickstart Beverton-Holt
        initial_biomass = np.full((n_lat, n_lon), 1.0)

        # Run with low density dependence (recruitment saturates slowly)
        result_low_dd = biomass_beverton_holt(
            mortality=mortality,
            primary_production=primary_production,
            mask_temperature=mask_temperature,
            timestep_number=timestep_number,
            delta_time=delta_time,
            density_dependance_parameter=0.1,
            initial_conditions_biomass=initial_biomass,
        )

        # Run with high density dependence (recruitment saturates quickly)
        result_high_dd = biomass_beverton_holt(
            mortality=mortality,
            primary_production=primary_production,
            mask_temperature=mask_temperature,
            timestep_number=timestep_number,
            delta_time=delta_time,
            density_dependance_parameter=1.0,
            initial_conditions_biomass=initial_biomass,
        )

        # Both should have positive biomass
        assert np.all(result_low_dd > 0)
        assert np.all(result_high_dd > 0)

        # With higher b parameter, BH coefficient reaches higher values at low-medium biomass
        # Formula: (b*SSB)/(1+b*SSB) - higher b means steeper initial growth
        # At moderate biomass levels, higher b gives higher coefficient and thus higher recruitment
        # Therefore, higher b leads to HIGHER final biomass (not lower!)
        assert np.all(result_high_dd[-1, ...] > result_low_dd[-1, ...])

    def test_biomass_beverton_holt_conservation_properties(self):
        """Test that biomass follows expected dynamics."""
        n_time = 5
        n_lat = 2
        n_lon = 2
        n_cohort = 2

        mortality = np.full((n_time, n_lat, n_lon), 0.2)
        primary_production = np.zeros((n_time, n_lat, n_lon))  # No input
        mask_temperature = np.ones((n_time, n_lat, n_lon, n_cohort), dtype=bool)
        timestep_number = np.array([1.0, 1.0])
        delta_time = 1.0
        alpha = 0.1

        # Initial biomass
        initial_biomass = np.full((n_lat, n_lon), 10.0)

        result = biomass_beverton_holt(
            mortality=mortality,
            primary_production=primary_production,
            mask_temperature=mask_temperature,
            timestep_number=timestep_number,
            delta_time=delta_time,
            density_dependance_parameter=alpha,
            initial_conditions_biomass=initial_biomass,
        )

        # With no production and positive mortality, biomass should decrease
        assert np.all(result[1:, ...] < result[:-1, ...])

        # Biomass should remain non-negative
        assert np.all(result >= 0)

    def test_biomass_beverton_holt_mask_effect(self):
        """Test that mask_temperature affects recruitment."""
        n_time = 5
        n_lat = 2
        n_lon = 2
        n_cohort = 2

        mortality = np.full((n_time, n_lat, n_lon), 0.1)
        primary_production = np.full((n_time, n_lat, n_lon), 1.0)
        timestep_number = np.array([2.0, 3.0])  # More realistic timestep numbers
        delta_time = 1.0
        alpha = 0.1

        # Need initial biomass to kickstart Beverton-Holt
        initial_biomass = np.full((n_lat, n_lon), 1.0)

        # Full recruitment
        mask_all = np.ones((n_time, n_lat, n_lon, n_cohort), dtype=bool)

        # No recruitment
        mask_none = np.zeros((n_time, n_lat, n_lon, n_cohort), dtype=bool)

        result_all = biomass_beverton_holt(
            mortality=mortality,
            primary_production=primary_production,
            mask_temperature=mask_all,
            timestep_number=timestep_number,
            delta_time=delta_time,
            density_dependance_parameter=alpha,
            initial_conditions_biomass=initial_biomass,
        )

        result_none = biomass_beverton_holt(
            mortality=mortality,
            primary_production=primary_production,
            mask_temperature=mask_none,
            timestep_number=timestep_number,
            delta_time=delta_time,
            density_dependance_parameter=alpha,
            initial_conditions_biomass=initial_biomass,
        )

        # With recruitment, biomass should be positive
        assert np.all(result_all > 0)

        # With recruitment, biomass should be higher
        assert np.all(result_all[-1, ...] > result_none[-1, ...])

        # Without recruitment, biomass should decay (only mortality, no recruitment)
        assert np.all(result_none[-1, ...] < initial_biomass)

    def test_biomass_beverton_holt_numerical_stability(self):
        """Test numerical stability with extreme values."""
        n_time = 3
        n_lat = 2
        n_lon = 2
        n_cohort = 2

        # Very low mortality
        mortality = np.full((n_time, n_lat, n_lon), 0.001)
        primary_production = np.full((n_time, n_lat, n_lon), 0.1)
        mask_temperature = np.ones((n_time, n_lat, n_lon, n_cohort), dtype=bool)
        timestep_number = np.array([1.0, 1.0])
        delta_time = 0.1
        alpha = 0.01

        result = biomass_beverton_holt(
            mortality=mortality,
            primary_production=primary_production,
            mask_temperature=mask_temperature,
            timestep_number=timestep_number,
            delta_time=delta_time,
            density_dependance_parameter=alpha,
        )

        # Should not produce NaN or Inf
        assert not np.any(np.isnan(result))
        assert not np.any(np.isinf(result))
        assert np.all(result >= 0)
