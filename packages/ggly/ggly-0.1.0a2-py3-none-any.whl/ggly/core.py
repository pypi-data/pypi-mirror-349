import plotly.graph_objects as go
import pandas as pd
import numpy as np
import re
from .aes import aes
from .geoms.point import GeomPoint
from .geoms.line import GeomLine
from .geoms.bar import GeomBar
from .geoms.histogram import GeomHistogram
from .geoms.boxplot import GeomBoxplot

def _parse_facet_formula(formula):
    """Parse a formula string like 'var1 ~ var2' or '~ var2' or 'var1 ~'"""
    if not isinstance(formula, str) or '~' not in formula:
        return None, None
    parts = [p.strip() for p in formula.split('~', 1)]
    left = parts[0] if parts[0] else None
    right = parts[1] if len(parts) > 1 and parts[1] else None
    return left, right

class ggplot:
    def __init__(self, data: pd.DataFrame, mapping=None):
        self.data = data
        self.mapping = mapping or {}
        self.layers = []
        self.labels = {}
        self.theme = None
        self.layout_params = {}
        self.facet = None
        self.coord = None
        self.scales = {}

    def geom_point(self, mapping=None, **kwargs):
        m = {**self.mapping, **(mapping or {})}
        self.layers.append(GeomPoint(self.data, m, **kwargs))
        return self

    def geom_line(self, mapping=None, **kwargs):
        m = {**self.mapping, **(mapping or {})}
        self.layers.append(GeomLine(self.data, m, **kwargs))
        return self

    def geom_path(self, mapping=None, **kwargs):
        m = {**self.mapping, **(mapping or {})}
        self.layers.append(GeomLine(self.data, m, **kwargs))
        return self

    def geom_bar(self, mapping=None, stat="count", **kwargs):
        m = {**self.mapping, **(mapping or {})}
        self.layers.append(GeomBar(self.data, m, stat=stat, **kwargs))
        return self

    def geom_col(self, mapping=None, **kwargs):
        m = {**self.mapping, **(mapping or {})}
        self.layers.append(GeomBar(self.data, m, stat="identity", **kwargs))
        return self

    def geom_histogram(self, mapping=None, bins=30, **kwargs):
        m = {**self.mapping, **(mapping or {})}
        self.layers.append(GeomHistogram(self.data, m, bins=bins, **kwargs))
        return self

    def geom_boxplot(self, mapping=None, **kwargs):
        m = {**self.mapping, **(mapping or {})}
        self.layers.append(GeomBoxplot(self.data, m, **kwargs))
        return self

    def geom_smooth(self, mapping=None, **kwargs):
        from .geoms.smooth import GeomSmooth
        m = {**self.mapping, **(mapping or {})}
        self.layers.append(GeomSmooth(self.data, m, **kwargs))
        return self

    def labs(self, **kwargs):
        self.labels.update(kwargs)
        return self

    def ggtitle(self, title, subtitle=None):
        self.labels['title'] = title
        if subtitle:
            self.labels['subtitle'] = subtitle
        return self

    def xlab(self, label):
        self.labels['x'] = label
        return self

    def ylab(self, label):
        self.labels['y'] = label
        return self

    def theme_lyric(self):
        from .themes.lyric import ThemeLyric
        self.theme = ThemeLyric()
        return self

    def theme_ggplot2(self):
        from .themes.ggplot2 import ThemeGGPlot2
        self.theme = ThemeGGPlot2()
        return self

    def theme_minimal(self):
        self.theme = 'minimal'
        return self
        
    def theme_dark(self):
        self.theme = 'dark'
        return self

    def theme_light(self):
        self.theme = 'light'
        return self

    def theme_classic(self):
        self.theme = 'classic'
        return self

    def coord_cartesian(self, xlim=None, ylim=None):
        self.coord = {'type': 'cartesian', 'xlim': xlim, 'ylim': ylim}
        return self
    
    def coord_flip(self):
        self.coord = {'type': 'flip'}
        return self

    def facet_wrap(self, facets, nrow=None, ncol=None, scales="fixed"):
        # Support tilde formula: 'var1 ~ var2' or '~ var2' or 'var1 ~'
        if isinstance(facets, str) and '~' in facets:
            left, right = _parse_facet_formula(facets)
            if left and right:
                # Both sides: treat as grid
                return self.facet_grid(rows=left, cols=right, scales=scales)
            elif left:
                facets = left
            elif right:
                facets = right
        self.facet = {
            'type': 'wrap',
            'facets': facets,
            'nrow': nrow,
            'ncol': ncol,
            'scales': scales
        }
        return self

    def facet_grid(self, rows=None, cols=None, scales="fixed"):
        # Support tilde formula: 'var1 ~ var2' or '~ var2' or 'var1 ~'
        if isinstance(rows, str) and '~' in rows and cols is None:
            left, right = _parse_facet_formula(rows)
            rows, cols = left, right
        self.facet = {
            'type': 'grid',
            'rows': rows,
            'cols': cols,
            'scales': scales
        }
        return self

    def scale_x_continuous(self, breaks=None, labels=None, limits=None, trans=None, **kwargs):
        self.scales['x'] = {
            'type': 'continuous',
            'breaks': breaks,
            'labels': labels, 
            'limits': limits,
            'trans': trans,
            **kwargs
        }
        return self

    def scale_y_continuous(self, breaks=None, labels=None, limits=None, trans=None, **kwargs):
        self.scales['y'] = {
            'type': 'continuous',
            'breaks': breaks,
            'labels': labels, 
            'limits': limits,
            'trans': trans,
            **kwargs
        }
        return self

    def scale_color_continuous(self, low=None, high=None, name=None, **kwargs):
        self.scales['color'] = {
            'type': 'continuous',
            'low': low,
            'high': high,
            'name': name,
            **kwargs
        }
        return self

    def scale_colour_continuous(self, low=None, high=None, name=None, **kwargs):
        return self.scale_color_continuous(low, high, name, **kwargs)

    def scale_color_discrete(self, palette=None, name=None, **kwargs):
        self.scales['color'] = {
            'type': 'discrete',
            'palette': palette,
            'name': name,
            **kwargs
        }
        return self

    def scale_colour_discrete(self, palette=None, name=None, **kwargs):
        return self.scale_color_discrete(palette, name, **kwargs)

    def scale_fill_continuous(self, low=None, high=None, name=None, palette=None, **kwargs):
        """Set a continuous fill scale (for e.g. geom_bar(fill=...), geom_histogram, etc)."""
        self.scales['fill'] = {
            'type': 'continuous',
            'low': low,
            'high': high,
            'name': name,
            'palette': palette,
            **kwargs
        }
        return self

    def scale_fill_discrete(self, palette=None, name=None, **kwargs):
        """Set a discrete fill scale (for e.g. geom_bar(fill=...), geom_histogram, etc)."""
        self.scales['fill'] = {
            'type': 'discrete',
            'palette': palette,
            'name': name,
            **kwargs
        }
        return self

    def scale_colour_fill_continuous(self, *args, **kwargs):
        return self.scale_fill_continuous(*args, **kwargs)

    def scale_colour_fill_discrete(self, *args, **kwargs):
        return self.scale_fill_discrete(*args, **kwargs)

    @property
    def fitted_models(self):
        """Return a list of fitted models from all GeomSmooth layers (if any)."""
        models = []
        for layer in self.layers:
            if hasattr(layer, 'fitted_model_') and layer.fitted_model_ is not None:
                models.append(layer.fitted_model_)
        return models

    @property
    def fitted_summaries(self):
        """Return a list of fitted model summaries from all GeomSmooth layers (if any)."""
        summaries = []
        for layer in self.layers:
            if hasattr(layer, 'fitted_summary_') and layer.fitted_summary_ is not None:
                summaries.append(layer.fitted_summary_)
        return summaries

    def build(self):
        # Faceting support
        if self.facet:
            if self.facet['type'] == 'wrap':
                from .facets.wrap import FacetWrap
                facet = FacetWrap(
                    self.facet['facets'],
                    nrow=self.facet.get('nrow'),
                    ncol=self.facet.get('ncol'),
                    scales=self.facet.get('scales', 'fixed')
                )
                fig = facet.apply(None, self.data, self.layers)
            elif self.facet['type'] == 'grid':
                from .facets.grid import FacetGrid
                facet = FacetGrid(
                    rows=self.facet.get('rows'),
                    cols=self.facet.get('cols'),
                    scales=self.facet.get('scales', 'fixed')
                )
                fig = facet.apply(None, self.data, self.layers)
            else:
                raise ValueError(f"Unknown facet type: {self.facet['type']}")
        else:
            fig = go.Figure()
            # Diagnostics: print trace types and names for debugging
            import sys
            for layer in self.layers:
                trace_result = layer.to_trace()
                if isinstance(trace_result, list):
                    for i, trace in enumerate(trace_result):
                        print(f"[DEBUG] Layer {type(layer).__name__} trace {i}: type={type(trace)}, name={getattr(trace, 'name', None)}", file=sys.stderr)
                        fig.add_trace(trace)
                else:
                    print(f"[DEBUG] Layer {type(layer).__name__}: type={type(trace_result)}, name={getattr(trace_result, 'name', None)}", file=sys.stderr)
                    fig.add_trace(trace_result)

        layout = {}
        # Handle title and subtitle
        if 'title' in self.labels:
            title_config = {
                'text': self.labels['title'],
                'x': 0.5
            }
            if 'subtitle' in self.labels:
                title_config['subtitle'] = {'text': self.labels['subtitle']}
            layout['title'] = title_config

        # Handle axis labels
        if 'x' in self.labels:
            layout['xaxis'] = {'title': self.labels['x']}
        if 'y' in self.labels:
            layout['yaxis'] = {'title': self.labels['y']}
        if 'color' in self.labels:
            # For legend title
            layout['legend'] = {'title': {'text': self.labels['color']}}

        # Apply coordinate system
        if self.coord:
            if self.coord['type'] == 'cartesian':
                if self.coord['xlim']:
                    layout.setdefault('xaxis', {})['range'] = self.coord['xlim']
                if self.coord['ylim']:
                    layout.setdefault('yaxis', {})['range'] = self.coord['ylim']
            elif self.coord['type'] == 'flip':
                x_layout = layout.get('xaxis', {})
                y_layout = layout.get('yaxis', {})
                layout['xaxis'] = y_layout
                layout['yaxis'] = x_layout

        # Apply theme
        if self.theme and hasattr(self.theme, 'layout'):
            # Cas des thèmes custom (ThemeLyric, etc.)
            fig.update_layout(**self.theme.layout)
        else:
            # Cas des thèmes simples par string
            default_templates = {
                'minimal': 'plotly_white',
                'dark': 'plotly_dark',
                'light': 'plotly',
                'classic': 'simple_white',
                'ggplot2': 'ggplot2',
                'lyric': 'plotly_white'
            }
            # Use 'plotly' as the default template (the default of plotly)
            template = default_templates.get(self.theme, 'plotly')
            fig.update_layout(template=template)

        # Appliquer barmode pour les bar charts si nécessaire
        barmode = None
        for layer in self.layers:
            if isinstance(layer, GeomBar):
                position = getattr(layer, 'position', None) or 'stack'
                if position == 'stack':
                    barmode = 'stack'
                elif position == 'group':
                    barmode = 'group'
        if barmode:
            fig.update_layout(barmode=barmode)

        # --- PATCH: Robust legend and colorbar layout (stacked, proportional height, multiple colorbars) ---
        # Detect all colorbars (not just if any are present)
        colorbar_traces = []
        for trace in fig.data:
            if hasattr(trace, 'marker') and hasattr(trace.marker, 'colorbar') and trace.marker.colorbar:
                colorbar_traces.append(trace)
        # Also check for coloraxis colorbar (e.g. for density/heatmap)
        has_coloraxis = 'coloraxis' in fig.layout
        n_colorbars = len(colorbar_traces) + (1 if has_coloraxis else 0)

        # Legend always at top right, vertical
        legend_x = 1.13  # Décalé plus à droite
        legend_y = 1.0
        legend_xanchor = 'left'
        legend_yanchor = 'top'
        legend_orientation = 'v'
        legend_tracegroupgap = 8
        n_blocks = 1 + n_colorbars  # 1 for legend, rest for colorbars
        block_height = 1.0 / n_blocks
        colorbar_padding = 0.10  # 10% padding in each block

        fig.update_layout(
            legend=dict(
                x=legend_x,
                xanchor=legend_xanchor,
                y=legend_y,
                yanchor=legend_yanchor,
                orientation=legend_orientation,
                tracegroupgap=legend_tracegroupgap,
                bgcolor='rgba(255,255,255,0.95)',
                bordercolor='rgba(0,0,0,0.08)',
                borderwidth=1,
                font=dict(size=13),
            ),
            margin=dict(r=200)  # Plus de marge à droite
        )

        # Place each colorbar in its block, centered, with padding
        for i, trace in enumerate(colorbar_traces):
            colorbar_x = 1.02  # Laisse la colorbar à gauche de la légende
            colorbar_xanchor = 'left'
            colorbar_len = block_height * (1 - colorbar_padding)
            colorbar_y = 1.0 - block_height * (i + 1) + block_height / 2
            colorbar_yanchor = 'middle'
            trace.marker.colorbar.x = colorbar_x
            trace.marker.colorbar.xanchor = colorbar_xanchor
            trace.marker.colorbar.len = colorbar_len
            trace.marker.colorbar.y = colorbar_y
            trace.marker.colorbar.yanchor = colorbar_yanchor

        if has_coloraxis:
            coloraxis_idx = len(colorbar_traces)
            colorbar_x = 1.02
            colorbar_xanchor = 'left'
            colorbar_len = block_height * (1 - colorbar_padding)
            colorbar_y = 1.0 - block_height * (coloraxis_idx + 1) + block_height / 2
            colorbar_yanchor = 'middle'
            fig.update_layout(
                coloraxis_colorbar=dict(
                    x=colorbar_x,
                    xanchor=colorbar_xanchor,
                    len=colorbar_len,
                    y=colorbar_y,
                    yanchor=colorbar_yanchor,
                )
            )
        return fig

    def show(self):
        self.build().show()

    def _repr_html_(self):
        # Jupyter/IPython rich display: show the plot inline, but return self for chaining
        try:
            fig = self.build()
            from plotly.io import to_html
            return to_html(fig, include_plotlyjs='cdn', full_html=False)
        except Exception as e:
            return f"<pre>ggly rendering error: {e}</pre>"

    def __repr__(self):
        # Fallback for plain Python: just show a summary
        return f"<ggplot object with {len(self.layers)} layer(s)>"
