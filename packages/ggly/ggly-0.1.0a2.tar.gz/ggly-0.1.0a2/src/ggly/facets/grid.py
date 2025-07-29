from .base import Facet
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class FacetGrid(Facet):
    """Facet grid implementation similar to ggplot2's facet_grid"""
    def __init__(self, rows=None, cols=None, scales="fixed"):
        super().__init__()
        self.row_vars = [rows] if isinstance(rows, str) else (rows or [])
        self.col_vars = [cols] if isinstance(cols, str) else (cols or [])
        self.scales = scales
        
    def create_facets(self, data):
        """Group data by facet variables (rows and columns)"""
        # Create combined row and column keys
        if self.row_vars:
            data['_row_key'] = data.apply(lambda x: ' / '.join(str(x[v]) for v in self.row_vars), axis=1)
        else:
            data['_row_key'] = '1'  # single row
            
        if self.col_vars:
            data['_col_key'] = data.apply(lambda x: ' / '.join(str(x[v]) for v in self.col_vars), axis=1)
        else:
            data['_col_key'] = '1'  # single column
            
        # Group by both row and column
        grouped = data.groupby(['_row_key', '_col_key'])
        
        return grouped
        
    def apply(self, fig, data, layers):
        """Apply facet_grid to create a grid of subplots"""
        # Group data by facet rows and columns
        grouped = self.create_facets(data)
        
        # Get unique row and column values
        row_values = sorted(set(k[0] for k in grouped.groups.keys()))
        col_values = sorted(set(k[1] for k in grouped.groups.keys()))
        
        n_rows = len(row_values)
        n_cols = len(col_values)
        
        # Create row and column titles
        row_titles = self._get_row_titles(row_values)
        col_titles = self._get_col_titles(col_values)
        
        # Create subplots
        fig = make_subplots(
            rows=n_rows,
            cols=n_cols,
            shared_xaxes='all' if self.scales in ["fixed", "free_y"] else False,
            shared_yaxes='all' if self.scales in ["fixed", "free_x"] else False,
            row_titles=row_titles if self.row_vars else None,
            column_titles=col_titles if self.col_vars else None,
        )
        
        # Add traces to subplots
        row_map = {val: i + 1 for i, val in enumerate(row_values)}
        col_map = {val: i + 1 for i, val in enumerate(col_values)}
        
        # Correction : n'afficher chaque légende de couleur qu'une seule fois
        legend_shown = set()
        for (row_key, col_key), group in grouped:
            row = row_map[row_key]
            col = col_map[col_key]
            for layer in layers:
                facet_layer = layer.__class__(group, layer.mapping, **layer.params)
                trace = facet_layer.to_trace()
                # Si la trace est une liste (plusieurs catégories)
                if isinstance(trace, list):
                    for t in trace:
                        # On tente d'utiliser t.name comme clé de légende
                        legend_key = getattr(t, 'name', None)
                        if legend_key and legend_key not in legend_shown:
                            t.showlegend = True
                            legend_shown.add(legend_key)
                        else:
                            t.showlegend = False
                        fig.add_trace(t, row=row, col=col)
                else:
                    legend_key = getattr(trace, 'name', None)
                    if legend_key and legend_key not in legend_shown:
                        trace.showlegend = True
                        legend_shown.add(legend_key)
                    else:
                        trace.showlegend = False
                    fig.add_trace(trace, row=row, col=col)
        
        # Update layout for uniform appearance
        fig.update_layout(showlegend=True)
        
        return fig
    
    def _get_row_titles(self, row_values):
        """Generate titles for rows"""
        if not self.row_vars:
            return None
        if len(self.row_vars) == 1:
            var_name = self.row_vars[0]
            return [f"{var_name}: {val}" for val in row_values]
        else:
            return row_values
            
    def _get_col_titles(self, col_values):
        """Generate titles for columns"""
        if not self.col_vars:
            return None
        if len(self.col_vars) == 1:
            var_name = self.col_vars[0]
            return [f"{var_name}: {val}" for val in col_values]
        else:
            return col_values