#!/usr/bin/env python3
"""
Example: AAA Growth Prediction Plots
====================================

This example demonstrates creating publication-ready plots for abdominal aortic
aneurysm (AAA) growth prediction research, specifically designed for PhD thesis
and journal publications.

"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plot_scaler import ScientificPlotter, PlotConfig
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def generate_aaa_data():
    """Generate synthetic AAA growth data for demonstration"""
    # Time points (months)
    time = np.linspace(0, 36, 37)  # 3 years of monthly data
    
    # Patient cohorts with different growth rates
    cohorts = {
        'Low Risk (n=45)': {
            'baseline': 35,  # mm
            'growth_rate': 1.2,  # mm/year
            'noise': 0.8
        },
        'Medium Risk (n=38)': {
            'baseline': 42,
            'growth_rate': 2.5,
            'noise': 1.2
        },
        'High Risk (n=22)': {
            'baseline': 48,
            'growth_rate': 4.1,
            'noise': 1.5
        }
    }
    
    data = {}
    for cohort_name, params in cohorts.items():
        # Generate growth trajectory
        diameter = params['baseline'] + (params['growth_rate'] * time / 12)
        
        # Add realistic noise
        noise = np.random.normal(0, params['noise'], len(time))
        diameter += noise
        
        # Ensure no shrinkage (biological constraint)
        for i in range(1, len(diameter)):
            if diameter[i] < diameter[i-1]:
                diameter[i] = diameter[i-1] + np.random.exponential(0.1)
        
        data[cohort_name] = {
            'time': time,
            'diameter': diameter,
            'baseline': params['baseline'],
            'growth_rate': params['growth_rate']
        }
    
    return data

def create_growth_prediction_plot(plotter: ScientificPlotter):
    """Create AAA growth prediction plot with confidence intervals"""
    
    # Generate data
    aaa_data = generate_aaa_data()
    
    fig, ax = plotter.create_figure()
    
    colors = ['#2E86C1', '#28B463', '#F39C12']  # Professional color scheme
    
    for i, (cohort_name, data) in enumerate(aaa_data.items()):
        time = data['time']
        diameter = data['diameter']
        
        # Plot actual data points
        ax.scatter(time[::3], diameter[::3], 
                  color=colors[i], alpha=0.6, s=20, 
                  label=f'{cohort_name}')
        
        # Fit polynomial for trend line
        z = np.polyfit(time, diameter, 2)
        p = np.poly1d(z)
        
        # Create smooth curve
        time_smooth = np.linspace(0, 36, 100)
        diameter_smooth = p(time_smooth)
        
        # Plot trend line
        ax.plot(time_smooth, diameter_smooth, 
               color=colors[i], linewidth=2, alpha=0.8)
        
        # Add confidence interval (simplified)
        residuals = diameter - p(time)
        std_error = np.std(residuals)
        
        ax.fill_between(time_smooth, 
                       diameter_smooth - 1.96*std_error,
                       diameter_smooth + 1.96*std_error,
                       color=colors[i], alpha=0.2)
    
    # Add intervention threshold
    ax.axhline(y=55, color='red', linestyle='--', linewidth=2, 
               alpha=0.8, label='Intervention Threshold (55mm)')
    
    # Customize plot
    plotter.finalize_plot(fig, ax,
                         title="AAA Growth Prediction: Multi-Cohort Analysis",
                         xlabel="Time (months)",
                         ylabel="Maximum Diameter (mm)",
                         legend=True)
    
    # Add annotation
    ax.text(24, 40, 'Generative AI\nPrediction Model', 
           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7),
           fontsize=plotter.calculate_font_sizes()['legend'])
    
    return fig, ax

def create_probabilistic_risk_plot(plotter: ScientificPlotter):
    """Create probabilistic risk assessment plot"""
    
    fig, ax = plotter.create_figure()
    
    # Risk categories
    diameter_range = np.linspace(30, 70, 100)
    
    # Probability curves based on diameter
    rupture_risk_1yr = 1 / (1 + np.exp(-0.3 * (diameter_range - 55)))
    rupture_risk_5yr = 1 / (1 + np.exp(-0.2 * (diameter_range - 45)))
    
    ax.plot(diameter_range, rupture_risk_1yr * 100, 
           color='#E74C3C', linewidth=2.5, label='1-year rupture risk')
    ax.plot(diameter_range, rupture_risk_5yr * 100, 
           color='#8E44AD', linewidth=2.5, label='5-year rupture risk')
    
    # Fill risk zones
    ax.fill_between(diameter_range, 0, rupture_risk_1yr * 100,
                   where=(diameter_range >= 55), alpha=0.2, color='red',
                   label='High Risk Zone')
    
    ax.fill_between(diameter_range, 0, rupture_risk_5yr * 100,
                   where=(diameter_range >= 45) & (diameter_range < 55), 
                   alpha=0.2, color='orange', label='Moderate Risk Zone')
    
    plotter.finalize_plot(fig, ax,
                         title="Probabilistic Rupture Risk Assessment",
                         xlabel="Maximum AAA Diameter (mm)",
                         ylabel="Rupture Risk (%)",
                         legend=True)
    
    # Set appropriate y-axis limits
    ax.set_ylim(0, 100)
    ax.set_xlim(30, 70)
    
    return fig, ax

def create_ai_validation_plot(plotter: ScientificPlotter):
    """Create AI model validation plot"""
    
    fig, ax = plotter.create_figure()
    
    # Synthetic validation data
    np.random.seed(42)
    n_patients = 50
    
    # Actual growth rates
    actual_growth = np.random.gamma(2, 1.5, n_patients)
    
    # AI predicted growth rates (with some correlation + noise)
    ai_predicted = actual_growth * (0.8 + 0.4 * np.random.random(n_patients)) + \
                  np.random.normal(0, 0.3, n_patients)
    
    # Traditional model predictions (less accurate)
    traditional_predicted = actual_growth * (0.6 + 0.6 * np.random.random(n_patients)) + \
                           np.random.normal(0, 0.5, n_patients)
    
    # Scatter plots
    ax.scatter(actual_growth, ai_predicted, 
              color='#3498DB', alpha=0.7, s=30, 
              label='Generative AI Model')
    ax.scatter(actual_growth, traditional_predicted, 
              color='#95A5A6', alpha=0.7, s=30, 
              label='Traditional Model')
    
    # Perfect prediction line
    max_val = max(np.max(actual_growth), np.max(ai_predicted), np.max(traditional_predicted))
    ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.5, linewidth=1.5, 
           label='Perfect Prediction')
    
    # Calculate and display R²
    r2_ai = stats.pearsonr(actual_growth, ai_predicted)[0]**2
    r2_trad = stats.pearsonr(actual_growth, traditional_predicted)[0]**2
    
    ax.text(0.05, 0.95, f'AI Model R² = {r2_ai:.3f}', 
           transform=ax.transAxes, fontsize=plotter.calculate_font_sizes()['legend'],
           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    ax.text(0.05, 0.85, f'Traditional R² = {r2_trad:.3f}', 
           transform=ax.transAxes, fontsize=plotter.calculate_font_sizes()['legend'],
           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7))
    
    plotter.finalize_plot(fig, ax,
                         title="AI Model Validation: Growth Rate Prediction",
                         xlabel="Actual Growth Rate (mm/year)",
                         ylabel="Predicted Growth Rate (mm/year)",
                         legend=True)
    
    return fig, ax

def create_multi_panel_figure(plotter: ScientificPlotter):
    """Create a multi-panel figure suitable for journal publication"""
    
    # Create figure with subplots
    fig = plt.figure(figsize=plotter.calculate_figure_size())
    
    # Create a 2x2 grid of subplots
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # Panel A: Growth curves
    ax1 = fig.add_subplot(gs[0, :])  # Top row, full width
    aaa_data = generate_aaa_data()
    colors = ['#2E86C1', '#28B463', '#F39C12']
    
    for i, (cohort_name, data) in enumerate(aaa_data.items()):
        ax1.plot(data['time'], data['diameter'], 
                color=colors[i], linewidth=2, label=cohort_name, alpha=0.8)
    
    ax1.set_title('A) Longitudinal Growth Patterns', 
                 fontsize=plotter.calculate_font_sizes()['title'], loc='left')
    ax1.set_xlabel('Time (months)', fontsize=plotter.calculate_font_sizes()['label'])
    ax1.set_ylabel('Diameter (mm)', fontsize=plotter.calculate_font_sizes()['label'])
    ax1.legend(fontsize=plotter.calculate_font_sizes()['legend'])
    ax1.grid(True, alpha=0.3)
    
    # Panel B: Risk assessment
    ax2 = fig.add_subplot(gs[1, 0])  # Bottom left
    diameter_range = np.linspace(30, 70, 100)
    rupture_risk = 1 / (1 + np.exp(-0.3 * (diameter_range - 55)))
    
    ax2.plot(diameter_range, rupture_risk * 100, 'r-', linewidth=2.5)
    ax2.fill_between(diameter_range, 0, rupture_risk * 100,
                    where=(diameter_range >= 55), alpha=0.3, color='red')
    ax2.set_title('B) Rupture Risk', 
                 fontsize=plotter.calculate_font_sizes()['title'], loc='left')
    ax2.set_xlabel('Diameter (mm)', fontsize=plotter.calculate_font_sizes()['label'])
    ax2.set_ylabel('Risk (%)', fontsize=plotter.calculate_font_sizes()['label'])
    ax2.grid(True, alpha=0.3)
    
    # Panel C: AI validation
    ax3 = fig.add_subplot(gs[1, 1])  # Bottom right
    np.random.seed(42)
    actual = np.random.gamma(2, 1.5, 30)
    predicted = actual * (0.8 + 0.4 * np.random.random(30)) + np.random.normal(0, 0.3, 30)
    
    ax3.scatter(actual, predicted, color='#3498DB', alpha=0.7)
    max_val = max(np.max(actual), np.max(predicted))
    ax3.plot([0, max_val], [0, max_val], 'k--', alpha=0.5)
    ax3.set_title('C) AI Validation', 
                 fontsize=plotter.calculate_font_sizes()['title'], loc='left')
    ax3.set_xlabel('Actual (mm/yr)', fontsize=plotter.calculate_font_sizes()['label'])
    ax3.set_ylabel('Predicted (mm/yr)', fontsize=plotter.calculate_font_sizes()['label'])
    ax3.grid(True, alpha=0.3)
    
    # Apply font sizes to all subplots
    for ax in [ax1, ax2, ax3]:
        ax.tick_params(labelsize=plotter.calculate_font_sizes()['tick'])
    
    return fig, [ax1, ax2, ax3]

def main():
    """Main function to generate all AAA-related plots"""
    
    print("Generating AAA Growth Prediction Plots...")
    print("=" * 50)
    
    # Configuration for different layouts
    layouts = {
        'single_column': PlotConfig(
            layout_type="single",
            latex_column_width=3.5,
            base_font_size=10
        ),
        'double_column': PlotConfig(
            layout_type="double",
            latex_text_width=7.0,
            base_font_size=10
        ),
        'subfigure': PlotConfig(
            layout_type="subfigure",
            subfigure_cols=2,
            subfigure_rows=1,
            base_font_size=9
        )
    }
    
    # Create plots for each layout
    for layout_name, config in layouts.items():
        print(f"\nCreating plots for {layout_name} layout...")
        plotter = ScientificPlotter(config)
        
        # 1. Growth prediction plot
        fig1, ax1 = create_growth_prediction_plot(plotter)
        filename1 = plotter.save_plot(fig1, f"aaa_growth_prediction_{layout_name}")
        print(f"  ✓ Growth prediction plot saved: {filename1}")
        plt.close(fig1)
        
        # 2. Risk assessment plot
        fig2, ax2 = create_probabilistic_risk_plot(plotter)
        filename2 = plotter.save_plot(fig2, f"aaa_risk_assessment_{layout_name}")
        print(f"  ✓ Risk assessment plot saved: {filename2}")
        plt.close(fig2)
        
        # 3. AI validation plot
        fig3, ax3 = create_ai_validation_plot(plotter)
        filename3 = plotter.save_plot(fig3, f"aaa_ai_validation_{layout_name}")
        print(f"  ✓ AI validation plot saved: {filename3}")
        plt.close(fig3)
        
        # 4. Multi-panel figure (only for single column to avoid overcrowding)
        if layout_name == 'single_column':
            fig4, axes4 = create_multi_panel_figure(plotter)
            filename4 = plotter.save_plot(fig4, f"aaa_multi_panel_{layout_name}")
            print(f"  ✓ Multi-panel figure saved: {filename4}")
            plt.close(fig4)
    
    print(f"\n{'='*50}")
    print("All plots generated successfully!")
    print("\nLaTeX Integration Examples:")
    print("-" * 25)
    
    print("\n% Single column figure")
    print("\\begin{figure}[h]")
    print("    \\centering")
    print("    \\includegraphics[width=\\columnwidth]{plots/aaa_growth_prediction_single_column.pdf}")
    print("    \\caption{AAA growth prediction using generative AI model}")
    print("    \\label{fig:aaa_growth}")
    print("\\end{figure}")
    
    print("\n% Double column figure")
    print("\\begin{figure*}[t]")
    print("    \\centering")
    print("    \\includegraphics[width=\\textwidth]{plots/aaa_growth_prediction_double_column.pdf}")
    print("    \\caption{Comprehensive AAA growth analysis}")
    print("    \\label{fig:aaa_growth_wide}")
    print("\\end{figure*}")
    
    print("\n% Subfigures")
    print("\\begin{figure}[h]")
    print("    \\centering")
    print("    \\begin{subfigure}{0.48\\textwidth}")
    print("        \\includegraphics[width=\\textwidth]{plots/aaa_risk_assessment_subfigure.pdf}")
    print("        \\caption{Risk assessment}")
    print("    \\end{subfigure}")
    print("    \\hfill")
    print("    \\begin{subfigure}{0.48\\textwidth}")
    print("        \\includegraphics[width=\\textwidth]{plots/aaa_ai_validation_subfigure.pdf}")
    print("        \\caption{AI validation}")
    print("    \\end{subfigure}")
    print("    \\caption{AAA analysis results}")
    print("\\end{figure}")

if __name__ == "__main__":
    main()