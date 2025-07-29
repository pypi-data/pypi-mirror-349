"""
Data module for gglyra package.
This module provides access to example datasets included with the package.
Data are from https://github.com/tidyverse/ggplot2/tree/main/data-raw
"""
import os
import pandas as pd

def get_data_path(filename: str) -> str:
    """
    Get the path to a data file in the package.
    
    Parameters
    ----------
    filename : str
        Name of the data file to locate.
    
    Returns
    -------
    str
        Absolute path to the data file.
    """
    return os.path.join(os.path.dirname(__file__), filename)

def load_diamonds() -> pd.DataFrame:
    """
    Load the diamonds dataset.
    
    Returns
    -------
    pd.DataFrame
        The diamonds dataset.
    """
    return pd.read_csv(get_data_path('diamonds.csv'))

def load_economics() -> pd.DataFrame:
    """
    Load the economics dataset.
    
    Returns
    -------
    pd.DataFrame
        The economics dataset.
    """
    return pd.read_csv(get_data_path('economics.csv'))


def load_faithful() -> pd.DataFrame:
    """
    Load the faithful dataset.
    
    Returns
    -------
    pd.DataFrame
        The faithful dataset.
    """
    return pd.read_csv(get_data_path('faithful.csv'))

def load_luv_colours() -> pd.DataFrame:
    """
    Load the luv_colours dataset.
    
    Returns
    -------
    pd.DataFrame
        The caluv_coloursrs dataset.
    """
    return pd.read_csv(get_data_path('luv_colours.csv'))

def load_midwest() -> pd.DataFrame:
    """
    Load the midwest dataset.
    
    Returns
    -------
    pd.DataFrame
        The midwest dataset.
    """
    return pd.read_csv(get_data_path('midwest.csv'))

def load_mpg() -> pd.DataFrame:
    """
    Load the cars dataset.
    
    Returns
    -------
    pd.DataFrame
        The cars dataset.
    """
    return pd.read_csv(get_data_path('mpg.csv'))


def load_msleep() -> pd.DataFrame:
    """
    Load the msleep dataset.
    
    Returns
    -------
    pd.DataFrame
        The msleep dataset.
    """
    return pd.read_csv(get_data_path('msleep.csv'))

def load_mtcars() -> pd.DataFrame:
    """
    Load the mtcars dataset.
    
    Returns
    -------
    pd.DataFrame
        The mtcars dataset.
    """
    return pd.read_csv(get_data_path('mtcars.csv'))

def load_presidential() -> pd.DataFrame:
    """
    Load the presidential dataset.
    
    Returns
    -------
    pd.DataFrame
        The presidential dataset.
    """
    return pd.read_csv(get_data_path('presidential.csv'))

def load_seals() -> pd.DataFrame:
    """
    Load the seals dataset.
    
    Returns
    -------
    pd.DataFrame
        The seals dataset.
    """
    return pd.read_csv(get_data_path('seals.csv'))

def load_tx_housing() -> pd.DataFrame:
    """
    Load the tx-housing dataset.
    
    Returns
    -------
    pd.DataFrame
        The tx-housing dataset.
    """
