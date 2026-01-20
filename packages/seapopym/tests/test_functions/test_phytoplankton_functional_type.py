"""Tests for phytoplankton functional type (PFT) functions."""

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from seapopym.function.phytoplankton_functional_type import food_efficiency
from seapopym.standard.coordinates import new_latitude, new_longitude, new_time
from seapopym.standard.labels import ConfigurationLabels, CoordinatesLabels, ForcingLabels


@pytest.mark.scientific
class TestFoodEfficiency:
    """Test class for food efficiency calculations."""

    def test_food_efficiency_basic(self):
        """Test basic food efficiency calculation."""
        # Create simple inputs
        n_time = 3
        n_lat = 4
        n_lon = 5
        n_fgroup = 2

        # Create coordinates
        time = new_time(pd.date_range(start="2020-01-01", periods=n_time, freq="D"))
        lat = new_latitude(np.linspace(-10, 10, n_lat))
        lon = new_longitude(np.linspace(140, 160, n_lon))
        fgroup = xr.DataArray([0, 1], dims=[CoordinatesLabels.functional_group])

        # Create weights (different preferences for each functional group)
        w_pico = xr.DataArray(
            [0.5, 0.2],  # fgroup 0 prefers pico, fgroup 1 less so
            dims=[CoordinatesLabels.functional_group],
            coords={CoordinatesLabels.functional_group: fgroup},
        )
        w_nano = xr.DataArray(
            [0.3, 0.3],
            dims=[CoordinatesLabels.functional_group],
            coords={CoordinatesLabels.functional_group: fgroup},
        )
        w_micro = xr.DataArray(
            [0.2, 0.5],  # fgroup 1 prefers micro
            dims=[CoordinatesLabels.functional_group],
            coords={CoordinatesLabels.functional_group: fgroup},
        )

        # Create chlorophyll concentrations
        chlorophyll_pico = xr.DataArray(
            np.full((n_time, n_lat, n_lon), 1.0),
            dims=[CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
            coords={CoordinatesLabels.time: time, CoordinatesLabels.Y: lat, CoordinatesLabels.X: lon},
        )
        chlorophyll_nano = xr.DataArray(
            np.full((n_time, n_lat, n_lon), 2.0),
            dims=[CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
            coords={CoordinatesLabels.time: time, CoordinatesLabels.Y: lat, CoordinatesLabels.X: lon},
        )
        chlorophyll_micro = xr.DataArray(
            np.full((n_time, n_lat, n_lon), 0.5),
            dims=[CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
            coords={CoordinatesLabels.time: time, CoordinatesLabels.Y: lat, CoordinatesLabels.X: lon},
        )

        # Saturation constant
        ks = xr.DataArray(
            [1.0, 1.0],
            dims=[CoordinatesLabels.functional_group],
            coords={CoordinatesLabels.functional_group: fgroup},
        )

        # Create state
        state = xr.Dataset(
            {
                ConfigurationLabels.w_pico: w_pico,
                ConfigurationLabels.w_nano: w_nano,
                ConfigurationLabels.w_micro: w_micro,
                ForcingLabels.chlorophyll_pico: chlorophyll_pico,
                ForcingLabels.chlorophyll_nano: chlorophyll_nano,
                ForcingLabels.chlorophyll_micro: chlorophyll_micro,
                ConfigurationLabels.ks: ks,
            }
        )

        # Compute food efficiency
        result = food_efficiency(state)

        # Check output structure
        assert ForcingLabels.food_efficiency in result
        food_eff = result[ForcingLabels.food_efficiency]
        assert food_eff.dims == (
            CoordinatesLabels.functional_group,
            CoordinatesLabels.time,
            CoordinatesLabels.Y,
            CoordinatesLabels.X,
        )

        # Check output shape
        assert food_eff.shape == (n_fgroup, n_time, n_lat, n_lon)

        # Food efficiency should be between 0 and 1
        assert np.all(food_eff >= 0)
        assert np.all(food_eff <= 1)

        # Check that values are non-zero (with non-zero chlorophyll and weights)
        assert np.all(food_eff > 0)

    def test_food_efficiency_saturation(self):
        """Test that food efficiency saturates at high chlorophyll concentrations."""
        n_time = 2
        n_lat = 3
        n_lon = 3
        n_fgroup = 1

        # Create coordinates
        time = new_time(pd.date_range(start="2020-01-01", periods=n_time, freq="D"))
        lat = new_latitude(np.linspace(-5, 5, n_lat))
        lon = new_longitude(np.linspace(145, 155, n_lon))
        fgroup = xr.DataArray([0], dims=[CoordinatesLabels.functional_group])

        # Equal weights
        w_pico = xr.DataArray([1.0], dims=[CoordinatesLabels.functional_group], coords={CoordinatesLabels.functional_group: fgroup})
        w_nano = xr.DataArray([0.0], dims=[CoordinatesLabels.functional_group], coords={CoordinatesLabels.functional_group: fgroup})
        w_micro = xr.DataArray([0.0], dims=[CoordinatesLabels.functional_group], coords={CoordinatesLabels.functional_group: fgroup})

        # Very high chlorophyll concentration
        chlorophyll_pico = xr.DataArray(
            np.full((n_time, n_lat, n_lon), 100.0),  # Very high
            dims=[CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
            coords={CoordinatesLabels.time: time, CoordinatesLabels.Y: lat, CoordinatesLabels.X: lon},
        )
        chlorophyll_nano = xr.DataArray(
            np.zeros((n_time, n_lat, n_lon)),
            dims=[CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
            coords={CoordinatesLabels.time: time, CoordinatesLabels.Y: lat, CoordinatesLabels.X: lon},
        )
        chlorophyll_micro = xr.DataArray(
            np.zeros((n_time, n_lat, n_lon)),
            dims=[CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
            coords={CoordinatesLabels.time: time, CoordinatesLabels.Y: lat, CoordinatesLabels.X: lon},
        )

        ks = xr.DataArray([1.0], dims=[CoordinatesLabels.functional_group], coords={CoordinatesLabels.functional_group: fgroup})

        state = xr.Dataset(
            {
                ConfigurationLabels.w_pico: w_pico,
                ConfigurationLabels.w_nano: w_nano,
                ConfigurationLabels.w_micro: w_micro,
                ForcingLabels.chlorophyll_pico: chlorophyll_pico,
                ForcingLabels.chlorophyll_nano: chlorophyll_nano,
                ForcingLabels.chlorophyll_micro: chlorophyll_micro,
                ConfigurationLabels.ks: ks,
            }
        )

        result = food_efficiency(state)
        food_eff = result[ForcingLabels.food_efficiency]

        # With very high concentration, food efficiency should approach 1
        # weighted_phyto = 1.0 * 100.0 = 100.0
        # food_eff = 100.0 / (1.0 + 100.0) ≈ 0.99
        assert np.all(food_eff > 0.98)
        assert np.all(food_eff < 1.0)

    def test_food_efficiency_half_saturation(self):
        """Test that food efficiency is 0.5 at ks concentration."""
        n_time = 1
        n_lat = 2
        n_lon = 2
        n_fgroup = 1

        # Create coordinates
        time = new_time(pd.date_range(start="2020-01-01", periods=n_time, freq="D"))
        lat = new_latitude(np.linspace(-5, 5, n_lat))
        lon = new_longitude(np.linspace(145, 155, n_lon))
        fgroup = xr.DataArray([0], dims=[CoordinatesLabels.functional_group])

        w_pico = xr.DataArray([1.0], dims=[CoordinatesLabels.functional_group], coords={CoordinatesLabels.functional_group: fgroup})
        w_nano = xr.DataArray([0.0], dims=[CoordinatesLabels.functional_group], coords={CoordinatesLabels.functional_group: fgroup})
        w_micro = xr.DataArray([0.0], dims=[CoordinatesLabels.functional_group], coords={CoordinatesLabels.functional_group: fgroup})

        # Set chlorophyll concentration equal to ks
        ks_value = 2.0
        chlorophyll_pico = xr.DataArray(
            np.full((n_time, n_lat, n_lon), ks_value),
            dims=[CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
            coords={CoordinatesLabels.time: time, CoordinatesLabels.Y: lat, CoordinatesLabels.X: lon},
        )
        chlorophyll_nano = xr.DataArray(
            np.zeros((n_time, n_lat, n_lon)),
            dims=[CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
            coords={CoordinatesLabels.time: time, CoordinatesLabels.Y: lat, CoordinatesLabels.X: lon},
        )
        chlorophyll_micro = xr.DataArray(
            np.zeros((n_time, n_lat, n_lon)),
            dims=[CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
            coords={CoordinatesLabels.time: time, CoordinatesLabels.Y: lat, CoordinatesLabels.X: lon},
        )

        ks = xr.DataArray([ks_value], dims=[CoordinatesLabels.functional_group], coords={CoordinatesLabels.functional_group: fgroup})

        state = xr.Dataset(
            {
                ConfigurationLabels.w_pico: w_pico,
                ConfigurationLabels.w_nano: w_nano,
                ConfigurationLabels.w_micro: w_micro,
                ForcingLabels.chlorophyll_pico: chlorophyll_pico,
                ForcingLabels.chlorophyll_nano: chlorophyll_nano,
                ForcingLabels.chlorophyll_micro: chlorophyll_micro,
                ConfigurationLabels.ks: ks,
            }
        )

        result = food_efficiency(state)
        food_eff = result[ForcingLabels.food_efficiency]

        # At ks concentration, food efficiency should be 0.5
        # weighted_phyto = 1.0 * 2.0 = 2.0
        # food_eff = 2.0 / (2.0 + 2.0) = 0.5
        np.testing.assert_array_almost_equal(food_eff.values, 0.5)

    def test_food_efficiency_zero_chlorophyll(self):
        """Test that food efficiency is zero with no chlorophyll."""
        n_time = 1
        n_lat = 2
        n_lon = 2
        n_fgroup = 1

        # Create coordinates
        time = new_time(pd.date_range(start="2020-01-01", periods=n_time, freq="D"))
        lat = new_latitude(np.linspace(-5, 5, n_lat))
        lon = new_longitude(np.linspace(145, 155, n_lon))
        fgroup = xr.DataArray([0], dims=[CoordinatesLabels.functional_group])

        w_pico = xr.DataArray([1.0], dims=[CoordinatesLabels.functional_group], coords={CoordinatesLabels.functional_group: fgroup})
        w_nano = xr.DataArray([0.0], dims=[CoordinatesLabels.functional_group], coords={CoordinatesLabels.functional_group: fgroup})
        w_micro = xr.DataArray([0.0], dims=[CoordinatesLabels.functional_group], coords={CoordinatesLabels.functional_group: fgroup})

        # Zero chlorophyll
        chlorophyll_pico = xr.DataArray(
            np.zeros((n_time, n_lat, n_lon)),
            dims=[CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
            coords={CoordinatesLabels.time: time, CoordinatesLabels.Y: lat, CoordinatesLabels.X: lon},
        )
        chlorophyll_nano = xr.DataArray(
            np.zeros((n_time, n_lat, n_lon)),
            dims=[CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
            coords={CoordinatesLabels.time: time, CoordinatesLabels.Y: lat, CoordinatesLabels.X: lon},
        )
        chlorophyll_micro = xr.DataArray(
            np.zeros((n_time, n_lat, n_lon)),
            dims=[CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
            coords={CoordinatesLabels.time: time, CoordinatesLabels.Y: lat, CoordinatesLabels.X: lon},
        )

        ks = xr.DataArray([1.0], dims=[CoordinatesLabels.functional_group], coords={CoordinatesLabels.functional_group: fgroup})

        state = xr.Dataset(
            {
                ConfigurationLabels.w_pico: w_pico,
                ConfigurationLabels.w_nano: w_nano,
                ConfigurationLabels.w_micro: w_micro,
                ForcingLabels.chlorophyll_pico: chlorophyll_pico,
                ForcingLabels.chlorophyll_nano: chlorophyll_nano,
                ForcingLabels.chlorophyll_micro: chlorophyll_micro,
                ConfigurationLabels.ks: ks,
            }
        )

        result = food_efficiency(state)
        food_eff = result[ForcingLabels.food_efficiency]

        # With no chlorophyll, food efficiency should be zero
        np.testing.assert_array_almost_equal(food_eff.values, 0.0)

    def test_food_efficiency_different_functional_groups(self):
        """Test that different functional groups have different food efficiencies."""
        n_time = 1
        n_lat = 2
        n_lon = 2
        n_fgroup = 2

        # Create coordinates
        time = new_time(pd.date_range(start="2020-01-01", periods=n_time, freq="D"))
        lat = new_latitude(np.linspace(-5, 5, n_lat))
        lon = new_longitude(np.linspace(145, 155, n_lon))
        fgroup = xr.DataArray([0, 1], dims=[CoordinatesLabels.functional_group])

        # Different weights for each functional group
        w_pico = xr.DataArray([1.0, 0.0], dims=[CoordinatesLabels.functional_group], coords={CoordinatesLabels.functional_group: fgroup})
        w_nano = xr.DataArray([0.0, 0.0], dims=[CoordinatesLabels.functional_group], coords={CoordinatesLabels.functional_group: fgroup})
        w_micro = xr.DataArray([0.0, 1.0], dims=[CoordinatesLabels.functional_group], coords={CoordinatesLabels.functional_group: fgroup})

        # Different chlorophyll concentrations
        chlorophyll_pico = xr.DataArray(
            np.full((n_time, n_lat, n_lon), 2.0),
            dims=[CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
            coords={CoordinatesLabels.time: time, CoordinatesLabels.Y: lat, CoordinatesLabels.X: lon},
        )
        chlorophyll_nano = xr.DataArray(
            np.full((n_time, n_lat, n_lon), 1.0),
            dims=[CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
            coords={CoordinatesLabels.time: time, CoordinatesLabels.Y: lat, CoordinatesLabels.X: lon},
        )
        chlorophyll_micro = xr.DataArray(
            np.full((n_time, n_lat, n_lon), 0.5),
            dims=[CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
            coords={CoordinatesLabels.time: time, CoordinatesLabels.Y: lat, CoordinatesLabels.X: lon},
        )

        ks = xr.DataArray([1.0, 1.0], dims=[CoordinatesLabels.functional_group], coords={CoordinatesLabels.functional_group: fgroup})

        state = xr.Dataset(
            {
                ConfigurationLabels.w_pico: w_pico,
                ConfigurationLabels.w_nano: w_nano,
                ConfigurationLabels.w_micro: w_micro,
                ForcingLabels.chlorophyll_pico: chlorophyll_pico,
                ForcingLabels.chlorophyll_nano: chlorophyll_nano,
                ForcingLabels.chlorophyll_micro: chlorophyll_micro,
                ConfigurationLabels.ks: ks,
            }
        )

        result = food_efficiency(state)
        food_eff = result[ForcingLabels.food_efficiency]

        # fgroup 0: weighted_phyto = 1.0 * 2.0 = 2.0, food_eff = 2.0 / 3.0 ≈ 0.667
        # fgroup 1: weighted_phyto = 1.0 * 0.5 = 0.5, food_eff = 0.5 / 1.5 ≈ 0.333
        food_eff_fgroup0 = food_eff.sel({CoordinatesLabels.functional_group: 0})
        food_eff_fgroup1 = food_eff.sel({CoordinatesLabels.functional_group: 1})

        # fgroup 0 should have higher food efficiency (prefers pico, which is abundant)
        assert np.all(food_eff_fgroup0 > food_eff_fgroup1)

        # Check approximate values
        np.testing.assert_array_almost_equal(food_eff_fgroup0.values, 2.0 / 3.0, decimal=5)
        np.testing.assert_array_almost_equal(food_eff_fgroup1.values, 0.5 / 1.5, decimal=5)
