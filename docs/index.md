# SeapoPym Documentation

Welcome to the SeapoPym documentation! SeapoPym is a Python implementation of the SEAPODYM (Spatial Ecosystem And POpulation DYnamics Model) focusing on low and mid trophic levels of marine ecosystems.

## Overview

SeapoPym provides a flexible framework for simulating spatial ecosystem dynamics using modern Python tools:

- **Modern Python stack**: Built with Xarray, Dask, and Numba for high-performance computing
- **High-performance computing**: Numba JIT compilation for efficient numerical computations
- **Parallel processing**: Dask support for large-scale simulations
- **CF-compliant data**: Xarray-based structures with pint-xarray for units
- **Scientific reproducibility**: Production-quality code accompanying our GMD publication

## The No-Transport Model

This documentation focuses on the **No-Transport Model**, which simulates local ecosystem dynamics without advection. This model is ideal for:

- Understanding fundamental ecosystem processes
- 1D vertical simulations
- Parameter sensitivity studies
- Learning the SeapoPym framework

[Get Started →](getting-started/installation.md){ .md-button .md-button--primary }

## Quick Example

```python
from seapopym.model import NoTransportModel

# Configure and run model
model = NoTransportModel(config)
results = model.run()

# Analyze results
biomass = results['biomass']
biomass.plot()
```

[Full Tutorial →](getting-started/quickstart.md){ .md-button .md-button--primary }

## Citation

If you use SeapoPym in your research, please cite:

```bibtex
@article{lehodey2026seapopym,
  title={SeapoPym v0.1: Implementation of the SEAPODYM low and mid trophic levels in Python with a flexible optimisation framework},
  author={Lehodey, J.V.},
  journal={Geoscientific Model Development},
  year={2026}
}
```

## License

SeapoPym is open-source software licensed under the GNU General Public License v3.0 or later (GPLv3+).

## Support

- 📚 [Documentation](https://seapopym.github.io/seapopym/)
- 💬 [GitHub Discussions](https://github.com/SeapoPym/seapopym/discussions)
- 🐛 [Issue Tracker](https://github.com/SeapoPym/seapopym/issues)
