# Contributing

We welcome contributions to SeapoPym! This page explains how to contribute.

## Ways to Contribute

- 🐛 Report bugs and issues
- 💡 Suggest new features or improvements
- 📖 Improve documentation
- 🔬 Add examples or tutorials
- 💻 Submit code contributions

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your contribution
4. Make your changes
5. Submit a pull request

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR-USERNAME/seapopym.git
cd seapopym
git checkout -b feature/my-contribution

# Make changes
# ...

git add .
git commit -m "Description of changes"
git push origin feature/my-contribution
```

## Development Setup

Install development dependencies:

```bash
uv sync --group dev --group docs
```

This installs:
- Testing: pytest, pytest-cov
- Linting: ruff, mypy
- Documentation: mkdocs, mkdocs-material

## Code Style

We use `ruff` for linting and formatting:

```bash
# Format code
uv run ruff format .

# Check for issues
uv run ruff check .
```

## Running Tests

Before submitting, ensure tests pass:

```bash
# Run all tests
uv run pytest packages/seapopym/tests/

# With coverage
uv run pytest --cov=seapopym packages/seapopym/tests/
```

## Documentation

If you add features, please update documentation:

```bash
# Build docs locally
uv run mkdocs serve

# View at http://localhost:8000
```

## Pull Request Guidelines

A good pull request:

1. **Focuses on a single issue** - One feature or bug fix per PR
2. **Includes tests** - New features should have tests
3. **Updates documentation** - Document new features
4. **Follows code style** - Run ruff before submitting
5. **Has a clear description** - Explain what and why

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
How were these changes tested?

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code formatted with ruff
```

## Reporting Issues

When reporting bugs, please include:

- Python version and operating system
- SeapoPym version
- Minimal code to reproduce the issue
- Expected vs actual behavior
- Error messages (if any)

## Feature Requests

For feature requests, please describe:

- The problem you're trying to solve
- Your proposed solution
- Any alternatives you've considered
- How this benefits other users

## Code of Conduct

Be respectful and constructive. We aim to foster an open and welcoming environment for all contributors.

## Questions?

Not sure where to start? Open a discussion on GitHub or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under GPLv3+.
