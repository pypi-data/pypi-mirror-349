"""
Command-line interface for the PreProPy package.

This module provides a simple command-line interface to run PreProPy functions.
"""
import argparse
import sys
import pandas as pd
import json
from sklearn.linear_model import LogisticRegression
import warnings

# Import package functions
from prepropy import (
    handle_nulls,
    drop_duplicates,
    get_duplicate_stats,
    scale_pipeline,
    get_available_scalers
)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='PreProPy: A preprocessing toolkit for Python.')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # NullSense command
    parser_nulls = subparsers.add_parser('nulls', help='Handle missing values')
    parser_nulls.add_argument('input_file', help='Input CSV file path')
    parser_nulls.add_argument('output_file', help='Output CSV file path')
    parser_nulls.add_argument(
        '--strategy', choices=['auto', 'mean', 'median', 'mode', 'zero'],
        default='auto', help='Strategy to fill nulls'
    )
    
    # DupliChecker command
    parser_dups = subparsers.add_parser('dups', help='Handle duplicates')
    parser_dups.add_argument('input_file', help='Input CSV file path')
    parser_dups.add_argument('output_file', help='Output CSV file path')
    parser_dups.add_argument(
        '--subset', help='Comma-separated list of columns to consider', default=None
    )
    parser_dups.add_argument(
        '--keep', choices=['first', 'last', 'none'], default='first',
        help="Which duplicates to keep ('none' for dropping all)"
    )
    parser_dups.add_argument(
        '--stats-only', action='store_true',
        help='Only show duplicate statistics, do not modify data'
    )
    
    # ScaleNPipe command (just show available scalers)
    parser_scale = subparsers.add_parser('scale', help='Scaling information')
    parser_scale.add_argument(
        '--list-scalers', action='store_true', 
        help='List available scalers'
    )
    
    return parser.parse_args()


def handle_nulls_command(args):
    """Run the NullSense handle_nulls command."""
    try:
        # Load data
        df = pd.read_csv(args.input_file)
        
        # Handle nulls
        filled_df = handle_nulls(df, strategy=args.strategy)
        
        # Save result
        filled_df.to_csv(args.output_file, index=False)
        
        # Print summary
        null_before = df.isna().sum().sum()
        null_after = filled_df.isna().sum().sum()
        print(f"Missing values before: {null_before}")
        print(f"Missing values after: {null_after}")
        print(f"Results saved to {args.output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def handle_dups_command(args):
    """Run the DupliChecker command."""
    try:
        # Load data
        df = pd.read_csv(args.input_file)
        
        # Parse subset
        subset = args.subset.split(',') if args.subset else None
        
        # Get stats
        stats = get_duplicate_stats(df, subset=subset)
        print("Duplicate Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # If stats only, exit
        if args.stats_only:
            return
        
        # Handle keep parameter
        keep = args.keep if args.keep != 'none' else False
        
        # Drop duplicates
        result_df = drop_duplicates(df, subset=subset, keep=keep)
        
        # Save result
        result_df.to_csv(args.output_file, index=False)
        print(f"Results saved to {args.output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def handle_scale_command(args):
    """Run the ScaleNPipe command."""
    if args.list_scalers:
        scalers = get_available_scalers()
        print("Available scalers:")
        for name, desc in scalers.items():
            print(f"  {name}: {desc}")


def main():
    """Main entry point for the command-line interface."""
    # Filter out certain warnings
    warnings.filterwarnings('ignore', category=UserWarning)
    
    # Parse arguments
    args = parse_arguments()
    
    # Run appropriate command
    if args.command == 'nulls':
        handle_nulls_command(args)
    elif args.command == 'dups':
        handle_dups_command(args)
    elif args.command == 'scale':
        handle_scale_command(args)
    else:
        print("Please specify a command. Use -h for help.")
        sys.exit(1)


if __name__ == '__main__':
    main()
