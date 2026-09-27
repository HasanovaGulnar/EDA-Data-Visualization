# Exploratory Data Analysis & Data Visualization

## Overview

This Python project implements an exploratory
data analysis and data visualization workflow.

It is divided into two tasks:

- Task 2: Exploratory Data Analysis
- Task 3: Data Visualization

## Objectives

- Understand the dataset structure
- Identify missing values and duplicates
- Analyze descriptive statistics
- Detect potential outliers
- Explore correlations
- Test appropriate statistical hypotheses
- Create visualizations and reports

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy

## Project Structure

- data/raw: Original dataset
- data/processed: Analysis dataset
- src/eda.py: Exploratory analysis
- src/visualization.py: Visualization
- reports: Analysis report
- reports/figures: Generated charts

## Installation

Create a Python virtual environment.

Install dependencies:

pip install -r requirements.txt

## Usage

Add one CSV file to data/raw.

Run the EDA script:

python src/eda.py

Generate visualizations:

python src/visualization.py

Optional parameters:

python src/eda.py --target TARGET --group GROUP

python src/visualization.py --target TARGET --date DATE

Replace these placeholders with actual column names.

## Outputs

The project generates:

- Descriptive statistical analysis
- Missing-value summaries
- Potential outlier counts
- Correlation analysis
- Histograms
- Boxplots
- Correlation heatmaps
- Categorical visualizations
- Optional monthly trends

## Limitations

Business questions and statistical hypotheses
must be defined for the selected dataset.

Outliers are flagged, not automatically removed.

Correlation does not establish causation.

## Author

Gulnar Hasanova
