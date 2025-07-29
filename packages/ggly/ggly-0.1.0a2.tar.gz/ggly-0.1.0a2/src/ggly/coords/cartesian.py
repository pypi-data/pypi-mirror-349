from .base import Coord

class CoordCartesian(Coord):
    """Cartesian coordinate system (the default)"""
    def __init__(self, xlim=None, ylim=None, expand=True):
        super().__init__()
        self.xlim = xlim
        self.ylim = ylim
        self.expand = expand
        
    def apply(self, fig):
        """Apply cartesian coordinates with specified limits"""
        layout_updates = {}
        
        if self.xlim is not None:
            layout_updates['xaxis'] = {'range': self.xlim}
            
        if self.ylim is not None:
            layout_updates['yaxis'] = {'range': self.ylim}
            
        if layout_updates:
            fig.update_layout(**layout_updates)
            
        return fig