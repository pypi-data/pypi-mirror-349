import plotly.graph_objects as go

class Theme:
    """Base theme class"""
    def __init__(self):
        self.layout = {}
        
    def apply(self, fig):
        """Apply theme to figure"""
        fig.update_layout(**self.layout)
        return fig
        
    def to_dict(self):
        """Return theme as dictionary"""
        return self.layout
