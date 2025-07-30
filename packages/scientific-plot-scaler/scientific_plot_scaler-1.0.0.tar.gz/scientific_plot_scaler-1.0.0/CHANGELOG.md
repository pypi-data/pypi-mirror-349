# CHANGELOG.md

# Changelog

All notable changes to Scientific Plot Scaler will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of Scientific Plot Scaler
- Support for single column, double column, and subfigure layouts
- Automatic text scaling based on figure dimensions
- Multiple output formats (PDF, PNG, EPS, SVG)
- Configuration system with JSON files
- Example configurations for common journals
- AAA growth prediction example for biomedical engineering
- Comprehensive test suite
- CI/CD pipeline with GitHub Actions

### Features
- **PlotConfig class**: Flexible configuration system
- **ScientificPlotter class**: Main plotting interface
- **Automatic font sizing**: Scales text appropriately for different layouts
- **LaTeX integration**: Optimized for LaTeX document inclusion
- **Publication quality**: High DPI output with proper formatting
- **Multiple styles**: Support for different matplotlib styles
- **Command line interface**: Easy batch processing

### Documentation
- Comprehensive README with examples
- Contributing guidelines
- Code documentation with type hints
- Example scripts for different research domains

## [1.0.0] - 2025-05-22

### Added
- Initial public release
- Core functionality for scientific plot scaling
- Support for mechanical engineering applications
- Integration examples for LaTeX documents
- Automated testing and quality assurance

### Technical Details
- Python 3.7+ support
- Dependencies: matplotlib, seaborn, numpy, scipy
- Cross-platform compatibility (Windows, macOS, Linux)
- Memory-efficient processing
- Error handling and validation

### Research Applications
- CFD mesh convergence studies
- Experimental data visualization  
- Multi-panel scientific figures
- Biomedical engineering plots
- Statistical analysis visualization

---

### Future Releases (Planned)

#### [1.1.0] - Planned
- Support for 3D plots
- Interactive plot previews
- More journal format presets
- Batch processing improvements
- Performance optimizations

#### [1.2.0] - Planned  
- GUI application for non-programmers
- Integration with Jupyter notebooks
- Custom color palette support
- Advanced grid layouts
- Export to multiple formats simultaneously

#### [2.0.0] - Planned
- Breaking changes for improved API
- Plugin system for custom plot types
- Cloud-based processing options
- Integration with reference managers
- Advanced statistical plot templates

---

### Version History Summary

| Version | Release Date | Key Features |
|---------|-------------|--------------|
| 1.0.0   | 2025-05-22  | Initial release, core functionality |

### Migration Guides

#### From Manual Matplotlib to Plot Scaler

**Before:**
```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, y)
ax.set_xlabel('X axis', fontsize=12)
plt.savefig('plot.pdf', dpi=300)
```

**After:**
```python
from plot_scaler import ScientificPlotter
plotter = ScientificPlotter()
fig, ax = plotter.create_figure()
ax.plot(x, y)
plotter.finalize_plot(fig, ax, xlabel='X axis')
plotter.save_plot(fig, 'plot')
```

### Known Issues

- LaTeX rendering requires system LaTeX installation for full functionality
- Some matplotlib styles may not be fully compatible
- Large datasets may require memory optimization

### Contributors

- Research Community Contributors
- University of Manchester Mechanical Engineering Department
- Open source contributors (see GitHub contributors page)

### Acknowledgments

Special thanks to:
- Matplotlib and seaborn development teams
- LaTeX community for document standards
- Research community for feedback and testing
- Academic institutions supporting open source development