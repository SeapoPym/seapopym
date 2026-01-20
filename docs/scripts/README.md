# Scripts

This directory contains Python scripts that are referenced in the documentation.

## Usage

Scripts here can be included in documentation pages using snippets:

### Full Script Inclusion

````markdown
```python title="scripts/run_model.py"
--8<-- "docs/scripts/run_model.py"
```
````

### Partial Inclusion with Line Numbers

````markdown
```python
--8<-- "docs/scripts/run_model.py:10:20"
```
````

## Guidelines

- Keep scripts self-contained and runnable
- Add docstrings and comments
- Include example usage in script docstrings
- Name scripts descriptively (e.g., `run_basic_model.py`)
