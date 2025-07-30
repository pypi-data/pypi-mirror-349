#!/usr/bin/env python3
"""
Basic Usage Example for Scientific Plot Scaler
==============================================

This example demonstrates the basic functionality of the Scientific Plot Scaler
for creating publication-ready plots with proper text scaling.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scientific_plot_scaler import ScientificPlotter, PlotConfig
import numpy as np
import matplotlib.pyplot as plt

def create_simple_line_plot():
    """Create a simple line plot with proper scaling"""
    print("Creating simple line plot...")
    
    # Create data
    x = np.linspace(0, 2*np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(2*x)
    
    # Single column configuration
    config = PlotConfig(layout_type="single")
    plotter = ScientificPlotter(config)
    
    # Create figure
    fig, ax = plotter.create_figure()
    
    # Plot data
    ax.plot(x, y1, label='sin(x)', linewidth=2)
    ax.plot(x, y2, label='cos(x)', linewidth=2)
    ax.plot(x, y3, label='sin(2x)', linewidth=2, linestyle='--')
    
    # Finalize plot
    plotter.finalize_plot(fig, ax,
                         title="Trigonometric Functions",
                         xlabel="x (radians)",
                         ylabel="Amplitude",
                         legend=True)
    
    # Save plot
    filename = plotter.save_plot(fig, "basic_trig_functions")
    print(f"✓ Saved: {filename}")
    plt.close(fig)

def create_scatter_plot():
    """Create a scatter plot with error bars"""
    print("Creating scatter plot with error bars...")
    
    # Generate experimental-like data
    np.random.seed(42)
    x = np.linspace(1, 10, 15)
    y = 2.5 * x + 3 + np.random.normal(0, 2, len(x))
    yerr = np.random.uniform(0.5, 2.0, len(x))
    
    # Double column configuration
    config = PlotConfig(layout_type="double")
    plotter = ScientificPlotter(config)
    
    fig, ax = plotter.create_figure()
    
    # Scatter plot with error bars
    ax.errorbar(x, y, yerr=yerr, fmt='o', capsize=5, capthick=2,
                elinewidth=1.5, markersize=6, alpha=0.8, label='Experimental data')
    
    # Fit line
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.plot(x, p(x), 'r--', linewidth=2, alpha=0.8, label=f'Linear fit: y = {z[0]:.2f}x + {z[1]:.2f}')
    
    plotter.finalize_plot(fig, ax,
                         title="Experimental Data Analysis",
                         xlabel="Input Parameter",
                         ylabel="Response Variable",
                         legend=True)
    
    filename = plotter.save_plot(fig, "experimental_scatter")
    print(f"✓ Saved: {filename}")
    plt.close(fig)

def create_multi_subplot():
    """Create multiple subplots"""
    print("Creating multi-subplot figure...")
    
    config = PlotConfig(layout_type="single")
    plotter = ScientificPlotter(config)
    
    # Create figure with custom subplot arrangement
    fig = plt.figure(figsize=plotter.calculate_figure_size())
    
    # Create 2x2 subplots
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    font_sizes = plotter.calculate_font_sizes()
    
    # Subplot 1: Line plot
    ax1 = fig.add_subplot(gs[0, 0])
    x = np.linspace(0, 5, 50)
    ax1.plot(x, np.exp(-x), 'b-', linewidth=2)
    ax1.set_title('A) Exponential Decay', fontsize=font_sizes['title'], loc='left')
    ax1.set_xlabel('Time', fontsize=font_sizes['label'])
    ax1.set_ylabel('Amplitude', fontsize=font_sizes['label'])
    ax1.tick_params(labelsize=font_sizes['tick'])
    ax1.grid(True, alpha=0.3)
    
    # Subplot 2: Bar plot
    ax2 = fig.add_subplot(gs[0, 1])
    categories = ['A', 'B', 'C', 'D']
    values = [23, 45, 56, 78]
    ax2.bar(categories, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    ax2.set_title('B) Category Comparison', fontsize=font_sizes['title'], loc='left')
    ax2.set_xlabel('Category', fontsize=font_sizes['label'])
    ax2.set_ylabel('Value', fontsize=font_sizes['label'])
    ax2.tick_params(labelsize=font_sizes['tick'])
    
    # Subplot 3: Histogram
    ax3 = fig.add_subplot(gs[1, 0])
    data = np.random.normal(0, 1, 1000)
    ax3.hist(data, bins=30, alpha=0.7, color='green', edgecolor='black')
    ax3.set_title('C) Normal Distribution', fontsize=font_sizes['title'], loc='left')
    ax3.set_xlabel('Value', fontsize=font_sizes['label'])
    ax3.set_ylabel('Frequency', fontsize=font_sizes['label'])
    ax3.tick_params(labelsize=font_sizes['tick'])
    ax3.grid(True, alpha=0.3)
    
    # Subplot 4: Heatmap-style
    ax4 = fig.add_subplot(gs[1, 1])
    data_2d = np.random.random((10, 10))
    im = ax4.imshow(data_2d, cmap='viridis', aspect='auto')
    ax4.set_title('D) 2D Data', fontsize=font_sizes['title'], loc='left')
    ax4.set_xlabel('X coordinate', fontsize=font_sizes['label'])
    ax4.set_ylabel('Y coordinate', fontsize=font_sizes['label'])
    ax4.tick_params(labelsize=font_sizes['tick'])
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax4, shrink=0.8)
    cbar.ax.tick_params(labelsize=font_sizes['tick']*0.9)
    
    filename = plotter.save_plot(fig, "multi_subplot_example")
    print(f"✓ Saved: {filename}")
    plt.close(fig)

def demonstrate_different_layouts():
    """Show same plot in different layouts"""
    print("Demonstrating different layout options...")
    
    # Create sample data
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x) * np.exp(-x/5)
    y2 = np.cos(x) * np.exp(-x/5)
    
    layouts = {
        'single': PlotConfig(layout_type="single"),
        'double': PlotConfig(layout_type="double"),
        'subfigure': PlotConfig(layout_type="subfigure", subfigure_cols=2)
    }
    
    for layout_name, config in layouts.items():
        plotter = ScientificPlotter(config)
        fig, ax = plotter.create_figure()
        
        ax.plot(x, y1, label='Damped sine', linewidth=2)
        ax.plot(x, y2, label='Damped cosine', linewidth=2)
        
        plotter.finalize_plot(fig, ax,
                             title=f"Damped Oscillations ({layout_name.title()} Layout)",
                             xlabel="Time (s)",
                             ylabel="Amplitude",
                             legend=True)
        
        filename = plotter.save_plot(fig, f"damped_oscillations_{layout_name}")
        print(f"✓ Saved {layout_name} layout: {filename}")
        plt.close(fig)

def main():
    """Run all basic examples"""
    print("Scientific Plot Scaler - Basic Usage Examples")
    print("=" * 50)
    
    # Create examples
    create_simple_line_plot()
    create_scatter_plot()
    create_multi_subplot()
    demonstrate_different_layouts()
    
    print("\n" + "=" * 50)
    print("All basic examples completed!")
    print("\nGenerated plots can be used in LaTeX documents like this:")
    print("\n% Single column")
    print("\\begin{figure}[h]")
    print("    \\centering")
    print("    \\includegraphics[width=\\columnwidth]{plots/basic_trig_functions.pdf}")
    print("    \\caption{Basic trigonometric functions}")
    print("\\end{figure}")
    print("\n% Double column")
    print("\\begin{figure*}[t]")
    print("    \\centering")
    print("    \\includegraphics[width=\\textwidth]{plots/experimental_scatter.pdf}")
    print("    \\caption{Experimental data analysis}")
    print("\\end{figure*}")

if __name__ == "__main__":
    main()