# ggly

A Grammar of Graphics for Plotly - Inspired by ggplot2

## Overview

ggly is a Python library that implements a grammar of graphics similar to R's ggplot2, but using Plotly as the visualization backend. It allows you to create sophisticated, publication-quality data visualizations using a consistent and intuitive API based on the principles of the grammar of graphics.

## Features

- **ggplot2-like syntax**: Method chaining API that will feel familiar to ggplot2 users
- **Built on Plotly**: Interactive visualizations powered by Plotly's graph_objects
- **Grammar components**: Support for geoms, stats, scales, faceting, and coords
- **Themes**: Built-in themes for consistent visualization styling

## Installation

```bash
# Install from PyPI
pip install ggly

# Or install from source
git clone https://github.com/yourusername/ggly.git
cd ggly
pip install -e .
```

## Basic Usage

```python
from ggly.core import ggplot
from ggly.aes import aes
import pandas as pd

# Load data
mpg = pd.DataFrame({
    'cty': [18, 21, 20, 16, 18],
    'hwy': [29, 33, 29, 26, 26],
    'class': ['compact', 'compact', 'midsize', 'midsize', 'suv']
})

# Create a plot
(
    ggplot(mpg, aes(x='cty', y='hwy', color='class'))
    .geom_point()
    .labs(
        title="Fuel consumption",
        subtitle="Highway Mileage vs City Mileage",
        x="City Mileage",
        y="Highway Mileage",
        color="Class of vehicles"
    )
    .theme_minimal()
    .show()
)
```

## Supported Features

- **Geoms**: point, line, bar, histogram, boxplot
- **Stats**: count, smooth
- **Coords**: cartesian, flip
- **Faceting**: wrap, grid
- **Scales**: continuous, discrete, color

## Comparison with ggplot2

ggly aims to emulate ggplot2's syntax and functionality as closely as possible, with some adaptations for Plotly's capabilities and Python's ecosystem.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
