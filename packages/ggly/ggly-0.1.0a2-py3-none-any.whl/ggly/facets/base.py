import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Facet:
    """Base class for facet layouts"""
    def __init__(self):
        self.facet_vars = []
        self.scales = "fixed"  # "fixed", "free", "free_x", "free_y"
        
    def create_facets(self, data, mapping):
        """Create facet groups from data"""
        raise NotImplementedError
        
    def apply(self, fig, layers):
        """Apply faceting to figure, creating subplots"""
        raise NotImplementedError
        
    def _get_subplot_titles(self, facet_data):
        """Generate titles for subplots based on facet variables"""
        raise NotImplementedError