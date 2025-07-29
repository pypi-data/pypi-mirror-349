from .base import Stat
import pandas as pd

class StatCount(Stat):
    """Count data points in different groups"""
    def __init__(self, data=None, mapping=None, **params):
        super().__init__(data, mapping, **params)
        
    def compute(self):
        """Count occurrences in x variable"""
        if self.data is None:
            return None
            
        x_col = self.mapping.get('x')
        if x_col is None:
            return None
            
        # Count occurrences of each unique value
        counts = self.data[x_col].value_counts().reset_index()
        counts.columns = ['x', 'count']
        counts = counts.sort_values('x')
        
        return counts
