"""
NullSense module for intelligent handling of missing values.

This module provides functionality to identify and fill missing values
in pandas DataFrames based on column types.
"""
import pandas as pd
import numpy as np


def handle_nulls(df, strategy="auto"):
    """
    Intelligently fills missing values based on column data types.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing missing values to fill.
    strategy : str, default="auto"
        Strategy to use for filling missing values:
        - "auto": Use mean/median for numeric columns and mode for categorical
        - "mean": Use mean for numeric columns
        - "median": Use median for numeric columns
        - "mode": Use mode for all columns
        - "zero": Fill with zeros for numeric columns and empty string for categorical

    Returns
    -------
    pandas.DataFrame
        A DataFrame with missing values filled according to the strategy.

    Raises
    ------
    TypeError
        If df is not a pandas DataFrame.
    ValueError
        If an invalid strategy is provided.
    """
    # Input validation
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")
        
    if strategy not in ["auto", "mean", "median", "mode", "zero"]:
        raise ValueError("Invalid strategy. Choose from: 'auto', 'mean', 'median', 'mode', 'zero'")
    
    # Create a copy of the DataFrame to avoid modifying the original
    result_df = df.copy()
    
    # Get numeric and categorical columns
    numeric_cols = result_df.select_dtypes(include=['number']).columns
    categorical_cols = result_df.select_dtypes(exclude=['number']).columns
    
    # Handle missing values based on strategy
    if strategy == "auto":
        # For numeric columns: fill with median
        for col in numeric_cols:
            if result_df[col].isna().any():
                result_df[col] = result_df[col].fillna(result_df[col].median())
        
        # For categorical columns: fill with mode
        for col in categorical_cols:
            if result_df[col].isna().any():
                mode_value = result_df[col].mode()[0] if not result_df[col].mode().empty else ""
                result_df[col] = result_df[col].fillna(mode_value)
    
    elif strategy == "mean":
        # Fill numeric columns with mean
        for col in numeric_cols:
            if result_df[col].isna().any():
                result_df[col] = result_df[col].fillna(result_df[col].mean())
                
    elif strategy == "median":
        # Fill numeric columns with median
        for col in numeric_cols:
            if result_df[col].isna().any():
                result_df[col] = result_df[col].fillna(result_df[col].median())
    
    elif strategy == "mode":
        # Fill all columns with their mode
        for col in result_df.columns:
            if result_df[col].isna().any():
                mode_value = result_df[col].mode()[0] if not result_df[col].mode().empty else ""
                result_df[col] = result_df[col].fillna(mode_value)
    
    elif strategy == "zero":
        # Fill numeric columns with 0
        for col in numeric_cols:
            if result_df[col].isna().any():
                result_df[col] = result_df[col].fillna(0)
        
        # Fill categorical columns with empty string
        for col in categorical_cols:
            if result_df[col].isna().any():
                result_df[col] = result_df[col].fillna("")
    
    return result_df
