# SeapoPym: Spatial Ecosystem And POPulation dYnamics Model

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Overview

SeapoPym is a spatial ecosystem and population dynamics model implemented in Python using Xarray and Numba for high-performance scientific computing.

This repository is the **production version** accompanying the Model Description Paper published in Geoscientific Model Development (GMD).

## Repository Structure

```
seapopym-organisation/
├── packages/
│   ├── seapopym/              # Core model (Xarray/Numba)
│   └── seapopym-optimization/ # Genetic algorithms and optimization
├── paper_workflow/            # Notebooks for article reproduction
└── pyproject.toml            # Workspace configuration
```

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/SeapoPym/seapopym.git
cd seapopym-organisation

# Install the workspace
uv sync
```

## Packages

### `seapopym` (Core)

The main package containing the spatial ecosystem model implementation.

### `seapopym-optimization`

Optimization tools including genetic algorithms for parameter calibration.

## License

This project is licensed under the GNU General Public License v3.0 or later (GPLv3+).
See [LICENSE](LICENSE) for details.

## Citation

If you use this software in your research, please cite:

```
J.V. Lehodey 2026, SeapoPym v0.1: Implementation of the SEAPODYM low and mid trophic levels in Python with a flexible optimisation framework
```

## Authors

- [J.V. Lehodey](https://github.com/Ash12H) - SPC, IRD, Mercator-Ocean

## Acknowledgments

[To be filled during migration]
