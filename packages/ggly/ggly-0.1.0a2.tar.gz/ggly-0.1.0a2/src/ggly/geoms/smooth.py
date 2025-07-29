from .base import Geom
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.nonparametric.smoothers_lowess import lowess
import statsmodels.api as sm

class GeomSmooth(Geom):
    """Smooth geom for regression/trend lines (linear regression or loess, with confidence interval)."""
    def create_trace(self, x=None, y=None, color=None, size=None, alpha=None, se=True, level=0.95, label=None, method='lm', span=0.75, **kwargs):
        # Use the provided values or resolve from aesthetics
        # --- PATCH: always use explicit color/size/alpha if given in params, override aes ---
        color = self.params.get('color', color)
        size = self.params.get('size', size)
        alpha = self.params.get('alpha', alpha)
        label = self.params.get('label', label)
        se = self.params.get('se', se)
        level = self.params.get('level', level)
        method = self.params.get('method', method)
        span = self.params.get('span', span)
        ci_opacity = self.params.get('ci_opacity', 0.25)
        x = x if x is not None else self._resolve_aesthetic('x')
        y = y if y is not None else self._resolve_aesthetic('y')
        if color is None:
            color = self._resolve_aesthetic('color', 'black')
        # PATCH: If size is a Series/array, use its mean for line width
        if hasattr(size, 'mean') and not np.isscalar(size):
            size = float(np.nanmean(size))
        elif isinstance(size, (list, np.ndarray)) and not np.isscalar(size):
            size = float(np.nanmean(size))
        if alpha is None:
            alpha = self._resolve_aesthetic('alpha', 1.0)
        if label is None:
            label = self._resolve_aesthetic('label', 'trend')
        # Use base _get_group_label for concise legend naming
        group_label = self._get_group_label()
        if label is None or label == 'trend':
            if group_label is not None:
                label = f"{method} - {group_label}"
            else:
                label = method
        # Determine group label for legend if color/group is mapped, but only use the value, not the full Series
        # Remove NaNs
        mask = (~pd.isnull(x)) & (~pd.isnull(y))
        x = np.array(x)[mask]
        y = np.array(y)[mask]
        if len(x) < 2:
            return []  # Not enough data
        order = np.argsort(x)
        x = x[order]
        y = y[order]
        traces = []
        # Store fitted model for export
        self.fitted_model_ = None
        self.fitted_summary_ = None
        # PATCH: Ensure color is a string before using in _rgba (for both CI and line)
        def _safe_color(c):
            if hasattr(c, 'dtype') or isinstance(c, (pd.Series, np.ndarray, list)):
                return 'black'
            return c
        if method == 'loess':
            loess_result = lowess(y, x, frac=span, return_sorted=True)
            x_smooth = loess_result[:, 0]
            y_smooth = loess_result[:, 1]
            self.fitted_model_ = (x_smooth, y_smooth)
            if se:
                resid = y - np.interp(x, x_smooth, y_smooth)
                s = np.std(resid)
                n = len(x)
                tval = stats.t.ppf(1 - (1 - level) / 2, n - 2)
                y_err = tval * s / np.sqrt(n)
                upper = y_smooth + y_err
                lower = y_smooth - y_err
                traces.append(go.Scatter(
                    x=np.concatenate([x_smooth, x_smooth[::-1]]),
                    y=np.concatenate([upper, lower[::-1]]),
                    fill='toself',
                    fillcolor=self._rgba(_safe_color(color), ci_opacity),
                    line=dict(color='rgba(255,255,255,0)'),
                    hoverinfo='skip',
                    showlegend=False,
                    name=label + ' CI',
                    marker=dict(showscale=False),  # PATCH: showscale must be inside marker
                ))
            traces.append(go.Scatter(
                x=x_smooth,
                y=y_smooth,
                mode='lines',
                line=dict(color=_safe_color(color), width=size),
                opacity=alpha,
                name=label,
                hoverinfo=self.params.get('hoverinfo', 'all'),
                marker=dict(showscale=False),  # PATCH: showscale must be inside marker
            ))
        else:
            # Linear regression using statsmodels
            X = sm.add_constant(x)
            model = sm.OLS(y, X).fit()
            y_pred = model.predict(X)
            self.fitted_model_ = model
            self.fitted_summary_ = model.summary()
            if se:
                n = len(x)
                tval = stats.t.ppf(1 - (1 - level) / 2, n - 2)
                mse = np.mean((y - y_pred) ** 2)
                mean_x = np.mean(x)
                se_fit = np.sqrt(mse * (1/n + (x - mean_x)**2 / np.sum((x - mean_x)**2)))
                y_err = tval * se_fit
                upper = y_pred + y_err
                lower = y_pred - y_err
                traces.append(go.Scatter(
                    x=np.concatenate([x, x[::-1]]) if method == 'lm' else np.concatenate([x_smooth, x_smooth[::-1]]),
                    y=np.concatenate([upper, lower[::-1]]),
                    fill='toself',
                    fillcolor=self._rgba(_safe_color(color), ci_opacity),
                    line=dict(color='rgba(255,255,255,0)'),
                    hoverinfo='skip',
                    showlegend=False,
                    name=label + ' CI',
                    marker=dict(showscale=False),  # PATCH: showscale must be inside marker
                ))
            traces.append(go.Scatter(
                x=x,
                y=y_pred,
                mode='lines',
                line=dict(color=_safe_color(color), width=size),
                opacity=alpha,
                name=label,
                hoverinfo=self.params.get('hoverinfo', 'all'),
                marker=dict(showscale=False),  # PATCH: showscale must be inside marker
            ))
        return traces

    def _rgba(self, color, opacity):
        # Accepts color names or rgb/hex, returns rgba string with given opacity
        if color is None:
            return f'rgba(0,0,0,{opacity})'
        if color.startswith('rgba'):
            parts = color.split(',')
            if len(parts) == 4:
                return ','.join(parts[:3]) + f',{opacity})'
            return color
        if color.startswith('#'):
            hex_color = color.lstrip('#')
            if len(hex_color) == 6:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                return f'rgba({r},{g},{b},{opacity})'
            elif len(hex_color) == 3:
                r = int(hex_color[0]*2, 16)
                g = int(hex_color[1]*2, 16)
                b = int(hex_color[2]*2, 16)
                return f'rgba({r},{g},{b},{opacity})'
        color_dict = {
            'black': (0,0,0), 'red': (255,0,0), 'green': (0,128,0), 'blue': (0,0,255),
            'gray': (128,128,128), 'grey': (128,128,128), 'yellow': (255,255,0),
            'orange': (255,165,0), 'purple': (128,0,128), 'pink': (255,192,203),
            'brown': (165,42,42), 'white': (255,255,255)
        }
        rgb = color_dict.get(color.lower())
        if rgb:
            return f'rgba({rgb[0]},{rgb[1]},{rgb[2]},{opacity})'
        return f'rgba(0,0,0,{opacity})'

def geom_smooth(mapping=None, **kwargs):
    """User-facing function for geom_smooth."""
    return GeomSmooth(None, mapping, **kwargs)
