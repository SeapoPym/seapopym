# Notebooks

This directory contains Jupyter notebooks that are included in the documentation.

## Usage

Notebooks placed here are automatically rendered by MkDocs when referenced in the documentation.

### Adding a Notebook to Documentation

1. Place your `.ipynb` file in this directory
2. Reference it in a markdown file:

```markdown
See the complete example: [Basic Model](notebooks/basic_example.ipynb)
```

3. Or add directly to navigation in `mkdocs.yml`:

```yaml
nav:
  - Examples:
      - Basic Example: notebooks/basic_example.ipynb
```

## Tips

- Clear all outputs before committing (`Cell → All Output → Clear`)
- Keep notebooks focused and concise
- Add markdown cells with explanations
- Include visualizations for clarity
