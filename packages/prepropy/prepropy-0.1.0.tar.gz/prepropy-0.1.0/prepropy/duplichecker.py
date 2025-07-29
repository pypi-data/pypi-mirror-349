"""
DupliChecker module for handling duplicate records in DataFrames.

This module provides functionality to identify and remove duplicate 
records from pandas DataFrames with configurability.
"""
import pandas as pd


def drop_duplicates(df, subset=None, keep='first'):
    """
    Remove duplicate rows from a DataFrame with configurable options.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to remove duplicates from.
    subset : str or list of str, default None
        Column(s) to consider for identifying duplicates.
        If None, all columns are used.
    keep : {'first', 'last', False}, default 'first'
        - 'first': Keep the first occurrence of duplicates.
        - 'last': Keep the last occurrence of duplicates.
        - False: Drop all duplicates.

    Returns
    -------
    pandas.DataFrame
        DataFrame with duplicates removed.

    Raises
    ------
    TypeError
        If df is not a pandas DataFrame.
    ValueError
        If an invalid 'keep' value is provided.
        If subset columns are not found in DataFrame.
    """
    # Input validation
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")
        
    if keep not in ['first', 'last', False]:
        raise ValueError("'keep' must be one of: 'first', 'last', or False")
    
    # Validate subset columns exist in the DataFrame
    if subset is not None:
        if isinstance(subset, str):
            subset = [subset]  # Convert single column name to list
        
        missing_cols = [col for col in subset if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Columns {missing_cols} not found in DataFrame. "
                             f"Available columns: {list(df.columns)}")
    
    # Return a new DataFrame with duplicates dropped
    return df.drop_duplicates(subset=subset, keep=keep)


def get_duplicate_stats(df, subset=None):
    """
    Get statistics about duplicate records in a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to analyze for duplicates.
    subset : str or list of str, default None
        Column(s) to consider for identifying duplicates.
        If None, all columns are used.

    Returns
    -------
    dict
        Dictionary containing duplicate statistics:
        - 'duplicate_count': Number of duplicate records
        - 'duplicate_percent': Percentage of records that are duplicates
        - 'unique_count': Number of unique records
        - 'total_count': Total number of records

    Raises
    ------
    TypeError
        If df is not a pandas DataFrame.
    """
    # Input validation
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    # Handle subset validation
    if subset is not None:
        if isinstance(subset, str):
            subset = [subset]  # Convert single column name to list
        
        missing_cols = [col for col in subset if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Columns {missing_cols} not found in DataFrame. "
                             f"Available columns: {list(df.columns)}")

    # Calculate duplicate statistics
    total_count = len(df)
    unique_df = df.drop_duplicates(subset=subset)
    unique_count = len(unique_df)
    duplicate_count = total_count - unique_count
    duplicate_percent = (duplicate_count / total_count) * 100 if total_count > 0 else 0
    
    return {
        'duplicate_count': duplicate_count,
        'duplicate_percent': duplicate_percent,
        'unique_count': unique_count,
        'total_count': total_count
    }
