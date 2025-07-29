"""
PreProPy: A Python package for data preprocessing tasks.

This package combines three core preprocessing tools:
- NullSense: Intelligent handling of missing values
- DupliChecker: Duplicate record detection and removal
- ScaleNPipe: Feature scaling and model pipeline creation

All main functions are available at the package level for easy import.
"""

# Import main functions from submodules
from .nullsense import handle_nulls
from .duplichecker import drop_duplicates, get_duplicate_stats
from .scalenpipe import scale_pipeline, get_available_scalers

# Define package metadata
__version__ = '0.1.0'
__author__ = 'PreProPy Team'

# Define what gets imported with "from prepropy import *"
__all__ = [
    'handle_nulls',
    'drop_duplicates',
    'get_duplicate_stats',
    'scale_pipeline',
    'get_available_scalers'
]

# Import CLI module for command-line execution
from . import cli
