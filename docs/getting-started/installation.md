# Installation

SeapoPym uses [uv](https://github.com/astral-sh/uv) for dependency management and is structured as a monorepo workspace.

## Requirements

- Python 3.12
- uv package manager

## Installing uv

If you don't have uv installed, follow the official installation guide:

**[uv Installation Documentation →](https://docs.astral.sh/uv/getting-started/installation/)**

## Installing SeapoPym

### From Source (Recommended)

Clone the repository and install:

```bash
git clone https://github.com/SeapoPym/seapopym.git
cd seapopym
uv sync
```

This installs both `seapopym` and `seapopym-optimization` packages in editable mode.

### Installing Only Core Package

If you only need the core model:

```bash
uv pip install -e packages/seapopym
```

### Installing Both Packages

To install both core and optimization:

```bash
uv pip install -e packages/seapopym -e packages/seapopym-optimization
```

## Verifying Installation

Test that everything works:

```python
import seapopym
print(f"SeapoPym installed successfully!")
```

## Development Tools

For contributing or running tests:

```bash
uv sync --group dev
```

This installs pytest, ruff, mypy, and other development tools.

## Documentation

To build the documentation locally:

```bash
uv sync --group docs
```

## Next Steps

Once installed, check out the [Quick Start Guide](quickstart.md) to run your first model!
