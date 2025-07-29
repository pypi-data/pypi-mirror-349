import unittest
import pandas as pd
from unittest.mock import MagicMock, patch
from ..api import PyRatioAPI

class TestPyRatioAPI(unittest.TestCase):
    def setUp(self):
        self.api = PyRatioAPI()
        self.api.query_engine.execute = MagicMock(return_value=pd.DataFrame())
        self.api.visualizer.create = MagicMock()
        
    def test_query(self):
        result = self.api.query("Show stocks with P/E < 15")
        self.assertIsInstance(result, pd.DataFrame)
        self.api.query_engine.execute.assert_called_once_with("Show stocks with P/E < 15")
        
    def test_visualize(self):
        test_df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        self.api.visualize("Scatter plot of A vs B", test_df)
        self.api.visualizer.create.assert_called_once_with("Scatter plot of A vs B", test_df)
        
    def test_export(self):
        with patch('pandas.DataFrame.to_excel') as mock_to_excel:
            self.api.export("Show stocks with P/E < 15", "test.xlsx")
            mock_to_excel.assert_called_once()