# GGLyra Data Directory

This directory contains CSV data files used by the GGLyra visualization library. These datasets are bundled with the library to provide examples and test data for visualization.

## Available Datasets

The following datasets are available in this directory:

- `cars.csv`: Car performance data including MPG, horsepower, and origin
- `diamonds.csv`: Diamond characteristics and prices 
- `economics.csv`: US economic time series data
- `faithful.csv`: Old Faithful geyser eruption data
- `luv_colours.csv`: Color data in LUV color space
- `midwest.csv`: Demographic data of midwest counties
- `mpg.csv`: Detailed fuel economy data for vehicles
- `msleep.csv`: Sleep data for various mammal species
- `mtcars.csv`: Motor Trend car road tests
- `presidential.csv`: US presidential terms data
- `seals.csv`: Seal locations and counts
- `tx-housing.csv`: Texas housing data

## Usage

These datasets can be loaded using either of the following methods:

### Method 1: Using the `load_data()` function

```python
from gglyra import load_data

# Load a dataset by name
cars = load_data("cars.csv")
```

### Method 2: Using the `data` module

```python
from gglyra import data

# Load datasets using convenience functions
cars = data.load_cars()
diamonds = data.load_diamonds()
```

## Search Path

The data loading functions search for datasets in the following locations:

1. The `docs/` directory (for notebook examples)
2. The `data/` directory (this directory)

This ensures that both development and installed package contexts work correctly.

## Adding New Datasets

To add a new dataset:

1. Add the CSV file to this directory
2. Add a corresponding loading function in `src/gglyra/data/__init__.py`

```python
def load_new_dataset():
    """
    Load the new dataset.
    
    Returns:
        pd.DataFrame: The new dataset.
    """
    return pd.read_csv(_get_data_path('new_dataset.csv'))
```
