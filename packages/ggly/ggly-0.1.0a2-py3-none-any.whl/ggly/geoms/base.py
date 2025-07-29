import pandas as pd
import numpy as np
from ..utils.colors import get_color_for_category

class Geom:
    """Base class for all geometric objects in ggly.
    
    This class provides common functionality for resolving aesthetics,
    handling color mapping, and managing trace creation. Individual geom
    implementations should inherit from this class and implement the
    to_trace method.
    """
    def __init__(self, data, mapping=None, stat=None, position=None, **params):
        self.data = data
        self.mapping = mapping or {}
        self.stat = stat
        self.position = position
        self.params = params
        
        # Handle color/colour naming consistency
        self._normalize_aesthetic_names()

    def _normalize_aesthetic_names(self):
        """Handle British/American spelling variations and other aliases"""
        # Handle color/colour
        if 'colour' in self.mapping and 'color' not in self.mapping:
            self.mapping['color'] = self.mapping['colour']
        if 'colour' in self.params and 'color' not in self.params:
            self.params['color'] = self.params['colour']
            
        # Similarly for fill/fill_colour
        if 'fill_colour' in self.mapping and 'fill_color' not in self.mapping:
            self.mapping['fill_color'] = self.mapping['fill_colour']
        if 'fill_colour' in self.params and 'fill_color' not in self.params:
            self.params['fill_color'] = self.params['fill_colour']
            
        # Handle linetype/line_type
        if 'line_type' in self.mapping and 'linetype' not in self.mapping:
            self.mapping['linetype'] = self.mapping['line_type']
        if 'line_type' in self.params and 'linetype' not in self.params:
            self.params['linetype'] = self.params['line_type']

    def to_trace(self):
        """Convert the geom to one or more plotly traces.
        
        This is the main method to implement in subclasses. It should return
        either a single trace or a list of traces.
        """
        # First check for categorical aesthetics that require separate traces
        for aesthetic in ['color', 'fill_color', 'group']:
            aes_value = self._resolve_aesthetic(aesthetic)
            if aes_value is not None:
                categorical_traces = self._process_categorical_aesthetic(aesthetic, aes_value)
                if categorical_traces:
                    # If any trace in the list is itself a list, flatten
                    flat = []
                    for t in categorical_traces:
                        if isinstance(t, (list, tuple)):
                            flat.extend(t)
                        else:
                            flat.append(t)
                    return flat
        
        # If no categorical aesthetics, create a single trace or a list of traces
        result = self.create_trace()
        # If result is a list or tuple, flatten any nested lists
        if isinstance(result, (list, tuple)):
            flat = []
            for t in result:
                if isinstance(t, (list, tuple)):
                    flat.extend(t)
                else:
                    flat.append(t)
            return flat
        return result
        
    def _resolve_aesthetic(self, aes_name, default=None):
        """Resolve an aesthetic value from mapping or params"""
        # Handle common aliases
        aliases = {
            'color': ['colour'],
            'fill_color': ['fill_colour'],
            'linetype': ['line_type'],
            'size': ['width'],
            'alpha': ['opacity']
        }
        
        # Check if we need to look for an alias
        if aes_name in aliases and aes_name not in self.mapping:
            for alias in aliases[aes_name]:
                if alias in self.mapping:
                    aes_name = alias
                    break
            
        if aes_name in self.mapping:
            return self.data[self.mapping[aes_name]]
        elif aes_name in self.params:
            return self.params[aes_name]
        return default
    
    def _process_categorical_aesthetic(self, aesthetic_name, aesthetic_value, **kwargs):
        """
        Process a categorical aesthetic (like color or fill) into separate traces.
        
        Parameters:
        -----------
        aesthetic_name: str
            The name of the aesthetic (e.g., 'color', 'fill_color', 'group')
        aesthetic_value: pd.Series or scalar
            The value of the aesthetic
        **kwargs:
            Additional keyword arguments to pass to the trace creation function
            
        Returns:
        --------
        list or None:
            A list of traces if categorical grouping is needed, None otherwise
        """
        # Only process if it's a categorical Series
        if not (isinstance(aesthetic_value, pd.Series) and
                (pd.api.types.is_categorical_dtype(aesthetic_value) or 
                 pd.api.types.is_object_dtype(aesthetic_value) or
                 (aesthetic_name == 'group'))):
            return None
            
        # Get the base aesthetics that all traces will use
        x = self._resolve_aesthetic('x')
        y = self._resolve_aesthetic('y')
        
        if x is None or y is None:
            return None
            
        traces = []
        for i, cat in enumerate(aesthetic_value.unique()):
            mask = aesthetic_value == cat
            trace_kwargs = kwargs.copy()
            
            # Set the color/fill based on the category
            if aesthetic_name == 'color':
                trace_kwargs['color'] = get_color_for_category(cat, i, self.params.get('palette'))
            elif aesthetic_name == 'fill_color':
                trace_kwargs['fill_color'] = get_color_for_category(cat, i, self.params.get('palette'))
            elif aesthetic_name == 'group':
                # Use the group palette if specified, otherwise use the default palette
                trace_kwargs['color'] = get_color_for_category(cat, i, self.params.get('group_palette', self.params.get('palette')))
                
            # Add masked data
            trace_kwargs['x'] = x[mask] if isinstance(x, pd.Series) else x
            trace_kwargs['y'] = y[mask] if isinstance(y, pd.Series) else y
            
            # Add other aesthetic properties that might be Series
            for prop in ['size', 'alpha', 'shape', 'linetype', 'label']:
                prop_val = self._resolve_aesthetic(prop)
                if isinstance(prop_val, pd.Series):
                    trace_kwargs[prop] = prop_val[mask]
                elif prop_val is not None:
                    trace_kwargs[prop] = prop_val
            
            # --- PATCH: set label to the category value for legend ---
            trace_kwargs['label'] = str(cat)
            trace = self.create_trace(**trace_kwargs)
            if isinstance(trace, (list, tuple)):
                for t in trace:
                    # For smooth, set label for CI and line
                    if hasattr(t, 'name') and 'CI' in getattr(t, 'name', ''):
                        t.name = f"{self.params.get('method', 'trend')} CI - {cat}"
                    elif hasattr(t, 'name'):
                        t.name = f"{self.params.get('method', 'trend')} - {cat}" if self.__class__.__name__.endswith('Smooth') else str(cat)
                traces.extend(trace)
            else:
                if hasattr(trace, 'name'):
                    trace.name = f"{self.params.get('method', 'trend')} - {cat}" if self.__class__.__name__.endswith('Smooth') else str(cat)
                traces.append(trace)
            
        return traces
        
    def _convert_linetype(self, linetype):
        """Convert a ggplot2-style linetype to a plotly dash style"""
        linetypes = {
            'solid': 'solid',
            'dashed': 'dash',
            'dotted': 'dot',
            'dotdash': 'dashdot',
            'longdash': 'longdash',
            'twodash': 'longdashdot'
        }
        return linetypes.get(linetype, 'solid')
        
    def create_trace(self, **kwargs):
        """Create a plotly trace with the given aesthetics.
        
        This method should be implemented by subclasses to create a trace
        with the appropriate type and properties.
        """
        raise NotImplementedError("Subclasses must implement create_trace method")
    
    def _get_group_label(self):
        """Return a concise group label if any mapped aesthetic (color, fill, size, linetype, shape, group) is homogeneous for this geom instance."""
        for aes in ['color', 'fill', 'fill_color', 'size', 'linetype', 'shape', 'group']:
            if aes in self.mapping and isinstance(self.mapping[aes], str):
                col = self.mapping[aes]
                if hasattr(self, 'data') and hasattr(self.data, 'loc') and col in self.data:
                    unique_vals = pd.unique(self.data[col])
                    if len(unique_vals) == 1:
                        return f"{col}={unique_vals[0]}"
        return None