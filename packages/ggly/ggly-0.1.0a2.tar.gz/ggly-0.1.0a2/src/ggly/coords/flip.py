from .base import Coord

class CoordFlip(Coord):
    """Flipped cartesian coordinate system (swap x and y axes)"""
    def __init__(self):
        super().__init__()
        
    def apply(self, fig):
        """Flip x and y axes"""
        # Swap axis labels if they exist
        layout = fig.layout
        
        # Save original axis properties
        x_props = {}
        y_props = {}
        
        if hasattr(layout, 'xaxis') and layout.xaxis:
            if hasattr(layout.xaxis, 'title') and layout.xaxis.title:
                x_props['title'] = layout.xaxis.title.text
        
        if hasattr(layout, 'yaxis') and layout.yaxis:
            if hasattr(layout.yaxis, 'title') and layout.yaxis.title:
                y_props['title'] = layout.yaxis.title.text
                
        # Update layout with swapped properties
        layout_updates = {}
        if 'title' in x_props:
            layout_updates['yaxis'] = {'title': x_props['title']}
        if 'title' in y_props:
            layout_updates['xaxis'] = {'title': y_props['title']}
            
        # For the trace data swapping, we'd need to handle this during trace creation
        # in the core ggplot class, because here we don't have access to the raw data
        
        if layout_updates:
            fig.update_layout(**layout_updates)
            
        return fig