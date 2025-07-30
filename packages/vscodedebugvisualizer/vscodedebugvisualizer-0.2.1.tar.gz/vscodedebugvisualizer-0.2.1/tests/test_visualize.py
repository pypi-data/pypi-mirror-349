import unittest
import numpy as np
import pandas as pd
from vscodedebugvisualizer import Visualize, globalVisualizationFactory

class TestVisualizeFactory(unittest.TestCase):
    def test_add_visualizer(self):
        """Test adding a custom visualizer to the factory"""
        class MockVisualizer:
            def checkType(self, t):
                return isinstance(t, str)
                
            def visualize(self, data):
                return '{"kind": {"text": true}, "text": "' + data + '"}'
        
        # Create a new factory to avoid affecting the global one
        factory = globalVisualizationFactory
        mock_visualizer = MockVisualizer()
        factory.addVisualizer(mock_visualizer)
        
        # Check if visualizer was added
        self.assertIn(mock_visualizer, factory.visualizers)
        
        # Test visualization
        result = factory.visualize("test string")
        self.assertIsNotNone(result)
        self.assertIn("test string", result)

class TestBuiltinVisualizers(unittest.TestCase):
    def test_numpy_visualizer(self):
        """Test visualization of numpy arrays"""
        arr = np.array([[1, 2, 3], [4, 5, 6]])
        result = globalVisualizationFactory.visualize(arr)
        self.assertIsNotNone(result)
        # Basic check that it returns a JSON string
        self.assertTrue(result.startswith('{'))
        self.assertTrue(result.endswith('}'))
    
    def test_dataframe_visualizer(self):
        """Test visualization of pandas DataFrames"""
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        result = globalVisualizationFactory.visualize(df)
        self.assertIsNotNone(result)
        # Basic check that it returns a JSON string
        self.assertTrue(result.startswith('{'))
        self.assertTrue(result.endswith('}'))

if __name__ == '__main__':
    unittest.main()
