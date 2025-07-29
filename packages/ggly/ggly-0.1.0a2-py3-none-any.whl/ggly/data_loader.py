import pandas as pd
import os
from pathlib import Path

# Get the path to the data directories in the project
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))
DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../docs'))
SEARCH_DIRS = [DOCS_DIR, DATA_DIR]

def load_data(name):
    """
    Loads a dataset from the project's data directories.
    First searches in the docs directory, then in the data directory.
    
    Args:
        name (str): The name of the dataset file (e.g., 'dataset.csv').
    Returns:
        pd.DataFrame: The loaded dataset as a pandas DataFrame.
    Raises:
        FileNotFoundError: If the dataset file does not exist in any of the search directories.
    """
    # Try to find the file in the search directories
    for directory in SEARCH_DIRS:
        data_path = os.path.join(directory, name)
        if os.path.exists(data_path):
            if data_path.endswith('economics.csv'):
                return pd.read_csv(data_path, parse_dates=["date"])
            else:
                return pd.read_csv(data_path)

    # If we get here, the file wasn't found
    raise FileNotFoundError(f"Dataset file '{name}' not found in any of the search directories: {SEARCH_DIRS}")

def list_datasets():
    """
    Lists all available datasets in the project's data directories.
    Returns:
        list: A list of dataset names (file names) available in the directories.
    """
    datasets = set()
    for directory in SEARCH_DIRS:
        if os.path.exists(directory):
            datasets.update([f for f in os.listdir(directory) if f.endswith('.csv')])
    return sorted(list(datasets))