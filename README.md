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
@software{SeapoPym_v0_1,
  author       = {Lehodey, J.V.},
  title        = {SeapoPym v0.1: Implementation of the SEAPODYM low and mid trophic levels in Python},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.PENDING},
  url          = {https://github.com/Seapodym/seapopym}
}
```

## Authors

- [J.V. Lehodey](https://github.com/Ash12H) - SPC, IRD, Mercator-Ocean

## Acknowledgments

This research was performed at Mercator Ocean International and the Pacific Community (SPC).

Financial support was provided by the Pacific Community (SPC) through the Climate Science to Ensure Pacific Access Work Programme (CSEPTA). J.V. Lehodey is supported by a PhD grant from the SPC and employed by the Institut de Recherche pour le Développement (IRD).
