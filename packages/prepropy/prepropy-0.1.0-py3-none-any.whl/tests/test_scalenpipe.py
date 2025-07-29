"""
Unit tests for the ScaleNPipe module.
"""
import unittest
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from prepropy.scalenpipe import scale_pipeline, get_available_scalers


class TestScaleNPipe(unittest.TestCase):
    """Test cases for the ScaleNPipe module."""

    def setUp(self):
        """Set up test model and data."""
        self.model = LogisticRegression(random_state=42)
        self.X = np.array([[-1, 2], [-0.5, 6], [0, 10], [1, 18], [2, 20]])
        self.y = np.array([0, 0, 0, 1, 1])

    def test_input_validation(self):
        """Test input validation."""
        # Test non-model input (no fit method)
        with self.assertRaises(TypeError):
            scale_pipeline({"not_a_model": True})
            
        # Test invalid scaler type
        with self.assertRaises(ValueError):
            scale_pipeline(self.model, scaler="invalid_scaler")

    def test_standard_scaler_pipeline(self):
        """Test creating pipeline with StandardScaler."""
        pipeline = scale_pipeline(self.model, scaler="standard")
        
        # Check pipeline structure
        self.assertIsInstance(pipeline, Pipeline)
        self.assertEqual(len(pipeline.steps), 2)
        self.assertEqual(pipeline.steps[0][0], 'scaler')
        self.assertEqual(pipeline.steps[1][0], 'model')
        
        # Check scaler type
        self.assertIsInstance(pipeline.steps[0][1], StandardScaler)
        
        # Check if pipeline works
        pipeline.fit(self.X, self.y)
        score = pipeline.score(self.X, self.y)
        self.assertGreaterEqual(score, 0)  # Simple check that it runs

    def test_minmax_scaler_pipeline(self):
        """Test creating pipeline with MinMaxScaler."""
        pipeline = scale_pipeline(self.model, scaler="minmax")
        
        # Check scaler type
        self.assertIsInstance(pipeline.steps[0][1], MinMaxScaler)
        
        # Check if pipeline works
        pipeline.fit(self.X, self.y)
        score = pipeline.score(self.X, self.y)
        self.assertGreaterEqual(score, 0)

    def test_robust_scaler_pipeline(self):
        """Test creating pipeline with RobustScaler."""
        pipeline = scale_pipeline(self.model, scaler="robust")
        
        # Check scaler type
        self.assertIsInstance(pipeline.steps[0][1], RobustScaler)
        
        # Check if pipeline works
        pipeline.fit(self.X, self.y)
        score = pipeline.score(self.X, self.y)
        self.assertGreaterEqual(score, 0)

    def test_default_scaler(self):
        """Test default scaler (standard)."""
        pipeline = scale_pipeline(self.model)  # No scaler specified
        self.assertIsInstance(pipeline.steps[0][1], StandardScaler)

    def test_get_available_scalers(self):
        """Test getting available scalers info."""
        scalers = get_available_scalers()
        
        # Check all expected scalers are returned
        self.assertIn('standard', scalers)
        self.assertIn('minmax', scalers)
        self.assertIn('robust', scalers)
        
        # Check descriptions are provided
        self.assertIn('StandardScaler', scalers['standard'])
        self.assertIn('MinMaxScaler', scalers['minmax'])
        self.assertIn('RobustScaler', scalers['robust'])


if __name__ == '__main__':
    unittest.main()
