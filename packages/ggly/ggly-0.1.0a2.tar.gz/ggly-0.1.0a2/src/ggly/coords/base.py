class Coord:
    """Base class for coordinate systems"""
    def __init__(self):
        pass
        
    def apply(self, fig):
        """Apply coordinate system to figure"""
        raise NotImplementedError