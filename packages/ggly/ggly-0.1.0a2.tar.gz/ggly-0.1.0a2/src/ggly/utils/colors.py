"""
Utility functions for handling colors in ggly
"""
import plotly.colors as colors

# Default color sequences
# These are directly from plotly's qualitative color sequences
QUALITATIVE_COLORS = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]

# Add more default color sequences
DARK_COLORS = [
    '#1b9e77',  # teal
    '#d95f02',  # orange
    '#7570b3',  # blue-purple
    '#e7298a',  # magenta
    '#66a61e',  # lime green
    '#e6ab02',  # mustard
    '#a6761d',  # tan
    '#666666'   # gray
]

PASTEL_COLORS = [
    '#a6cee3',  # pale blue
    '#1f78b4',  # steel blue
    '#b2df8a',  # pale green
    '#33a02c',  # dark green
    '#fb9a99',  # pink
    '#e31a1c',  # red
    '#fdbf6f',  # light orange
    '#ff7f00',  # orange
    '#cab2d6',  # pale purple
    '#6a3d9a'   # purple
]

def get_color_for_category(category_name, category_index, palette=None):
    """
    Get a color for a categorical value based on its index.
    
    Parameters:
    -----------
    category_name : str
        The name of the category
    category_index : int
        The index of the category in the list of unique categories
    palette : str or list
        The name of a predefined palette or a list of colors
        
    Returns:
    --------
    color : str
        A color in hex format
    """
    # Choose default palette if none specified
    if palette is None:
        color_list = QUALITATIVE_COLORS
    elif palette == 'dark':
        color_list = DARK_COLORS
    elif palette == 'pastel':
        color_list = PASTEL_COLORS
    elif isinstance(palette, list):
        color_list = palette
    else:
        # Try to get a named Plotly colorscale
        try:
            color_list = getattr(colors.qualitative, palette)
        except:
            color_list = QUALITATIVE_COLORS
    
    # Return a color from the palette, cycling if needed
    return color_list[category_index % len(color_list)]

def generate_color_mapping(categories, palette=None):
    """
    Generate a mapping from categories to colors.
    
    Parameters:
    -----------
    categories : list-like
        A list or array of category names
    palette : str or list
        The name of a predefined palette or a list of colors
        
    Returns:
    --------
    mapping : dict
        A dictionary mapping each category to a color
    """
    mapping = {}
    for i, cat in enumerate(categories):
        mapping[cat] = get_color_for_category(cat, i, palette)
    return mapping
