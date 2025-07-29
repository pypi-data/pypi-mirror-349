# filepath: /home/essi/Documents/gitlab/ggly/src/ggly/facets/wrap.py
from .base import Facet
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

class FacetWrap(Facet):
    """Facet wrap implementation similar to ggplot2's facet_wrap"""
    def __init__(self, facets, nrow=None, ncol=None, scales="fixed"):
        super().__init__()
        self.facet_vars = [facets] if isinstance(facets, str) else facets
        self.nrow = nrow
        self.ncol = ncol
        self.scales = scales
        
    def create_facets(self, data):
        """Group data by facet variables"""
        # Group the data by facet variables
        if len(self.facet_vars) == 1:
            grouped = data.groupby(self.facet_vars[0])
        else:
            # For multiple facet variables, combine them
            data['_facet_key'] = data.apply(lambda x: ' ~ '.join(str(x[v]) for v in self.facet_vars), axis=1)
            grouped = data.groupby('_facet_key')
            
        return grouped
        
    def apply(self, fig, data, layers):
        """Apply facet_wrap to create a grid of subplots"""
        # Group data by facet
        grouped = self.create_facets(data)
        group_names = list(grouped.groups.keys())
        
        # Determine grid dimensions
        n_facets = len(group_names)
        if self.ncol is None and self.nrow is None:
            # Default: square-ish grid
            self.ncol = math.ceil(math.sqrt(n_facets))
            self.nrow = math.ceil(n_facets / self.ncol)
        elif self.ncol is None:
            self.ncol = math.ceil(n_facets / self.nrow)
        elif self.nrow is None:
            self.nrow = math.ceil(n_facets / self.ncol)
        
        # Create subplot titles
        titles = self._get_subplot_titles(group_names)
        
        # Create subplots
        fig = make_subplots(
            rows=self.nrow,
            cols=self.ncol,
            subplot_titles=titles,
            shared_xaxes='all' if self.scales in ["fixed", "free_y"] else False,
            shared_yaxes='all' if self.scales in ["fixed", "free_x"] else False,
        )
        
        # Add traces to subplots
        for i, (name, group) in enumerate(grouped):
            row = i // self.ncol + 1
            col = i % self.ncol + 1
            
            # Apply each layer to this facet's data
            for layer in layers:
                # Create a new instance of the layer with this facet's data
                facet_layer = layer.__class__(group, layer.mapping, **layer.params)
                trace = facet_layer.to_trace()
                
                # Handle case when multiple traces are returned (e.g., from grouped boxplots)
                if isinstance(trace, list):
                    for t in trace:
                        fig.add_trace(t, row=row, col=col)
                else:
                    fig.add_trace(trace, row=row, col=col)
        
        # Update layout for uniform appearance
        fig.update_layout(showlegend=True)
        
        return fig
    
    def _get_subplot_titles(self, group_names):
        """Generate titles for each facet"""
        if len(self.facet_vars) == 1:
            var_name = self.facet_vars[0]
            return [f"{var_name}: {name}" for name in group_names]
        else:
            return group_names