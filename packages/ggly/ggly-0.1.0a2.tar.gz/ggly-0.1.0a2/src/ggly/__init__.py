"""
ggly: A Grammar of Graphics for Plotly

ggly is a Python library implementing a ggplot2-inspired grammar of graphics using Plotly as the backend.
It provides a method-chaining API for creating sophisticated data visualizations.
"""

__version__ = "0.1.0"

from .core import ggplot
from .aes import aes

# Import key components
from .geoms import GeomPoint, GeomLine, GeomBar, GeomHistogram, GeomBoxplot
from .stats import Stat, StatCount, StatSmooth
from .coords import Coord, CoordCartesian, CoordFlip
from .scales import Scale
from .themes import Theme, ThemeMinimal, ThemeClassic, ThemeDark, ThemeGGPlot2, ThemeLyric
from .facets import Facet, FacetWrap, FacetGrid
from .utils import get_color_for_category, generate_color_mapping
from .data_loader import load_data, list_datasets

__all__ = [
    'ggplot', 'aes', 
    'GeomPoint', 'GeomLine', 'GeomBar', 'GeomHistogram', 'GeomBoxplot',
    'Stat', 'StatCount', 'StatSmooth',
    'Coord', 'CoordCartesian', 'CoordFlip',
    'Scale', 
    'Theme', 'ThemeMinimal', 'ThemeClassic', 'ThemeDark', 'ThemeGGPlot2', 'ThemeLyric',
    'Facet', 'FacetWrap', 'FacetGrid',
    'get_color_for_category', 'generate_color_mapping',
    'load_data', 'list_datasets'
]
