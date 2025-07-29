"""
ScaleNPipe module for creating sklearn pipelines with scaling.

This module provides functionality to create scikit-learn pipelines 
that include feature scaling followed by a model.
"""
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler


def scale_pipeline(model, scaler="standard"):
    """
    Create a scikit-learn pipeline with the chosen scaler followed by the user-provided model.

    Parameters
    ----------
    model : estimator object
        The scikit-learn estimator to use after scaling.
    scaler : {'standard', 'minmax', 'robust'}, default='standard'
        Type of scaler to use:
        - 'standard': StandardScaler (mean=0, std=1)
        - 'minmax': MinMaxScaler (range 0-1)
        - 'robust': RobustScaler (uses median and quantiles, robust to outliers)

    Returns
    -------
    sklearn.pipeline.Pipeline
        A scikit-learn Pipeline with the chosen scaler and model.

    Raises
    ------
    ValueError
        If an invalid scaler type is specified.
    TypeError
        If model doesn't have fit and predict methods.
    """
    # Validate model has fit and predict methods
    if not (hasattr(model, 'fit') and hasattr(model, 'predict')):
        raise TypeError("Model must have 'fit' and 'predict' methods")

    # Choose the appropriate scaler
    if scaler == "standard":
        scaler_obj = StandardScaler()
    elif scaler == "minmax":
        scaler_obj = MinMaxScaler()
    elif scaler == "robust":
        scaler_obj = RobustScaler()
    else:
        raise ValueError("Invalid scaler type. Choose from: 'standard', 'minmax', or 'robust'")

    # Create and return the pipeline
    return Pipeline([
        ('scaler', scaler_obj),
        ('model', model)
    ])


def get_available_scalers():
    """
    Get information about available scalers in the module.

    Returns
    -------
    dict
        Dictionary with scaler names as keys and their descriptions as values.
    """
    return {
        'standard': "StandardScaler: Standardize features by removing the mean and scaling to unit variance",
        'minmax': "MinMaxScaler: Scale features to a given range, default 0-1",
        'robust': "RobustScaler: Scale features using statistics that are robust to outliers"
    }
