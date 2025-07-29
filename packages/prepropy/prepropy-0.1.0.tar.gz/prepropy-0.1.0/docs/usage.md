# PreProPy Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [NullSense](#nullsense)
4. [DupliChecker](#duplichecker)
5. [ScaleNPipe](#scalenpipe)
6. [Command Line Interface](#command-line-interface)
7. [Advanced Usage](#advanced-usage)
8. [API Reference](#api-reference)

## Introduction

PreProPy is a Python package that combines three essential preprocessing tools for data science and machine learning workflows:

- **NullSense**: Intelligent handling of missing values based on column types
- **DupliChecker**: Duplicate record detection and removal with configurable options
- **ScaleNPipe**: Feature scaling and model pipeline creation

The package is designed to streamline the data preprocessing phase of your projects, making it easy to prepare your data for modeling.

## Installation

Install PreProPy using pip:

```bash
pip install prepropy
```

### Requirements
- Python 3.7+
- pandas >= 1.0.0
- scikit-learn >= 0.24.0

## NullSense

NullSense provides intelligent handling of missing values in pandas DataFrames.

### `handle_nulls`

The main function in NullSense is `handle_nulls`, which fills missing values based on column types:

```python
from prepropy import handle_nulls

# Fill missing values using the default 'auto' strategy
df_filled = handle_nulls(df)

# Using different strategies
df_mean = handle_nulls(df, strategy="mean")  # Fill numeric with mean
df_median = handle_nulls(df, strategy="median")  # Fill numeric with median
df_mode = handle_nulls(df, strategy="mode")  # Fill all columns with mode
df_zero = handle_nulls(df, strategy="zero")  # Fill numeric with 0, categorical with ""
```

#### Parameters

- `df`: pandas DataFrame with missing values
- `strategy`: Strategy to use for filling missing values
  - `"auto"` (default): Mean/median for numeric, mode for categorical
  - `"mean"`: Fill numeric columns with mean
  - `"median"`: Fill numeric columns with median
  - `"mode"`: Fill all columns with mode
  - `"zero"`: Fill numeric with 0, categorical with empty string

#### Returns

A new DataFrame with missing values filled according to the strategy.

## DupliChecker

DupliChecker helps you identify and remove duplicate records from your datasets.

### `drop_duplicates`

This function removes duplicate rows with configurable options:

```python
from prepropy import drop_duplicates

# Drop duplicates considering all columns
df_unique = drop_duplicates(df)

# Drop duplicates based on specific columns
df_unique_subset = drop_duplicates(df, subset=['column1', 'column2'])

# Keep the last occurrence instead of first
df_unique_last = drop_duplicates(df, keep='last')

# Drop all duplicates
df_no_dups = drop_duplicates(df, keep=False)
```

#### Parameters

- `df`: pandas DataFrame to remove duplicates from
- `subset`: Column(s) to consider for identifying duplicates (defaults to all columns)
- `keep`: Which duplicates to keep
  - `'first'` (default): Keep the first occurrence
  - `'last'`: Keep the last occurrence
  - `False`: Drop all duplicates

#### Returns

A new DataFrame with duplicates removed according to the parameters.

### `get_duplicate_stats`

This function provides statistics about duplicate records:

```python
from prepropy import get_duplicate_stats

# Get duplicate statistics
stats = get_duplicate_stats(df)
print(stats)
# {'duplicate_count': 5, 'duplicate_percent': 10.0, 'unique_count': 45, 'total_count': 50}

# Get statistics based on specific columns
stats_subset = get_duplicate_stats(df, subset=['column1', 'column2'])
```

#### Parameters

- `df`: pandas DataFrame to analyze
- `subset`: Column(s) to consider for identifying duplicates (defaults to all columns)

#### Returns

Dictionary with duplicate statistics:
- `duplicate_count`: Number of duplicate records
- `duplicate_percent`: Percentage of duplicates
- `unique_count`: Number of unique records
- `total_count`: Total number of records

## ScaleNPipe

ScaleNPipe helps create scikit-learn pipelines with feature scaling and your model.

### `scale_pipeline`

This function creates a scikit-learn pipeline with the chosen scaler and your model:

```python
from sklearn.linear_model import LogisticRegression
from prepropy import scale_pipeline

# Create a model
model = LogisticRegression()

# Create pipelines with different scalers
std_pipeline = scale_pipeline(model, scaler="standard")
minmax_pipeline = scale_pipeline(model, scaler="minmax")
robust_pipeline = scale_pipeline(model, scaler="robust")

# Use the pipeline
std_pipeline.fit(X_train, y_train)
predictions = std_pipeline.predict(X_test)
```

#### Parameters

- `model`: scikit-learn estimator to use after scaling
- `scaler`: Type of scaler to use
  - `"standard"` (default): StandardScaler (mean=0, std=1)
  - `"minmax"`: MinMaxScaler (range 0-1)
  - `"robust"`: RobustScaler (robust to outliers)

#### Returns

A scikit-learn Pipeline with the chosen scaler and model.

### `get_available_scalers`

This function returns information about available scalers:

```python
from prepropy import get_available_scalers

scalers = get_available_scalers()
print(scalers)
```

#### Returns

Dictionary with scaler names and descriptions.

## Command Line Interface

PreProPy provides a command-line interface to run its functions:

### Handling Missing Values

```bash
prepropy nulls input.csv output.csv --strategy auto
```

### Handling Duplicates

```bash
prepropy dups input.csv output.csv --subset col1,col2 --keep first
```

To get just the statistics:

```bash
prepropy dups input.csv output.csv --stats-only
```

### List Available Scalers

```bash
prepropy scale --list-scalers
```

## Advanced Usage

### Complete ML Workflow

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from prepropy import handle_nulls, drop_duplicates, scale_pipeline

# Load data
df = pd.read_csv('data.csv')

# Handle missing values
df_filled = handle_nulls(df, strategy='auto')

# Remove duplicates
df_unique = drop_duplicates(df_filled)

# Prepare features and target
X = df_unique[['feature1', 'feature2', 'feature3']]
y = df_unique['target']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create model
model = LogisticRegression()

# Create pipeline with scaling
pipeline = scale_pipeline(model, scaler='standard')

# Train model
pipeline.fit(X_train, y_train)

# Make predictions
predictions = pipeline.predict(X_test)
```

## API Reference

### NullSense Module

- `handle_nulls(df, strategy="auto")`

### DupliChecker Module

- `drop_duplicates(df, subset=None, keep='first')`
- `get_duplicate_stats(df, subset=None)`

### ScaleNPipe Module

- `scale_pipeline(model, scaler="standard")`
- `get_available_scalers()`
