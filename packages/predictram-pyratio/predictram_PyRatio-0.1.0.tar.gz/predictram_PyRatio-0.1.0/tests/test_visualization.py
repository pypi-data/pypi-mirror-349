import unittest
import pandas as pd
import matplotlib.pyplot as plt
from ..visualization import Visualizer

class TestVisualizer(unittest.TestCase):
    def setUp(self):
        self.viz = Visualizer()
        self.test_data = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'Category': ['X', 'Y', 'X']
        })
        
    def test_scatter_plot(self):
        fig = self.viz._create_scatter_plot("A vs B", self.test_data)
        self.assertIsInstance(fig, plt.Figure)
        plt.close(fig)
        
    def test_bar_plot(self):
        fig = self.viz._create_bar_plot("Bar of A", self.test_data)
        self.assertIsInstance(fig, plt.Figure)
        plt.close(fig)
        
    def test_extract_axes(self):
        x, y = self.viz._extract_axes("scatter of A and B")
        self.assertEqual(x, 'A')
        self.assertEqual(y, 'B')