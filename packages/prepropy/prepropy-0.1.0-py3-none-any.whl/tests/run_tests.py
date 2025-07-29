"""
Main test runner for the PreProPy package.
"""
import unittest
import sys
import os

# Add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all test modules
from tests.test_nullsense import TestNullSense
from tests.test_duplichecker import TestDupliChecker
from tests.test_scalenpipe import TestScaleNPipe


if __name__ == '__main__':    # Create a test suite and loader
    test_suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    # Add all test classes
    test_suite.addTests(loader.loadTestsFromTestCase(TestNullSense))
    test_suite.addTests(loader.loadTestsFromTestCase(TestDupliChecker))
    test_suite.addTests(loader.loadTestsFromTestCase(TestScaleNPipe))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate status code
    sys.exit(not result.wasSuccessful())
