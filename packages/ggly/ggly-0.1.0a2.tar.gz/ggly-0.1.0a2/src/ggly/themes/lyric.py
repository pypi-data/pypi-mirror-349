from .base import Theme

class ThemeLyric(Theme):
    """A custom aesthetic theme for ggly charts."""
    def __init__(self):
        super().__init__()
        self.layout = {
            'template': 'simple_white',
            'plot_bgcolor': "#F0EEE8",
            'paper_bgcolor': 'white',
            'font': {
                'family': 'Arial',
                'color': '#222B45',
                'size': 12
            },
            'xaxis': {
                'gridcolor': '#fff',
                'gridwidth': 1,
                'zeroline': False,
                'tickcolor': '#222222',
                'linecolor': '#222222',
                'ticks': 'outside',
                'showgrid': True,
                'layer': 'below traces'
            },
            'yaxis': {
                'gridcolor': '#fff',
                'gridwidth': 1,
                'zeroline': False,
                'tickcolor': '#222222',
                'linecolor': '#222222',
                'ticks': 'outside',
                'showgrid': True,
                'layer': 'below traces'
            },

            'legend': {
                'bgcolor': 'rgba(0,0,0,0)',
                'bordercolor': 'rgba(0,0,0,0)',
                'orientation': 'v',
                'font': {
                    'color': '#222B45',
                    'family': 'Arial',
                    'size': 11
                }
            },
            'title': {
                'x': 0.01,
                'xanchor': 'left',
                'font': {
                    'family': 'Arial',
                    'size': 16,
                    'color': '#222222'
                }
            },
            'margin': {'t': 80, 'b': 50, 'l': 50, 'r': 50}
        }
