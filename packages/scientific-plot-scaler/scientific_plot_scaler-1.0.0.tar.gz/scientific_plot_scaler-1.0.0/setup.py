#!/usr/bin/env python3
"""
Setup script for Scientific Plot Scaler
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
if (this_directory / "requirements.txt").exists():
    requirements = (this_directory / "requirements.txt").read_text().strip().split('\n')
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]

setup(
    name="scientific-plot-scaler",
    version="1.0.0",
    author="Vijay Nandurdikar",
    author_email="vijaynandurdikar@gmail.com",
    description="A tool for creating publication-ready scientific plots with proper text scaling for LaTeX documents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VijayN10/scientific-plot-scaler",
    project_urls={
        "Bug Tracker": "https://github.com/VijayN10/scientific-plot-scaler/issues",
        "Documentation": "https://github.com/VijayN10/scientific-plot-scaler/wiki",
        "Source Code": "https://github.com/VijayN10/scientific-plot-scaler",
        "Changelog": "https://github.com/VijayN10/scientific-plot-scaler/blob/main/CHANGELOG.md",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords="scientific plotting latex publication matplotlib research",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.812",
            "pre-commit>=2.0",
        ],
        "examples": [
            "jupyter>=1.0",
            "pandas>=1.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "plot-scaler=scientific_plot_scaler.plot_scaler:main",
        ],
    },
    include_package_data=True,
    package_data={
        "scientific_plot_scaler": [
            "configs/*.json",
        ],
    },
    zip_safe=False,
)