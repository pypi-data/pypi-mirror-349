# filepath: /home/essi/Documents/gitlab/ggly/src/ggly/geoms/path.py
from .base import Geom
import plotly.graph_objects as go
import pandas as pd

class GeomPath(Geom):
    """Path geom for creating line segments that aren't necessarily connected, with unified aesthetic handling."""
    def to_trace(self):
        # Use the base class's categorical aesthetic handling for color/group
        return super().to_trace()

    def create_trace(self, x=None, y=None, color=None, size=None, alpha=None, linetype=None, label=None, **kwargs):
        x = x if x is not None else self._resolve_aesthetic('x')
        y = y if y is not None else self._resolve_aesthetic('y')
        color = color if color is not None else self._resolve_aesthetic('color')
        size = size if size is not None else self._resolve_aesthetic('size', 1)
        alpha = alpha if alpha is not None else self._resolve_aesthetic('alpha', 1.0)
        linetype = linetype if linetype is not None else self._resolve_aesthetic('linetype', 'solid')
        label = label if label is not None else self._resolve_aesthetic('label')
        line = {
            'width': size,
            'dash': self._convert_linetype(linetype)
        }
        if color is not None:
            if isinstance(color, pd.Series) and pd.api.types.is_numeric_dtype(color):
                line['color'] = color
                line['colorscale'] = self.params.get('colorscale', 'Viridis')
            else:
                line['color'] = color
        if alpha is not None and alpha != 1.0:
            line['opacity'] = alpha
        return go.Scatter(
            x=x,
            y=y,
            mode='lines',
            line=line,
            name=label or self.params.get('name', ''),
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