from .base import Theme

class ThemeMinimal(Theme):
    """A minimal theme similar to ggplot2's theme_minimal"""
    def __init__(self):
        super().__init__()
        self.layout = {
            'template': 'plotly_white',
            'plot_bgcolor': 'white',
            'paper_bgcolor': 'white',
            'xaxis': {
                'showgrid': True,
                'gridcolor': 'lightgray',
                'zeroline': False,
                'ticks': '',
            },
            'yaxis': {
                'showgrid': True,
                'gridcolor': 'lightgray',
                'zeroline': False,
                'ticks': '',
            },
            'legend': {
                'bgcolor': 'rgba(0,0,0,0)',
                'bordercolor': 'rgba(0,0,0,0)'
            },
            'margin': {'t': 80, 'b': 50, 'l': 50, 'r': 50}
        }
