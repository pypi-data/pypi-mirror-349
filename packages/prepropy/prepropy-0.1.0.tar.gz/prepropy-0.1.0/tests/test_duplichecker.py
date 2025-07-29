"""
Unit tests for the DupliChecker module.
"""
import unittest
import pandas as pd
from prepropy.duplichecker import drop_duplicates, get_duplicate_stats


class TestDupliChecker(unittest.TestCase):
    """Test cases for the DupliChecker module."""

    def setUp(self):
        """Set up test DataFrame with duplicates."""
        self.df = pd.DataFrame({
            'id': [1, 2, 3, 2, 4, 5, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'Bob', 'David', 'Eve', 'Eve'],
            'value': [100, 200, 150, 200, 300, 250, 250]
        })

    def test_input_validation(self):
        """Test input validation."""
        # Test non-DataFrame input
        with self.assertRaises(TypeError):
            drop_duplicates([1, 2, 3])
        
        # Test invalid keep value
        with self.assertRaises(ValueError):
            drop_duplicates(self.df, keep='invalid')
            
        # Test invalid subset column
        with self.assertRaises(ValueError):
            drop_duplicates(self.df, subset=['nonexistent_column'])

    def test_drop_duplicates_all_cols(self):
        """Test dropping duplicates considering all columns."""
        result = drop_duplicates(self.df)
        
        # Should have 5 rows (2 duplicates removed)
        self.assertEqual(len(result), 5)
        
        # First occurrences should remain
        expected_ids = [1, 2, 3, 4, 5]
        self.assertListEqual(result['id'].tolist(), expected_ids)

    def test_drop_duplicates_subset(self):
        """Test dropping duplicates considering only subset of columns."""
        # Drop duplicates based on 'name' column
        result = drop_duplicates(self.df, subset=['name'])
        
        # Should have 5 rows (Bob and Eve duplicates removed)
        self.assertEqual(len(result), 5)
        
        # Check unique names
        unique_names = result['name'].unique()
        self.assertEqual(len(unique_names), 5)
        self.assertSetEqual(set(unique_names), set(['Alice', 'Bob', 'Charlie', 'David', 'Eve']))

    def test_drop_duplicates_keep_last(self):
        """Test dropping duplicates keeping last occurrence."""
        result = drop_duplicates(self.df, keep='last')
        
        # Should still have 5 rows
        self.assertEqual(len(result), 5)
        
        # Check that the kept rows include the last occurrence of duplicate 'id's
        id_indices = {}
        for i, id_val in enumerate(self.df['id']):
            id_indices[id_val] = i
        
        # The index for id=2 should be 3 (last occurrence)
        self.assertEqual(result.loc[result['id'] == 2].index[0], 3)
        
        # The index for id=5 should be 6 (last occurrence)
        self.assertEqual(result.loc[result['id'] == 5].index[0], 6)

    def test_drop_all_duplicates(self):
        """Test dropping all duplicates (no keeps)."""
        result = drop_duplicates(self.df, keep=False)
        
        # Should have 3 rows (all duplicated rows removed)
        self.assertEqual(len(result), 3)
        
        # Only non-duplicated ids should remain
        expected_ids = [1, 3, 4]
        self.assertListEqual(result['id'].tolist(), expected_ids)

    def test_get_duplicate_stats(self):
        """Test getting statistics about duplicates."""
        stats = get_duplicate_stats(self.df)
        
        # Total count should be 7
        self.assertEqual(stats['total_count'], 7)
        
        # 2 duplicates out of 7 records (28.57%)
        self.assertEqual(stats['duplicate_count'], 2)
        self.assertAlmostEqual(stats['duplicate_percent'], 28.57, places=2)
        
        # 5 unique records
        self.assertEqual(stats['unique_count'], 5)
        
        # Test with subset
        subset_stats = get_duplicate_stats(self.df, subset=['name'])
        self.assertEqual(subset_stats['duplicate_count'], 2)


if __name__ == '__main__':
    unittest.main()
