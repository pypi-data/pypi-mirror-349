#!/usr/bin/env python3
"""
Scientific Plot Scaler for LaTeX Documents
==========================================

A tool to create publication-ready scientific plots with proper text scaling
for different LaTeX document layouts (single column, double column, subfigures).

Author: Vijay Nandurdikar
License: MIT
Repository: https://github.com/VijayN10/scientific-plot-scaler

Installation:
pip install matplotlib seaborn numpy scipy

Usage:
python plot_scaler.py --config config.json
or
from plot_scaler import ScientificPlotter
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import json
import argparse
import os
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
from pathlib import Path

@dataclass
class PlotConfig:
    """Configuration for plot dimensions and styling"""
    # LaTeX document settings
    latex_column_width: float = 3.5   # inches - typical single column width
    latex_text_width: float = 7.0     # inches - typical full text width
    latex_margin: float = 0.1         # inches - margin for safety
    
    # Plot layout options
    layout_type: str = "single"       # "single", "double", "subfigure"
    subfigure_rows: int = 1
    subfigure_cols: int = 2
    
    # Font settings
    base_font_size: int = 10          # LaTeX document font size
    title_scale: float = 1.2
    label_scale: float = 1.0
    tick_scale: float = 0.9
    legend_scale: float = 0.9
    
    # Figure quality
    dpi: int = 300
    format: str = "pdf"               # "pdf", "png", "eps", "svg"
    
    # Style preferences
    style: str = "seaborn-v0_8"       # matplotlib style
    color_palette: str = "deep"       # seaborn color palette
    grid: bool = True
    spine_style: str = "classic"      # "classic", "minimal", "none"

class ScientificPlotter:
    """Main class for creating scalable scientific plots"""
    
    def __init__(self, config: PlotConfig = None):
        self.config = config or PlotConfig()
        self._setup_matplotlib()
        
    def _setup_matplotlib(self):
        """Configure matplotlib for publication-quality plots"""
        # Set backend for better text rendering
        mpl.use('Agg')
        
        # Configure matplotlib for LaTeX-like text rendering
        plt.rcParams.update({
            'font.family': 'serif',
            'font.serif': ['Times', 'Computer Modern Roman'],
            'text.usetex': False,  # Set to True if LaTeX is installed
            'mathtext.fontset': 'cm',
            'axes.linewidth': 0.8,
            'axes.spines.left': True,
            'axes.spines.bottom': True,
            'axes.spines.top': False,
            'axes.spines.right': False,
            'xtick.direction': 'in',
            'ytick.direction': 'in',
            'xtick.major.size': 3,
            'ytick.major.size': 3,
            'xtick.minor.size': 2,
            'ytick.minor.size': 2,
            'legend.frameon': False,
            'figure.autolayout': True,
        })
        
    def calculate_figure_size(self) -> Tuple[float, float]:
        """Calculate optimal figure size based on layout type"""
        margin = self.config.latex_margin
        
        if self.config.layout_type == "single":
            width = self.config.latex_column_width - 2 * margin
            height = width * 0.75  # Golden ratio approximation
            
        elif self.config.layout_type == "double":
            width = self.config.latex_text_width - 2 * margin
            height = width * 0.5   # Wider aspect ratio for double column
            
        elif self.config.layout_type == "subfigure":
            available_width = self.config.latex_text_width - 2 * margin
            width = available_width / self.config.subfigure_cols - 0.1
            height = width * 0.8   # Slightly taller for subfigures
            
        else:
            raise ValueError(f"Unknown layout type: {self.config.layout_type}")
            
        return width, height
    
    def calculate_font_sizes(self) -> Dict[str, float]:
        """Calculate font sizes based on figure size and layout"""
        width, height = self.calculate_figure_size()
        
        # Scale factor based on figure size relative to standard size
        scale_factor = min(width / 3.5, height / 2.6)
        
        # Additional scaling for different layouts
        if self.config.layout_type == "subfigure":
            scale_factor *= 0.9  # Slightly smaller for subfigures
        elif self.config.layout_type == "double":
            scale_factor *= 1.1  # Slightly larger for double column
            
        base_size = self.config.base_font_size * scale_factor
        
        return {
            'title': base_size * self.config.title_scale,
            'label': base_size * self.config.label_scale,
            'tick': base_size * self.config.tick_scale,
            'legend': base_size * self.config.legend_scale,
        }
    
    def create_figure(self, **kwargs) -> Tuple[plt.Figure, plt.Axes]:
        """Create a properly sized figure with appropriate font scaling"""
        width, height = self.calculate_figure_size()
        font_sizes = self.calculate_font_sizes()
        
        # Apply style
        if hasattr(plt.style, 'context'):
            style_context = plt.style.context(self.config.style)
        else:
            style_context = plt.style.context('default')
            
        with style_context:
            fig, ax = plt.subplots(figsize=(width, height), **kwargs)
            
        # Apply font sizes
        ax.tick_params(labelsize=font_sizes['tick'])
        
        return fig, ax
    
    def finalize_plot(self, fig: plt.Figure, ax: plt.Axes, 
                     title: str = "", xlabel: str = "", ylabel: str = "",
                     legend: bool = True, tight_layout: bool = True) -> plt.Figure:
        """Apply final styling and prepare plot for export"""
        font_sizes = self.calculate_font_sizes()
        
        # Set labels and title
        if title:
            ax.set_title(title, fontsize=font_sizes['title'], pad=10)
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=font_sizes['label'])
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=font_sizes['label'])
            
        # Configure legend
        if legend and ax.get_legend_handles_labels()[0]:
            ax.legend(fontsize=font_sizes['legend'], 
                     loc='best', frameon=False)
        
        # Grid styling
        if self.config.grid:
            ax.grid(True, alpha=0.3, linewidth=0.5)
            ax.set_axisbelow(True)
            
        # Spine styling
        if self.config.spine_style == "minimal":
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        elif self.config.spine_style == "none":
            for spine in ax.spines.values():
                spine.set_visible(False)
                
        # Tight layout
        if tight_layout:
            fig.tight_layout(pad=0.5)
            
        return fig
    
    def save_plot(self, fig: plt.Figure, filename: str, 
                  output_dir: str = "plots") -> str:
        """Save plot with appropriate settings for LaTeX inclusion"""
        Path(output_dir).mkdir(exist_ok=True)
        
        # Ensure proper file extension
        base_name = Path(filename).stem
        full_filename = f"{base_name}.{self.config.format}"
        full_path = Path(output_dir) / full_filename
        
        # Save with high quality settings
        fig.savefig(full_path, 
                   dpi=self.config.dpi,
                   bbox_inches='tight',
                   pad_inches=0.05,
                   facecolor='white',
                   edgecolor='none')
        
        return str(full_path)
    
    def create_mesh_convergence_example(self) -> Tuple[plt.Figure, plt.Axes]:
        """Create an example mesh convergence plot similar to the uploaded image"""
        # Simulate mesh convergence data
        positions = np.linspace(0, 50, 100)
        
        # Different mesh densities
        mesh_data = {
            '6.7K H-4 cells': np.exp(-0.1 * (positions - 25)**2 / 100) * 0.3 + 0.15,
            '1.29E+06 cells': np.exp(-0.1 * (positions - 25)**2 / 100) * 0.25 + 0.12,
            '2.7K H-4 cells': np.exp(-0.1 * (positions - 25)**2 / 100) * 0.28 + 0.13,
            '4.0M 847 cells': np.exp(-0.1 * (positions - 25)**2 / 100) * 0.24 + 0.11,
            '7.73K 742 cells': np.exp(-0.1 * (positions - 25)**2 / 100) * 0.26 + 0.115,
        }
        
        fig, ax = self.create_figure()
        
        colors = plt.cm.Set1(np.linspace(0, 1, len(mesh_data)))
        
        for i, (label, data) in enumerate(mesh_data.items()):
            ax.plot(positions, data, label=label, linewidth=1.5, 
                   color=colors[i], alpha=0.8)
        
        self.finalize_plot(fig, ax,
                          title="Mesh Convergence: Velocity Distribution along Centerline",
                          xlabel="Position along Centerline",
                          ylabel="Velocity (m/s)",
                          legend=True)
        
        return fig, ax

def load_config(config_file: str) -> PlotConfig:
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            config_dict = json.load(f)
        return PlotConfig(**config_dict)
    except FileNotFoundError:
        print(f"Config file {config_file} not found. Using default configuration.")
        return PlotConfig()

def create_example_config():
    """Create example configuration files"""
    configs = {
        'single_column.json': {
            'layout_type': 'single',
            'latex_column_width': 3.5,
            'base_font_size': 10,
            'format': 'pdf'
        },
        'double_column.json': {
            'layout_type': 'double', 
            'latex_text_width': 7.0,
            'latex_column_width': 3.5,
            'base_font_size': 10,
            'format': 'pdf'
        },
        'subfigure.json': {
            'layout_type': 'subfigure',
            'subfigure_rows': 1,
            'subfigure_cols': 2,
            'latex_text_width': 7.0,
            'base_font_size': 9,
            'format': 'pdf'
        }
    }
    
    for filename, config in configs.items():
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Created example config: {filename}")

def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(description='Scientific Plot Scaler for LaTeX Documents')
    parser.add_argument('--config', '-c', default='config.json',
                       help='Configuration file path')
    parser.add_argument('--create-examples', action='store_true',
                       help='Create example configuration files')
    parser.add_argument('--demo', action='store_true',
                       help='Create demonstration plots')
    
    args = parser.parse_args()
    
    if args.create_examples:
        create_example_config()
        return
    
    # Load configuration
    config = load_config(args.config)
    plotter = ScientificPlotter(config)
    
    if args.demo:
        # Create demonstration plots
        print("Creating demonstration plots...")
        
        # Single column version
        config.layout_type = "single" 
        plotter.config = config
        fig, ax = plotter.create_mesh_convergence_example()
        plotter.save_plot(fig, "mesh_convergence_single")
        plt.close(fig)
        
        # Double column version
        config.layout_type = "double"
        plotter.config = config  
        fig, ax = plotter.create_mesh_convergence_example()
        plotter.save_plot(fig, "mesh_convergence_double")
        plt.close(fig)
        
        # Subfigure version
        config.layout_type = "subfigure"
        plotter.config = config
        fig, ax = plotter.create_mesh_convergence_example()
        plotter.save_plot(fig, "mesh_convergence_subfigure")
        plt.close(fig)
        
        print("Demonstration plots created in 'plots' directory")

if __name__ == "__main__":
    main()