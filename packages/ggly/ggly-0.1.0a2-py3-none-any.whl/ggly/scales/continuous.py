from .base import Scale

class ScaleContinuous(Scale):
    """Continuous scale"""
    def __init__(self, limits=None, breaks=None, labels=None, name=None, trans=None):
        super().__init__(limits, breaks, labels, name)
        self.trans = trans
        
    def apply(self, fig, axis):
        """Apply continuous scale to axis"""
        axis_props = {}
        
        if self.limits:
            axis_props['range'] = self.limits
            
        if self.breaks:
            axis_props['tickvals'] = self.breaks
            
        if self.labels:
            axis_props['ticktext'] = self.labels
            
        if self.name:
            axis_props['title'] = self.name
        
        # Apply transformation
        if self.trans:
            if self.trans == 'log10':
                axis_props['type'] = 'log'
                axis_props['dtick'] = 1  # 1 log cycle
            elif self.trans == 'log2':
                # Plotly doesn't have direct log2 support, would need a custom implementation
                axis_props['type'] = 'log'
                # Further customization needed
            elif self.trans == 'sqrt':
                # Would need custom implementation
                pass
            
        # Apply the properties to the correct axis
        if axis == 'x':
            fig.update_xaxes(**axis_props)
        elif axis == 'y':
            fig.update_yaxes(**axis_props)
            
        return fig
