"""
Unit tests for the NullSense module.
"""
import unittest
import numpy as np
import pandas as pd
from prepropy.nullsense import handle_nulls


class TestNullSense(unittest.TestCase):
    """Test cases for the NullSense module."""

    def setUp(self):
        """Set up test DataFrame with missing values."""
        self.df = pd.DataFrame({
            'numeric1': [1, 2, None, 4, 5, 6, None],
            'numeric2': [10.5, None, 12.2, 13.5, None, 9.8, 8.5],
            'category1': ['A', 'B', None, 'B', 'C', None, 'A'],
            'category2': [None, 'Y', 'Z', 'Y', 'Y', 'X', None]
        })

    def test_input_validation(self):
        """Test input validation."""
        # Test non-DataFrame input
        with self.assertRaises(TypeError):
            handle_nulls([1, 2, 3])
            
        # Test invalid strategy
        with self.assertRaises(ValueError):
            handle_nulls(self.df, strategy="invalid_strategy")

    def test_auto_strategy(self):
        """Test auto strategy fills with median for numeric and mode for categorical."""
        filled_df = handle_nulls(self.df, strategy="auto")
        
        # Check numeric columns filled with median
        self.assertEqual(filled_df['numeric1'].iloc[2], 4.0)  # median of numeric1
        self.assertEqual(filled_df['numeric2'].iloc[1], 10.5)  # median of numeric2
        
        # Check categorical columns filled with mode
        self.assertEqual(filled_df['category1'].iloc[2], 'A')  # mode of category1 is 'A'
        self.assertEqual(filled_df['category2'].iloc[0], 'Y')  # mode of category2 is 'Y'
        
        # Check no nulls remain
        self.assertEqual(filled_df.isna().sum().sum(), 0)

    def test_mean_strategy(self):
        """Test mean strategy fills numeric columns with mean."""
        filled_df = handle_nulls(self.df, strategy="mean")
        
        # Check numeric columns filled with mean
        # Mean of numeric1 = (1+2+4+5+6)/5 = 3.6
        self.assertAlmostEqual(filled_df['numeric1'].iloc[2], 3.6)
        
        # Mean of numeric2 = (10.5+12.2+13.5+9.8+8.5)/5 = 10.9
        self.assertAlmostEqual(filled_df['numeric2'].iloc[1], 10.9, places=1)
        
        # Check categorical columns still have nulls
        self.assertTrue(filled_df['category1'].isna().any())
        self.assertTrue(filled_df['category2'].isna().any())

    def test_median_strategy(self):
        """Test median strategy fills numeric columns with median."""
        filled_df = handle_nulls(self.df, strategy="median")
        
        # Check numeric columns filled with median
        self.assertEqual(filled_df['numeric1'].iloc[2], 4.0)  # median of numeric1
        self.assertEqual(filled_df['numeric2'].iloc[1], 10.5)  # median of numeric2
        
        # Check categorical columns still have nulls
        self.assertTrue(filled_df['category1'].isna().any())
        self.assertTrue(filled_df['category2'].isna().any())

    def test_mode_strategy(self):
        """Test mode strategy fills all columns with mode."""
        filled_df = handle_nulls(self.df, strategy="mode")
        
        # Check all columns filled with mode
        self.assertEqual(filled_df['category1'].iloc[2], 'A')  # mode of category1
        self.assertEqual(filled_df['category2'].iloc[0], 'Y')  # mode of category2
        
        # Check no nulls remain
        self.assertEqual(filled_df.isna().sum().sum(), 0)

    def test_zero_strategy(self):
        """Test zero strategy fills numeric with 0 and categorical with ''."""
        filled_df = handle_nulls(self.df, strategy="zero")
        
        # Check numeric columns filled with 0
        self.assertEqual(filled_df['numeric1'].iloc[2], 0)
        self.assertEqual(filled_df['numeric2'].iloc[1], 0)
        
        # Check categorical columns filled with empty string
        self.assertEqual(filled_df['category1'].iloc[2], '')
        self.assertEqual(filled_df['category2'].iloc[0], '')
        
        # Check no nulls remain
        self.assertEqual(filled_df.isna().sum().sum(), 0)


if __name__ == '__main__':
    unittest.main()
