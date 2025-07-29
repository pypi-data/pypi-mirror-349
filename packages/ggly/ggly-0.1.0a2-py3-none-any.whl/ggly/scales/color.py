from .base import Scale

class ScaleColorContinuous(Scale):
    """Continuous color scale"""
    def __init__(self, limits=None, breaks=None, labels=None, name=None, low=None, high=None, colorscale=None):
        super().__init__(limits, breaks, labels, name)
        self.low = low
        self.high = high
        self.colorscale = colorscale or 'Viridis'
        
    def apply(self, fig, colorbar=True):
        """Apply continuous color scale to figure"""
        for trace in fig.data:
            if hasattr(trace, 'marker') and trace.marker:
                # Update the colorscale
                if hasattr(trace.marker, 'colorscale'):
                    trace.marker.colorscale = self.colorscale
                    
                    # Update color range if limits provided
                    if self.limits:
                        trace.marker.cmin = self.limits[0]
                        trace.marker.cmax = self.limits[1]
                        
                    # Update colorbar
                    if colorbar and hasattr(trace.marker, 'colorbar'):
                        if self.name:
                            trace.marker.colorbar.title = self.name
                        if self.breaks:
                            trace.marker.colorbar.tickvals = self.breaks
                        if self.labels:
                            trace.marker.colorbar.ticktext = self.labels
        return fig


class ScaleColorDiscrete(Scale):
    """Discrete color scale"""
    def __init__(self, limits=None, breaks=None, labels=None, name=None, palette=None):
        super().__init__(limits, breaks, labels, name)
        self.palette = palette or ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                                  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
    def apply(self, fig, legend=True):
        """Apply discrete color scale to figure"""
        # Get unique categories across all traces
        categories = set()
        for trace in fig.data:
            if hasattr(trace, 'name') and trace.name:
                categories.add(trace.name)
        
        # Assign colors from palette
        color_map = {}
        for i, cat in enumerate(sorted(categories)):
            color_map[cat] = self.palette[i % len(self.palette)]
        
        # Apply colors to traces
        for trace in fig.data:
            if hasattr(trace, 'name') and trace.name in color_map:
                if hasattr(trace, 'marker') and trace.marker:
                    trace.marker.color = color_map[trace.name]
                elif hasattr(trace, 'line') and trace.line:
                    trace.line.color = color_map[trace.name]
        
        # Update legend if needed
        if legend and self.name:
            fig.update_layout(legend_title_text=self.name)
            
        return fig
