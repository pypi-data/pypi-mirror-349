"""
Unit tests for the core ggplot functionality
"""
import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.ggly.core import ggplot
from src.ggly.aes import aes

class TestGGPlot:
    """Test suite for the ggplot class"""
    
    @pytest.fixture
    def sample_data(self):
        """Create a simple sample dataframe for testing"""
        return pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [10, 20, 15, 30, 25],
            'group': ['A', 'A', 'B', 'B', 'C']
        })
        
    def test_ggplot_init(self, sample_data):
        """Test ggplot initialization"""
        p = ggplot(sample_data, aes(x='x', y='y'))
        
        assert p.data is sample_data
        assert p.mapping == {'x': 'x', 'y': 'y'}
        assert p.layers == []
        
    def test_geom_point_adds_layer(self, sample_data):
        """Test that geom_point adds a layer"""
        p = ggplot(sample_data, aes(x='x', y='y'))
        p = p.geom_point()
        
        assert len(p.layers) == 1
        
    def test_labs_updates_labels(self, sample_data):
        """Test that labs updates the labels"""
        p = ggplot(sample_data, aes(x='x', y='y'))
        p = p.labs(title="Test Title", x="X Label", y="Y Label")
        
        assert p.labels['title'] == "Test Title"
        assert p.labels['x'] == "X Label"
        assert p.labels['y'] == "Y Label"
        
    def test_build_returns_figure(self, sample_data):
        """Test that build returns a plotly figure"""
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point()
        fig = p.build()
        
        # Check that it's a plotly figure
        assert hasattr(fig, 'update_layout')
        assert hasattr(fig, 'add_trace')
        
        # Check that it has one trace
        assert len(fig.data) == 1
