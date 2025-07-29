from .base import Geom
import plotly.graph_objects as go
import pandas as pd

class GeomPoint(Geom):
    """Scatter plot geom for creating points.
    
    This geom creates a scatter plot of points, optionally mapping aesthetics
    like color, size, and shape to variables in the data.
    """
    # No need to override to_trace as the base implementation handles categorical aesthetics
    
    # Track if colorbar has been shown for this plot
    _colorbar_shown = False

    def create_trace(self, x=None, y=None, color=None, size=None, alpha=None, shape=None, label=None, **kwargs):
        """Create a scatter trace with the given aesthetics"""
        # Use the provided values or resolve from aesthetics
        x = x if x is not None else self._resolve_aesthetic('x')
        y = y if y is not None else self._resolve_aesthetic('y')
        color = color if color is not None else self._resolve_aesthetic('color')
        size = size if size is not None else self._resolve_aesthetic('size')
        alpha = alpha if alpha is not None else self._resolve_aesthetic('alpha', 1.0)
        shape = shape if shape is not None else self._resolve_aesthetic('shape', 'circle')
        label = label if label is not None else self._resolve_aesthetic('label')
        
        # Use base _get_group_label for concise legend naming
        if label is None:
            group_label = self._get_group_label()
            if group_label is not None:
                label = group_label
        
        marker = {}
        
        # Handle the color aesthetic
        if color is not None:
            if isinstance(color, pd.Series) and pd.api.types.is_numeric_dtype(color):
                marker['color'] = color
                marker['colorscale'] = self.params.get('colorscale', 'Viridis')
                # Only show colorbar for the first geom_point with numeric color
                if not GeomPoint._colorbar_shown:
                    marker['showscale'] = True
                    GeomPoint._colorbar_shown = True
                else:
                    marker['showscale'] = False
            else:
                marker['color'] = color
                
        # Add other aesthetic properties
        if size is not None:
            marker['size'] = size
        
        if alpha is not None and alpha != 1.0:
            marker['opacity'] = alpha
            
        if shape is not None:
            marker['symbol'] = shape
            
        return go.Scatter(
            x=x,
            y=y,
            mode='markers',
            marker=marker,
            name=label,
            hoverinfo=self.params.get('hoverinfo', 'all')
        )