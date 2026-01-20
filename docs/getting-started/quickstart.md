# Quick Start

This guide will help you run your first SeapoPym No-Transport model.

## Basic Workflow

The typical workflow with SeapoPym:

1. **Prepare forcing data** (temperature, primary production)
2. **Configure the model** (forcing parameters, functional groups)
3. **Run the simulation**
4. **Analyze results**

## Minimal Example

```python
import xarray as xr
from seapopym.model import NoTransportModel
from seapopym.configuration.no_transport import (
    NoTransportConfiguration,
    ForcingParameter,
    ForcingUnit,
    FunctionalGroupParameter,
    FunctionalGroupUnit,
    FunctionalTypeParameter,
    MigratoryTypeParameter,
)

# 1. Load forcing data
forcing_data = xr.open_dataset('forcing.nc')

# 2. Configure forcing
forcing = ForcingParameter(
    temperature=ForcingUnit(forcing=forcing_data['temperature']),
    primary_production=ForcingUnit(forcing=forcing_data['pp']),
)

# 3. Define functional groups
functional_groups = FunctionalGroupParameter(
    functional_group=[
        FunctionalGroupUnit(
            name="zooplankton",
            energy_transfert=0.1668,
            migratory_type=MigratoryTypeParameter(day_layer=0, night_layer=0),
            functional_type=FunctionalTypeParameter(
                lambda_temperature_0=1/150,
                gamma_lambda_temperature=0.15,
                tr_0=10.38,
                gamma_tr=-0.11,
            ),
        ),
    ]
)

# 4. Create configuration
config = NoTransportConfiguration(
    forcing=forcing,
    functional_group=functional_groups,
)

# 5. Run model with context manager
with NoTransportModel.from_configuration(configuration=config) as model:
    model.run()
    # Extract results (copy for use outside context)
    biomass = model.state['biomass'].copy()

# 6. Analyze
print(biomass)
biomass.mean(['Y', 'X']).plot(x='T')
```

## Understanding the Configuration

### Functional Groups

Functional groups represent different biological components of the ecosystem (e.g., zooplankton, micronekton). Each functional group is defined by:

- **Energy transfer** (`energy_transfert`): Efficiency of energy transfer from primary production (typical values: 0.1-0.2)
- **Migratory behavior** (`migratory_type`): Vertical migration pattern defined by day and night depth layers
- **Functional type** (`functional_type`): Temperature response parameters that control how the group responds to environmental conditions

```python
FunctionalGroupUnit(
    name="zooplankton",
    energy_transfert=0.1668,                    # Energy transfer efficiency
    migratory_type=MigratoryTypeParameter(
        day_layer=0,                             # Depth layer during day
        night_layer=0,                           # Depth layer during night
    ),
    functional_type=FunctionalTypeParameter(
        lambda_temperature_0=1/150,              # Base mortality rate
        gamma_lambda_temperature=0.15,           # Temperature effect on mortality
        tr_0=10.38,                              # Reference temperature for recruitment
        gamma_tr=-0.11,                          # Temperature sensitivity of recruitment
    ),
)
```

You can define multiple functional groups in a single simulation to represent different ecosystem components.

### Forcing Data

The No-Transport model requires two environmental forcing variables:

```python
forcing = ForcingParameter(
    temperature=ForcingUnit(forcing=temp_data),           # Sea temperature (°C)
    primary_production=ForcingUnit(forcing=pp_data),      # Primary production (g/m²/day or similar)
)
```

All forcing data must be `xarray.DataArray` with proper coordinates:

- **T**: Time coordinate
- **Y**: Latitude coordinate (can be single point for 1D models)
- **X**: Longitude coordinate (can be single point for 1D models)
- **Z**: Depth layer coordinate (for temperature)

## Understanding the Model

### Context Manager

The recommended way to run SeapoPym models is with a context manager. This ensures automatic memory cleanup after execution, which is especially important for repeated simulations:

```python
with NoTransportModel.from_configuration(configuration=config) as model:
    model.run()
    # Access results via model.state
    biomass = model.state['biomass'].copy()  # Important: copy() for use outside context
```

The `copy()` method is important when extracting data for use outside the context manager.

### Model State

After running the model, results are stored in `model.state` as an `xarray.Dataset` containing:

- **biomass**: Total biomass per functional group (dimensions: functional_group, T, Y, X)
- **recruited**: Recruited biomass (dimensions: functional_group, T, Y, X)
- **mortality_field**: Mortality rate field (dimensions: functional_group, T, Y, X)
- **primary_production_by_fgroup**: Primary production allocated to each functional group
- And many other diagnostic variables...

```python
# Access results
print(model.state)

# Extract specific variables
biomass = model.state['biomass']
mean_biomass = biomass.mean(dim=['Y', 'X'])  # Average over space
```

## Working with NetCDF Data

Most oceanographic data comes in NetCDF format. Here's how to load and prepare your data:

```python
import xarray as xr

# Load data
ds = xr.open_dataset('ocean_data.nc')

# Check contents
print(ds)

# Extract variables
temperature = ds['temp']
pp = ds['primary_production']

# Check coordinates match SeapoPym requirements (T, Y, X, Z)
print(temperature.coords)
```

## Visualizing Results

Plot your results using xarray's built-in plotting:

```python
import matplotlib.pyplot as plt

# Time series of spatially-averaged biomass
biomass.mean(dim=['Y', 'X']).plot(x='T', hue='functional_group')
plt.title('Mean Biomass Over Time')
plt.legend()
plt.show()

# Spatial distribution at one time step (for 2D/3D models)
biomass.isel(T=0, functional_group=0).plot()
plt.title('Biomass Spatial Distribution')
plt.show()
```

## Next Steps

- Explore complete [examples with notebooks](../examples/basic-example.md)
- Check the [API Reference](../api/seapopym.md)
