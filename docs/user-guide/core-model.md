# No-Transport Model

The **No-Transport Model** is the simplest configuration of SeapoPym. It simulates local ecosystem dynamics without advection or diffusion.

## Model Overview

The No-Transport model simulates:

- Primary production uptake by functional groups
- Temperature-dependent metabolism
- Natural mortality
- Biomass dynamics over time

This model is ideal for:
- 1D vertical simulations
- Understanding fundamental processes
- Parameter sensitivity studies
- Educational purposes

## Model Equations

At each time step and location, the model computes:

### Biomass Change

```
dB/dt = Production - Mortality
```

Where:
- `B`: Biomass (mg C m⁻³)
- `Production`: Growth from primary production uptake
- `Mortality`: Natural and temperature-dependent losses

### Production

```
Production = PP × Energy_Transfer × Temperature_Effect × Day_Length_Effect
```

Where:
- `PP`: Primary production (mg C m⁻³ day⁻¹)
- `Energy_Transfer`: Trophic transfer efficiency (0-1)
- `Temperature_Effect`: Temperature dependence factor
- `Day_Length_Effect`: Light availability factor

### Mortality

```
Mortality = B × Mortality_Rate × Temperature_Effect
```

## Using the Model

### Basic Usage

```python
from seapopym.model import NoTransportModel
from seapopym.configuration.no_transport import Configuration

# Create configuration
config = Configuration(...)

# Instantiate model
model = NoTransportModel(config)

# Run simulation
results = model.run()
```

### Model Configuration

The model requires three main components:

#### 1. Forcing Data

Environmental drivers:

```python
from seapopym.configuration.no_transport import ForcingParameter

forcing = ForcingParameter(
    temperature=temp_array,       # °C
    primary_production=pp_array,  # mg C m⁻³ day⁻¹
    day_length=daylen_array,      # hours
)
```

#### 2. Functional Groups

Ecological components:

```python
from seapopym.configuration.no_transport import FunctionalGroupParameter

zooplankton = FunctionalGroupParameter(
    name="zooplankton",
    energy_transfer=0.15,          # 15% transfer efficiency
    mortality_rate=0.1,            # 0.1 day⁻¹
    temperature_sensitivity=0.05,  # Temperature response
    production_efficiency=0.6,     # Production efficiency
)
```

#### 3. Complete Configuration

```python
config = Configuration(
    forcing=forcing,
    functional_groups=[zooplankton],
    time_step=1.0,                # days
    start_date="2000-01-01",
    end_date="2000-12-31",
)
```

## Model Outputs

The model returns an `xarray.Dataset` with:

### Variables

- **biomass**: Biomass per functional group (mg C m⁻³)
- **production**: Production rate (mg C m⁻³ day⁻¹)
- **mortality**: Mortality rate (mg C m⁻³ day⁻¹)
- **recruitment**: Recruitment from production (mg C m⁻³ day⁻¹)

### Coordinates

- **time**: Time steps
- **functional_group**: Functional group names
- **lat**, **lon**: Spatial coordinates (if applicable)
- **depth**: Depth levels (if applicable)

### Accessing Results

```python
results = model.run()

# Get biomass
biomass = results['biomass']

# Select specific functional group
zoop_biomass = biomass.sel(functional_group='zooplankton')

# Time series at a location
time_series = zoop_biomass.sel(lat=30.0, lon=-120.0, method='nearest')
time_series.plot()

# Spatial average
spatial_mean = zoop_biomass.mean(dim=['lat', 'lon'])
spatial_mean.plot()
```

## Parameter Sensitivity

The model behavior is sensitive to key parameters:

### Energy Transfer

Controls growth efficiency:
- Higher values → more biomass production
- Typical range: 0.05 - 0.25

### Mortality Rate

Controls biomass loss:
- Higher values → lower equilibrium biomass
- Typical range: 0.01 - 0.5 day⁻¹

### Temperature Sensitivity

Controls metabolic response:
- Higher values → stronger temperature effects
- Typical range: 0.01 - 0.1

## Performance

### Numba Compilation

Core functions are JIT-compiled for speed:

```python
# First run compiles (takes longer)
results = model.run()

# Subsequent runs are fast
results2 = model.run()
```

### Dask Parallelization

For large spatial domains:

```python
from dask.distributed import Client

# Start Dask cluster
client = Client(n_workers=4)

# Load data with chunks
forcing_data = xr.open_dataset(
    'forcing.nc',
    chunks={'time': 12, 'lat': 90, 'lon': 180}
)

# Model automatically parallelizes
results = model.run()
```

## Advanced Usage

### Custom Time Stepping

```python
# Manual time stepping
model = NoTransportModel(config)

for t in range(n_timesteps):
    state = model.step(state, t)
    # Custom analysis at each step
```

### State Inspection

```python
def callback(state, time_index):
    """Called after each time step"""
    biomass = state['biomass']
    print(f"Time {time_index}: Max biomass = {biomass.max().values}")

model = NoTransportModel(config, callback=callback)
results = model.run()
```

## Validation

Always validate your model setup:

```python
from seapopym.configuration.validation import validate_configuration

# Raises informative errors if configuration is invalid
validate_configuration(config)
```

## Next Steps

- See [Configuration Guide](configuration.md) for detailed parameters
- Explore [Examples](../examples/basic-example.md) with real data
- Check [API Reference](../api/seapopym.md) for all options
