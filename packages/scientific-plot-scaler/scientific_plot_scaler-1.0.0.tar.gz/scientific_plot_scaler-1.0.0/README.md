# Scientific Plot Scaler for LaTeX Documents

A Python tool designed to solve the common problem of text scaling in scientific plots when integrating them into LaTeX documents. Whether you're preparing figures for single-column, double-column, or subfigure layouts, this tool automatically calculates appropriate font sizes and figure dimensions for publication-ready plots.

## Problem Statement

When creating scientific plots for LaTeX documents (like papers, theses, dissertations), researchers often face these issues:

- **Text too small**: When a plot is scaled down to fit in a column, text becomes unreadable
- **Inconsistent sizing**: Different plots have different text sizes when included in the document
- **Manual adjustment**: Constantly tweaking font sizes for different layout requirements
- **Poor quality**: Plots that look good on screen but poor in print

## Solution

This tool automatically:
- ✅ Calculates optimal figure dimensions for different LaTeX layouts
- ✅ Scales text proportionally to maintain readability
- ✅ Provides consistent sizing across all your figures
- ✅ Generates publication-quality output formats (PDF, PNG, EPS, SVG)

## Installation

```bash
# Clone the repository
git clone https://github.com/VijayN10/scientific-plot-scaler.git
cd scientific-plot-scaler

# Install dependencies
pip install matplotlib seaborn numpy scipy

# Or using conda
conda install matplotlib seaborn numpy scipy
```

## Quick Start

### 1. Basic Usage

```python
from plot_scaler import ScientificPlotter, PlotConfig
import numpy as np

# Create plotter for single column layout
plotter = ScientificPlotter()

# Create your plot
fig, ax = plotter.create_figure()

# Your plotting code
x = np.linspace(0, 10, 100)
y = np.sin(x)
ax.plot(x, y, label='sin(x)')

# Finalize and save
plotter.finalize_plot(fig, ax, 
                     title="Sine Wave",
                     xlabel="x",
                     ylabel="sin(x)")
plotter.save_plot(fig, "sine_wave")
```

### 2. Different Layout Types

```python
# Single column (default)
config = PlotConfig(layout_type="single")
plotter = ScientificPlotter(config)

# Double column (full text width)
config = PlotConfig(layout_type="double")
plotter = ScientificPlotter(config)

# Subfigure (2x1 layout)
config = PlotConfig(
    layout_type="subfigure",
    subfigure_rows=1,
    subfigure_cols=2
)
plotter = ScientificPlotter(config)
```

### 3. Command Line Usage

```bash
# Create example configuration files
python plot_scaler.py --create-examples

# Create demonstration plots
python plot_scaler.py --demo

# Use custom configuration
python plot_scaler.py --config my_config.json
```

## Configuration

### JSON Configuration File

```json
{
  "layout_type": "single",
  "latex_column_width": 3.5,
  "latex_text_width": 7.0,
  "base_font_size": 10,
  "format": "pdf",
  "dpi": 300,
  "grid": true,
  "style": "seaborn-v0_8"
}
```

### Available Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `layout_type` | "single", "double", or "subfigure" | "single" |
| `latex_column_width` | Width of single column (inches) | 3.5 |
| `latex_text_width` | Full text width (inches) | 7.0 |
| `base_font_size` | LaTeX document font size | 10 |
| `format` | Output format: "pdf", "png", "eps", "svg" | "pdf" |
| `dpi` | Resolution for raster formats | 300 |
| `subfigure_rows` | Rows in subfigure layout | 1 |
| `subfigure_cols` | Columns in subfigure layout | 2 |

## Advanced Usage

### Custom Styling

```python
config = PlotConfig(
    style="seaborn-v0_8",
    color_palette="deep",
    spine_style="minimal",  # "classic", "minimal", "none"
    grid=True,
    title_scale=1.2,
    label_scale=1.0,
    tick_scale=0.9,
    legend_scale=0.9
)
```

### LaTeX Integration

```latex
% In your LaTeX document
\documentclass[twocolumn]{article}
\usepackage{graphicx}
\usepackage{subcaption}

% Single column figure
\begin{figure}[h]
    \centering
    \includegraphics[width=\columnwidth]{plots/mesh_convergence_single.pdf}
    \caption{Mesh convergence study}
    \label{fig:convergence}
\end{figure}

% Double column figure
\begin{figure*}[t]
    \centering
    \includegraphics[width=\textwidth]{plots/mesh_convergence_double.pdf}
    \caption{Wide mesh convergence study}
    \label{fig:convergence_wide}
\end{figure*}

% Subfigures
\begin{figure}[h]
    \centering
    \begin{subfigure}{0.48\textwidth}
        \includegraphics[width=\textwidth]{plots/result_a.pdf}
        \caption{Result A}
    \end{subfigure}
    \hfill
    \begin{subfigure}{0.48\textwidth}
        \includegraphics[width=\textwidth]{plots/result_b.pdf}
        \caption{Result B}
    \end{subfigure}
    \caption{Comparison of results}
\end{figure}
```

## Examples

The repository includes several example scripts:

- `examples/mesh_convergence.py` - CFD mesh convergence study
- `examples/experimental_data.py` - Experimental data with error bars
- `examples/multi_subplot.py` - Multiple subplots with shared axes
- `examples/aaa_growth.py` - AAA growth prediction plots

## Features for Research Papers

### Automatic Text Scaling
- Font sizes automatically adjusted based on figure dimensions
- Consistent text appearance across different layout types
- Proper scaling for subfigures and multi-panel plots

### Publication Quality
- High DPI output for crisp text and lines
- Vector formats (PDF, EPS, SVG) for scalable graphics
- LaTeX-compatible font rendering

### Research-Friendly
- Easy integration with existing matplotlib code
- Configurable styling for different journals
- Batch processing capabilities for multiple figures

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup

```bash
git clone https://github.com/VijayN10/scientific-plot-scaler.git
cd scientific-plot-scaler
pip install -e .
pip install pytest black flake8  # development dependencies
```

### Running Tests

```bash
pytest tests/
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Citation

If you use this tool in your research, please cite:

```bibtex
@software{scientific_plot_scaler,
  title={Scientific Plot Scaler for LaTeX Documents},
  author={Research Community},
  url={https://github.com/VijayN10/scientific-plot-scaler},
  year={2025}
}
```

## Acknowledgments

This tool was developed to address common plotting challenges faced by researchers, particularly in mechanical engineering and computational fluid dynamics. Special thanks to the University of Manchester research community for feedback and testing.