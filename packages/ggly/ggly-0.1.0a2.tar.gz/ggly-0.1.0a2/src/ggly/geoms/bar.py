# filepath: /home/essi/Documents/gitlab/ggly/src/ggly/geoms/bar.py
from .base import Geom
import plotly.graph_objects as go
import pandas as pd
from ..utils.colors import get_color_for_category

class GeomBar(Geom):
    """Bar chart geom for creating bar plots.
    
    This geom creates bar charts, supporting both counting (stat='count')
    and identity (stat='identity') modes.
    """
    def to_trace(self):
        if self.stat == 'count':
            return self._create_count_trace()
        else:  # identity
            # For identity mode, leverage the base class's categorical aesthetic handling
            return super().to_trace()
    
    def _create_count_trace(self):
        """Create a bar chart that counts occurrences (like ggplot2's geom_bar)"""
        x = self._resolve_aesthetic('x')
        fill = self._resolve_aesthetic('fill')
        color = self._resolve_aesthetic('color')
        alpha = self._resolve_aesthetic('alpha', 1.0)
        
        # Count occurrences of each x value
        if fill is not None:
            # For stacked or grouped bars
            counts = pd.crosstab(x, fill)
            traces = []
            
            # Choose between stacked and grouped
            position = self.position or 'stack'
            barmode = 'stack' if position == 'stack' else 'group'
            
            for i, col in enumerate(counts.columns):
                marker = {}
                marker['color'] = get_color_for_category(col, i, self.params.get('palette'))
                
                if alpha != 1.0:
                    marker['opacity'] = alpha
                
                # Use fill for different colors
                trace = go.Bar(
                    x=counts.index,
                    y=counts[col],
                    name=str(col),
                    marker=marker,
                )
                traces.append(trace)
            
            # Return multiple traces
            return traces
        else:
            # Simple count
            counts = x.value_counts().sort_index()
            
            marker = {}
            if color is not None:
                marker['color'] = color
            else:
                # Use a default color
                marker['color'] = get_color_for_category("default", 0, self.params.get('palette'))
                
            if alpha != 1.0:
                marker['opacity'] = alpha
            
            return go.Bar(
                x=counts.index,
                y=counts.values,
                name=self.params.get('name', ''),
                marker=marker
            )
    
    def create_trace(self, x=None, y=None, color=None, fill_color=None, alpha=None, label=None, **kwargs):
        """Create a bar trace with the given aesthetics (for stat='identity')"""
        # Use the provided values or resolve from aesthetics
        x = x if x is not None else self._resolve_aesthetic('x')
        y = y if y is not None else self._resolve_aesthetic('y')
        color = color if color is not None else self._resolve_aesthetic('color')
        fill_color = fill_color if fill_color is not None else self._resolve_aesthetic('fill_color', color)
        alpha = alpha if alpha is not None else self._resolve_aesthetic('alpha', 1.0)
        label = label if label is not None else self._resolve_aesthetic('label')
        
        marker = {}
        
        # Handle the color aesthetic
        if color is not None:
            if isinstance(color, pd.Series) and pd.api.types.is_numeric_dtype(color):
                # For numeric data, use a colorscale
                marker['color'] = color
                marker['colorscale'] = self.params.get('colorscale', 'Viridis')
                marker['showscale'] = True
            else:
                # For a single color or non-numeric array
                marker['color'] = color
        
        # Prefer fill_color over color for bars if specified
        if fill_color is not None:
            marker['color'] = fill_color
            
        # Add opacity if needed
        if alpha is not None and alpha != 1.0:
            marker['opacity'] = alpha
            
        return go.Bar(
            x=x,
            y=y,
            name=label,
            marker=marker,
            hoverinfo=self.params.get('hoverinfo', 'all')
        )