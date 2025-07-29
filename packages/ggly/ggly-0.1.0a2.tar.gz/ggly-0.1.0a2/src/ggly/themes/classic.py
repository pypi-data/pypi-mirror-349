from .base import Theme

class ThemeClassic(Theme):
    """A classic theme similar to ggplot2's theme_classic"""
    def __init__(self):
        super().__init__()
        self.layout = {
            'template': 'simple_white',
            'plot_bgcolor': 'white',
            'paper_bgcolor': 'white',
            'xaxis': {
                'showgrid': False,
                'zeroline': True,
                'zerolinecolor': 'black',
                'zerolinewidth': 1,
                'ticks': 'outside',
                'tickcolor': 'black',
                'linecolor': 'black'
            },
            'yaxis': {
                'showgrid': False,
                'zeroline': True,
                'zerolinecolor': 'black',
                'zerolinewidth': 1,
                'ticks': 'outside',
                'tickcolor': 'black',
                'linecolor': 'black'
            },
            'legend': {
                'bgcolor': 'rgba(0,0,0,0)',
                'bordercolor': 'rgba(0,0,0,0)'
            },
            'margin': {'t': 80, 'b': 50, 'l': 50, 'r': 50}
        }
