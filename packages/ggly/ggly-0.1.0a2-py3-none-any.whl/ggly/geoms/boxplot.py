# filepath: /home/essi/Documents/gitlab/ggly/src/ggly/geoms/boxplot.py
from .base import Geom
import plotly.graph_objects as go
import pandas as pd

class GeomBoxplot(Geom):
    """Boxplot geom for creating boxplots with unified aesthetic handling."""
    def to_trace(self):
        # Use the base class's categorical aesthetic handling for color/group
        return super().to_trace()

    def create_trace(self, x=None, y=None, color=None, alpha=None, label=None, **kwargs):
        x = x if x is not None else self._resolve_aesthetic('x')
        y = y if y is not None else self._resolve_aesthetic('y')
        color = color if color is not None else self._resolve_aesthetic('color')
        alpha = alpha if alpha is not None else self._resolve_aesthetic('alpha', 1.0)
        label = label if label is not None else self._resolve_aesthetic('label')
        marker = {}
        if color is not None:
            marker['color'] = color
        if alpha != 1.0:
            marker['opacity'] = alpha
        # Handle both vertical and horizontal boxplots
        if y is None:
            return go.Box(
                x=x,
                name=label or self.params.get('name', ''),
                opacity=alpha,
                marker_color=color if color is not None else None
            )
        elif x is None:
            return go.Box(
                y=y,
                name=label or self.params.get('name', ''),
                opacity=alpha,
                marker_color=color if color is not None else None
            )
        else:
            # Grouped boxplot: one trace per group (handled by base if color/group is categorical)
            return go.Box(
                x=x,
                y=y,
                name=label or self.params.get('name', ''),
                opacity=alpha,
                marker_color=color if color is not None else None
            )