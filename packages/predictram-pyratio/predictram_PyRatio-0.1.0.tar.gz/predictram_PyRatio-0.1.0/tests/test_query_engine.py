import unittest
import pandas as pd
from unittest.mock import MagicMock
from ..query_engine import QueryEngine
from ..data_loader import DataLoader

class TestQueryEngine(unittest.TestCase):
    def setUp(self):
        mock_loader = MagicMock(spec=DataLoader)
        mock_loader.df = pd.DataFrame({
            'trailingPE': [10, 20, 30],
            'returnOnEquity': [0.15, 0.25, 0.35],
            'industry': ['Tech', 'Finance', 'Tech']
        })
        self.engine = QueryEngine(mock_loader)
        
    def test_parse_query_simple(self):
        conditions = self.engine._parse_query("Show stocks with trailingPE < 20")
        self.assertEqual(len(conditions), 1)
        self.assertEqual(conditions[0]['metric'], 'trailingPE')
        self.assertEqual(conditions[0]['operator'], '<')
        self.assertEqual(conditions[0]['value'], 20)
        
    def test_parse_query_multiple(self):
        conditions = self.engine._parse_query(
            "Show stocks with trailingPE < 20 and returnOnEquity > 0.20"
        )
        self.assertEqual(len(conditions), 2)
        
    def test_apply_conditions(self):
        conditions = [{'metric': 'trailingPE', 'operator': '<', 'value': 25}]
        result = self.engine._apply_conditions(conditions)
        self.assertEqual(len(result), 2)  # Should include 10 and 20
        
    def test_normalize_metric(self):
        self.assertEqual(self.engine._normalize_metric("P/E Ratio"), "trailingPE")
        self.assertEqual(self.engine._normalize_metric("trailingPE"), "trailingPE")