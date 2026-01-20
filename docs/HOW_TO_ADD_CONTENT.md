# How to Add Content to the Documentation

This guide explains how to add notebooks, scripts, and images to the SeapoPym documentation.

## Directory Structure

```
docs/
├── notebooks/        # Jupyter notebooks
├── scripts/          # Python scripts
├── images/           # Figures and images
└── *.md              # Markdown pages
```

## Adding Jupyter Notebooks

### 1. Create Your Notebook

Place your `.ipynb` file in `docs/notebooks/`:

```bash
# Example notebook structure
docs/notebooks/
└── basic_example.ipynb
```

### 2. Include in Documentation

**Option A: Link from Markdown**

```markdown
See the complete example: [Basic Model Tutorial](notebooks/basic_example.ipynb)
```

**Option B: Add to Navigation (mkdocs.yml)**

```yaml
nav:
  - Examples:
      - Basic Tutorial: notebooks/basic_example.ipynb  # Direct notebook
```

The notebook will be rendered as an interactive page with:
- Code cells with syntax highlighting
- Output cells (plots, tables, etc.)
- Markdown cells as formatted text

### 3. Best Practices

- Clear all outputs before committing: `Cell → All Output → Clear`
- Add markdown cells to explain each step
- Include visualizations
- Keep notebooks focused (one topic per notebook)

## Adding Python Scripts

### 1. Create Your Script

Place your `.py` file in `docs/scripts/`:

```bash
docs/scripts/
└── run_model.py
```

### 2. Include in Documentation

**Full Script Inclusion:**

````markdown
```python title="scripts/run_model.py"
--8<-- "docs/scripts/run_model.py"
```
````

**Partial Inclusion (specific lines):**

````markdown
```python title="scripts/run_model.py" hl_lines="3-5"
--8<-- "docs/scripts/run_model.py:10:30"
```
````

### 3. Example

**Script: `docs/scripts/run_basic_model.py`**

```python
"""
Basic SeapoPym model example.
"""
import xarray as xr
from seapopym.model import NoTransportModel

def main():
    # Load data
    forcing = xr.open_dataset('forcing.nc')

    # Configure model
    model = NoTransportModel(config)

    # Run
    results = model.run()
    print(results)

if __name__ == '__main__':
    main()
```

**In Documentation:**

````markdown
Here's a complete example:

```python title="scripts/run_basic_model.py"
--8<-- "docs/scripts/run_basic_model.py"
```

Run it with:

```bash
python docs/scripts/run_basic_model.py
```
````

## Adding Images and Figures

### 1. Add Your Image

Place images in `docs/images/`:

```bash
docs/images/
├── biomass_timeseries.png
├── model_schematic.svg
└── spatial_distribution.png
```

### 2. Include in Documentation

**Basic Image:**

```markdown
![Biomass time series](images/biomass_timeseries.png)
```

**Image with Caption:**

```markdown
<figure markdown>
  ![Model schematic](images/model_schematic.svg)
  <figcaption>Figure 1: Schematic representation of the No-Transport model</figcaption>
</figure>
```

**Image with Custom Size:**

```markdown
<img src="images/model_schematic.svg" alt="Model diagram" width="600"/>
```

### 3. Best Practices

- Use descriptive filenames: `biomass_comparison.png` not `fig1.png`
- Prefer vector formats (SVG) for diagrams and schematics
- Use PNG for plots and raster images
- Optimize file sizes (compress images before adding)
- Always include alt text for accessibility

## Inline Code Examples

For short snippets directly in markdown:

````markdown
```python
from seapopym.model import NoTransportModel

model = NoTransportModel(config)
results = model.run()
```
````

With title and line highlights:

````markdown
```python title="example.py" hl_lines="2-3"
from seapopym.model import NoTransportModel

model = NoTransportModel(config)
results = model.run()
```
````

## Live Preview

Preview your changes locally:

```bash
uv run mkdocs serve
# Open http://localhost:8000
```

The documentation auto-reloads when you save changes!

## Building the Documentation

Build the complete documentation:

```bash
uv run mkdocs build --strict
```

This generates a `site/` directory with the full HTML documentation.

## Tips

1. **Keep it simple**: Documentation should be easy to follow
2. **Test your examples**: Make sure code actually runs
3. **Use descriptive names**: For files, variables, and sections
4. **Add context**: Explain why, not just what
5. **Preview locally**: Always check before committing

## Getting Help

- MkDocs documentation: https://www.mkdocs.org/
- Material theme: https://squidfunk.github.io/mkdocs-material/
- mkdocs-jupyter: https://github.com/danielfrg/mkdocs-jupyter
