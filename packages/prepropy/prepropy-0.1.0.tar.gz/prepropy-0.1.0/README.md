# PreProPy

A Python package combining three essential preprocessing tools: NullSense, DupliChecker, and ScaleNPipe.

## Installation

```bash
pip install prepropy
```

## Features

PreProPy provides three core components:

### 1. NullSense

Intelligently handle missing values in your data based on column types:

```python
import pandas as pd
from prepropy import handle_nulls

# Create a sample dataframe with missing values
df = pd.DataFrame({
    'numeric': [1, 2, None, 4, 5],
    'categorical': ['A', 'B', None, 'B', 'C']
})

# Fill missing values with intelligent defaults
df_filled = handle_nulls(df, strategy="auto")
# Numeric columns filled with median, categorical with mode

# Other available strategies
df_mean = handle_nulls(df, strategy="mean")  # Fill numeric with mean
df_median = handle_nulls(df, strategy="median")  # Fill numeric with median
df_mode = handle_nulls(df, strategy="mode")  # Fill all columns with mode
df_zero = handle_nulls(df, strategy="zero")  # Fill numeric with 0, categorical with ""
```

### 2. DupliChecker

Identify and remove duplicate records with configurable options:

```python
import pandas as pd
from prepropy import drop_duplicates, get_duplicate_stats

# Create a sample dataframe with duplicates
df = pd.DataFrame({
    'A': [1, 2, 2, 3, 3],
    'B': ['x', 'y', 'y', 'z', 'z']
})

# Get duplicate statistics
stats = get_duplicate_stats(df)
print(stats)
# Output: {'duplicate_count': 2, 'duplicate_percent': 40.0, 'unique_count': 3, 'total_count': 5}

# Drop duplicates (keeping first occurrence)
df_unique = drop_duplicates(df)

# Drop duplicates based on specific columns
df_unique_subset = drop_duplicates(df, subset=['B'])

# Keep the last occurrence instead of first
df_unique_last = drop_duplicates(df, keep='last')

# Drop all duplicates
df_no_dups = drop_duplicates(df, keep=False)
```

### 3. ScaleNPipe

Create scikit-learn pipelines with feature scaling and your model:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from prepropy import scale_pipeline, get_available_scalers

# Load sample data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create a model
model = LogisticRegression()

# Create a pipeline with standard scaling
pipeline = scale_pipeline(model, scaler="standard")

# Train the pipeline
pipeline.fit(X_train, y_train)

# Make predictions
predictions = pipeline.predict(X_test)

# See available scalers
scalers = get_available_scalers()
print(scalers)
```

## Requirements

- pandas >= 1.0.0
- scikit-learn >= 0.24.0

## License

MIT

---

Made with ❤️ by the PreProPy Team
