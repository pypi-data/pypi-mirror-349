# CONTRIBUTING.md

# Contributing to Scientific Plot Scaler

Thank you for considering contributing to Scientific Plot Scaler! This tool was created by researchers, for researchers, and we welcome contributions from the scientific community.

## How to Contribute

### Reporting Issues

- Check existing issues first to avoid duplicates
- Use the issue template and provide detailed information
- Include your Python version, matplotlib version, and OS
- Provide a minimal example that reproduces the issue

### Suggesting Features

- Open an issue with the "enhancement" label
- Describe the use case and why it would be beneficial
- Consider if it fits the scope of the project (scientific plotting for LaTeX)

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Install development dependencies**: `pip install -e .[dev]`
4. **Make your changes**:
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed
   - Ensure all tests pass: `pytest tests/`

5. **Code Quality Checks**:
   ```bash
   # Format code
   black .
   
   # Check linting
   flake8 .
   
   # Type checking
   mypy plot_scaler.py
   
   # Run tests
   pytest tests/ -v --cov=plot_scaler
   ```

6. **Commit your changes**: 
   - Use clear, descriptive commit messages
   - Follow conventional commits format if possible
   - Example: `feat: add support for Nature journal format`

7. **Push to your fork**: `git push origin feature/amazing-feature`

8. **Create a Pull Request**:
   - Use the PR template
   - Link to any related issues
   - Describe what changes you made and why

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/scientific-plot-scaler.git
cd scientific-plot-scaler

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]

# Install pre-commit hooks (optional but recommended)
pre-commit install
```

## Code Style Guidelines

- **Python Style**: Follow PEP 8, enforced by `black` and `flake8`
- **Line Length**: Maximum 88 characters (black default)
- **Type Hints**: Use type hints for public functions
- **Docstrings**: Use Google-style docstrings
- **Imports**: Group imports (standard library, third-party, local)

### Example Function

```python
def calculate_figure_size(self, layout_type: str) -> Tuple[float, float]:
    """Calculate optimal figure size based on layout type.
    
    Args:
        layout_type: Type of layout ('single', 'double', 'subfigure')
        
    Returns:
        Tuple of (width, height) in inches
        
    Raises:
        ValueError: If layout_type is not supported
    """
    # Implementation here
    pass
```

## Testing Guidelines

- Write tests for all new functionality
- Aim for >90% code coverage
- Use pytest fixtures for common setup
- Test both success and error cases

### Test Structure

```python
def test_feature_name():
    """Test description explaining what is being tested."""
    # Arrange
    config = PlotConfig(layout_type="single")
    plotter = ScientificPlotter(config)
    
    # Act
    result = plotter.some_method()
    
    # Assert
    assert result == expected_value
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all public functions and classes
- Include examples in docstrings when helpful
- Update configuration documentation for new options

## Research Domain Expertise Welcome

We especially welcome contributions from researchers in:

- **Mechanical Engineering**: CFD, FEA, materials science plots
- **Biomedical Engineering**: Medical imaging, biomechanics
- **Physics**: Experimental data, theoretical plots
- **Mathematics**: Statistical plots, numerical analysis
- **Other Sciences**: Any field that uses scientific plotting

### Domain-Specific Contributions

If you work in a specific research field, consider contributing:

1. **Example scripts** for your field (like the AAA example)
2. **Configuration presets** for common journals in your field
3. **Specialized plot types** common in your discipline
4. **Color schemes** appropriate for your field (e.g., colorblind-friendly)

## Journal Format Contributions

We welcome configurations for specific journals:

```python
# Example: Add support for your field's top journal
configs/journal_name.json
```

Include:
- Column widths
- Font size requirements  
- Style preferences
- Any special requirements

## Community Guidelines

- Be respectful and inclusive
- Help other researchers solve plotting problems
- Share knowledge about publication requirements
- Provide constructive feedback on PRs

## Release Process

1. Version follows semantic versioning (MAJOR.MINOR.PATCH)
2. Update CHANGELOG.md
3. Tag releases: `git tag v1.2.0`
4. Releases are automated via GitHub Actions

## Questions?

- Open an issue for technical questions
- Join our discussions for general questions
- Email maintainers for sensitive issues

## Recognition

Contributors are acknowledged in:
- README.md contributors section
- Release notes
- Academic citations when applicable

Thank you for helping make scientific plotting better for everyone!