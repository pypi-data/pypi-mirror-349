from .base import Theme

class ThemeGGPlot2(Theme):
    """A theme inspired by ggplot2's default look."""
    def __init__(self):
        super().__init__()
        self.layout = {
            'template': 'ggplot2',  # reste utile comme base
            'plot_bgcolor': '#EBEBEB',
            'paper_bgcolor': 'white',
            'font': {
                'family': 'Arial',
                'color': '#222B45',
                'size': 12
            },
            'xaxis': {
                'showgrid': True,
                'gridcolor': 'white',
                'gridwidth': 1,
                'zeroline': False,
                'tickcolor': '#222222',
                'ticks': 'outside',
                'linecolor': 'rgba(0,0,0,0)',  # ggplot2 ne montre pas l'axe
                'layer': 'below traces'       # grille en arrière-plan
            },
            'yaxis': {
                'showgrid': True,
                'gridcolor': 'white',
                'gridwidth': 1,
                'zeroline': False,
                'tickcolor': '#222222',
                'ticks': 'outside',
                'linecolor': 'rgba(0,0,0,0)',  # pas de ligne visible
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
