# Configuration

Model configuration in SeapoPym is handled through configuration classes that define parameters, forcing data, and model setup.

## Configuration Structure

Each model variant has its own configuration:

```python
from seapopym.configuration.no_transport import Configuration
from seapopym.configuration.acidity import Configuration as AcidityConfiguration
```

## Basic Configuration

```python
from seapopym.configuration.no_transport import (
    Configuration,
    ForcingParameter,
    FunctionalGroupParameter
)

config = Configuration(
    forcing=forcing_params,
    functional_groups=functional_group_params,
    time_step=1.0,  # days
    start_date="2000-01-01",
    end_date="2000-12-31"
)
```

## Forcing Parameters

Define environmental forcing data:

```python
forcing = ForcingParameter(
    temperature=temperature_ds,
    primary_production=pp_ds,
    day_length=daylen_ds,
)
```

## Functional Group Parameters

Define biological parameters for each functional group:

```python
fg_params = FunctionalGroupParameter(
    name="zooplankton",
    energy_transfer=0.15,
    mortality_rate=0.1,
    temperature_sensitivity=0.05,
    production_efficiency=0.6,
)
```

## Configuration Files

Save and load configurations:

```python
# Save to file
config.to_yaml('config.yaml')

# Load from file
config = Configuration.from_yaml('config.yaml')
```

## Validation

Configurations are automatically validated:

```python
from seapopym.configuration.validation import validate_configuration

# Raises error if invalid
validate_configuration(config)
```

For detailed parameter descriptions and examples, see the [API Reference](../api/seapopym.md).
