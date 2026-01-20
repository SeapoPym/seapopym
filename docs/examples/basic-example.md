# Examples Overview

This section contains working examples demonstrating how to use SeapoPym.

## Available Examples

### [1D Model Example](../notebooks/example_1d_model.ipynb)

A complete tutorial showing:

- **Data generation**: Creating synthetic forcing data (temperature, primary production)
- **Model configuration**: Setting up functional groups with proper parameters
- **Sequential execution**: Running the model with context manager
- **Parallel execution**: Using Dask for distributed computing
- **Time resolution**: Degrading to weekly timesteps
- **Visualization**: Plotting biomass evolution over time

[View the 1D Model Example →](../notebooks/example_1d_model.ipynb){ .md-button .md-button--primary }

### [Optimization Example](../notebooks/optimization_example.ipynb)

A comprehensive guide to the optimization module, demonstrating:

- **Synthetic Truth**: Generating a "ground truth" simulation with known parameters
- **Observation Generation**: Creating synthetic observations with added noise
- **Cost Function**: Defining a cost function to compare model output with observations
- **Genetic Algorithm**: Using the optimization framework to recover the original parameters
- **Calibration**: Visualizing the convergence and fit of the optimized parameters

[View the Optimization Example →](../notebooks/optimization_example.ipynb){ .md-button .md-button--primary }
