# filepath: /home/essi/Documents/gitlab/ggly/src/ggly/stats/base.py
import pandas as pd
import numpy as np

class Stat:
    """Base class for statistical transformations"""
    def __init__(self, data=None, mapping=None, **params):
        self.data = data
        self.mapping = mapping or {}
        self.params = params
        
    def compute(self):
        """Perform the statistical transformation on the data"""
        raise NotImplementedError