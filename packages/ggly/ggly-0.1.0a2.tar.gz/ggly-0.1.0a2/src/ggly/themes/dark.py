# filepath: /home/essi/Documents/gitlab/ggly/src/ggly/themes/dark.py
from .base import Theme

class ThemeDark(Theme):
    """A dark theme similar to ggplot2's theme_dark"""
    def __init__(self):
        super().__init__()
        self.layout = {
            'template': 'plotly_dark',
            'plot_bgcolor': '#222222',
            'paper_bgcolor': '#222222',
            'font': {'color': 'white'},
            'xaxis': {
                'showgrid': True,
                'gridcolor': '#444444',
                'zeroline': False,
                'ticks': '',
                'color': 'white'
            },
            'yaxis': {
                'showgrid': True,
                'gridcolor': '#444444',
                'zeroline': False,
                'ticks': '',
                'color': 'white'
            },
            'legend': {
                'bgcolor': 'rgba(0,0,0,0)',
                'bordercolor': 'rgba(0,0,0,0)',
                'font': {'color': 'white'}
            },
            'margin': {'t': 80, 'b': 50, 'l': 50, 'r': 50}
        }