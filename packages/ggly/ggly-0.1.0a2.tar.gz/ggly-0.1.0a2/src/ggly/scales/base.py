class Scale:
    """Base scale class"""
    def __init__(self, limits=None, breaks=None, labels=None, name=None):
        self.limits = limits
        self.breaks = breaks
        self.labels = labels
        self.name = name
        
    def apply(self, fig, axis):
        """Apply scale to axis"""
        axis_props = {}
        
        if self.limits:
            axis_props['range'] = self.limits
            
        if self.breaks:
            axis_props['tickvals'] = self.breaks
            
        if self.labels:
            axis_props['ticktext'] = self.labels
            
        if self.name:
            axis_props['title'] = self.name
            
        # Apply the properties to the correct axis
        if axis == 'x':
            fig.update_xaxes(**axis_props)
        elif axis == 'y':
            fig.update_yaxes(**axis_props)
            
        return fig
