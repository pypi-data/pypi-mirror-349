from .base import Scale

class ScaleDiscrete(Scale):
    """Discrete scale"""
    def __init__(self, limits=None, breaks=None, labels=None, name=None):
        super().__init__(limits, breaks, labels, name)
        
    def apply(self, fig, axis):
        """Apply discrete scale to axis"""
        axis_props = {}
        
        if self.limits:
            # In discrete scales, limits are categories to include
            if axis == 'x':
                # Filter trace data to only include specified categories
                # Would need custom implementation
                pass
            elif axis == 'y':
                # Similar to x-axis
                pass
            
        if self.breaks:
            axis_props['tickvals'] = self.breaks
            
        if self.labels:
            axis_props['ticktext'] = self.labels
            
        if self.name:
            axis_props['title'] = self.name
        
        # For categorical data
        axis_props['type'] = 'category'
        
        # Apply the properties to the correct axis
        if axis == 'x':
            fig.update_xaxes(**axis_props)
        elif axis == 'y':
            fig.update_yaxes(**axis_props)
            
        return fig
