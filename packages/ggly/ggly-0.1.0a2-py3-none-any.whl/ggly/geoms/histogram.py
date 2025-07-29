# filepath: /home/essi/Documents/gitlab/ggly/src/ggly/geoms/histogram.py
from .base import Geom
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class GeomHistogram(Geom):
    """Histogram geom for creating histograms with unified aesthetic handling."""
    def to_trace(self):
        # Use the base class's categorical aesthetic handling for color/fill
        return super().to_trace()

    def create_trace(self, x=None, y=None, color=None, alpha=None, label=None, **kwargs):
        x = x if x is not None else self._resolve_aesthetic('x')
        y = y if y is not None else self._resolve_aesthetic('y')
        bins = self.params.get('bins', 30)
        color = color if color is not None else self._resolve_aesthetic('color')
        alpha = alpha if alpha is not None else self._resolve_aesthetic('alpha', 1.0)
        label = label if label is not None else self._resolve_aesthetic('label')
        marker = {}
        if color is not None:
            marker['color'] = color
        if alpha != 1.0:
            marker['opacity'] = alpha
        if y is not None and x is None:
            return go.Histogram(
                y=y,
                nbinsy=bins,
                marker=marker,
                name=label or self.params.get('name', '')
            )
        else:
            return go.Histogram(
                x=x,
                nbinsx=bins,
                marker=marker,
                name=label or self.params.get('name', '')
            )