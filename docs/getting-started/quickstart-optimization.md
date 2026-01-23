# Quick Start (Optimization)

SeapoPym Optimization describes a workflow to estimate model parameters using Genetic Algorithms (DEAP). Ideally suited for fitting the `NoTransportModel` to observed data (such as biomass time series or spatial maps), this module separates parameter definition, observation handling, and the optimization engine for clarity and reproducibility.

## Optimization Workflow

The optimization process follows four main steps:

1.  **Prepare Observations**: Wrap your reference data (xarray DataArray) into `Observation` objects (e.g., `TimeSeriesObservation`).
2.  **Define Parameters**: Use `Parameter` objects within your `FunctionalGroup` to specify which values to optimize and their bounds.
3.  **Configure GA**: Set up the `CostFunction` and `GeneticAlgorithmParameters` (population size, generations, mutation rates).
4.  **Run & Analyze**: Instantiate the algorithm via `GeneticAlgorithmFactory` and run `.optimize()`.

## Minimal Example

This example demonstrates how to set up an optimization for a simplified case.

```python
import numpy as np
import xarray as xr
from seapopym_optimization.functional_group import (
    NoTransportFunctionalGroup,
    Parameter,
    FunctionalGroupSet
)
from seapopym_optimization.observations.time_serie import TimeSeriesObservation
from seapopym_optimization.cost_function.cost_function import CostFunction
from seapopym_optimization.algorithm.genetic_algorithm.genetic_algorithm import (
    GeneticAlgorithmParameters
)
from seapopym_optimization.algorithm.genetic_algorithm.factory import GeneticAlgorithmFactory

# --- 1. Prepare Observations ---
# Create fake observed data (e.g., biomass over time)
# Note: Real observations require specific coordinates (e.g., 'time', 'latitude', 'longitude').
obs_data = xr.DataArray(
    data=np.random.rand(100),
    coords={"time": np.arange(100)},
    dims="time",
    name="biomass"
)
# Wrap in an Observation object
obs = TimeSeriesObservation(name="obs_sample", observation=obs_data)

# --- 2. Define Parameters ---
# Define the Functional Group with some fixed values and some Parameters to optimize
f_group = NoTransportFunctionalGroup(
    day_layer=Parameter(value=1.5, min_value=0.0, max_value=3.0), # To optimize
    night_layer=1.0,                                              # Fixed
    energy_transfert=Parameter(value=0.1, min_value=0.01, max_value=0.5), # To optimize
    lambda_temperature_0=0.5,
    gamma_lambda_temperature=0.1,
    tr_0=0.1,
    gamma_tr=0.1,
    name="example_group"
)

# --- 3. Configure GA ---
# Define GA hyperparameters
ga_params = GeneticAlgorithmParameters(
    population_size=10,
    generations=5,
    mutation_probability=0.2,
    crossover_probability=0.5
)

# Note: In a real scenario, you also need:
# - 'forcing' (ForcingParameter containing Temperature/PP)
# - 'configuration_generator' (NoTransportConfigurationGenerator)
#
cost_function = CostFunction(
    configuration_generator=my_config_gen,
    functional_groups=FunctionalGroupSet([f_group]),
    forcing=my_forcing_param,
    kernel=None,
    observations=[obs],
    processor=TimeSeriesScoreProcessor(comparator=rmse_comparator)
)

# --- 4. Run Optimization ---
# Create the optimizer (Sequential for simple debugging, Parallel for speed)
ga = GeneticAlgorithmFactory.create_sequential(
    meta_parameter=ga_params,
    cost_function=cost_function
)

# Run
results = ga.optimize()
print(results) # The logbook containing statistics
```

For a fully working executable example including model and forcing generation, see the [Optimization Example](../notebooks/optimization_example.ipynb).

## Next Steps

- **[Optimization Example](../notebooks/optimization_example.ipynb)**: See a complete, executable example.
- **[API Reference](../api/seapopym-optimization.md)**: Explore the detailed API documentation for classes and functions.
