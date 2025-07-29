# filepath: /home/essi/Documents/gitlab/ggly/src/ggly/geoms/line.py
from .base import Geom
import plotly.graph_objects as go
import pandas as pd

class GeomLine(Geom):
    """Line plot geom for creating connected lines.
    
    This geom creates a line plot, optionally mapping aesthetics
    like color, size (line width), and linetype to variables in the data.
    """
    # No need to override to_trace as the base implementation handles categorical aesthetics
    
    def create_trace(self, x=None, y=None, color=None, size=None, alpha=None, linetype=None, label=None, **kwargs):
        """Create a line trace with the given aesthetics"""
        # Use the provided values or resolve from aesthetics
        x = x if x is not None else self._resolve_aesthetic('x')
        y = y if y is not None else self._resolve_aesthetic('y')
        color = color if color is not None else self._resolve_aesthetic('color')
        size = size if size is not None else self._resolve_aesthetic('size', 2)  # Default line width
        alpha = alpha if alpha is not None else self._resolve_aesthetic('alpha', 1.0)
        linetype = linetype if linetype is not None else self._resolve_aesthetic('linetype', 'solid')
        label = label if label is not None else self._resolve_aesthetic('label')
        
        line = {
            'width': size,
            'dash': self._convert_linetype(linetype)
        }
        
        # Handle the color aesthetic
        if color is not None:
            if isinstance(color, pd.Series) and pd.api.types.is_numeric_dtype(color):
                # For numeric data, use a colorscale
                line['color'] = color
                line['colorscale'] = self.params.get('colorscale', 'Viridis')
            else:
                # For a single color or non-numeric array
                line['color'] = color
                
        # Add opacity if needed
        if alpha is not None and alpha != 1.0:
            line['opacity'] = alpha
            
        return go.Scatter(
            x=x,
            y=y,
            mode='lines',
            line=line,
            name=label,
            hoverinfo=self.params.get('hoverinfo', 'all')
        )
    
    def _convert_linetype(self, linetype):
        """Convert ggplot2 linetype to plotly dash style"""
        linetypes = {
            'solid': 'solid',
            'dashed': 'dash',
            'dotted': 'dot',
            'dotdash': 'dashdot',
            'longdash': 'longdash',
            'twodash': 'longdashdot'
        }
        return linetypes.get(linetype, 'solid')