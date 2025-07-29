import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from ggly.core import ggplot
from ggly.aes import aes

def test_geom_smooth_basic():
    # Simple linear data
    df = pd.DataFrame({'x': np.arange(10), 'y': np.arange(10) + np.random.normal(0, 1, 10)})
    p = ggplot(df, aes(x='x', y='y')).geom_point().geom_smooth(method='lm', se=True)
    fig = p.build()
    # Should have at least 2 traces (scatter + smooth)
    assert len(fig.data) >= 2, f"Expected at least 2 traces, got {len(fig.data)}"
    # Check that one trace is a line (smooth)
    trace_types = [t.type for t in fig.data]
    assert 'scatter' in trace_types, f"No scatter trace found: {trace_types}"
    # Check that at least one trace has mode 'lines'
    assert any(getattr(t, 'mode', None) == 'lines' for t in fig.data), "No line trace found for smooth"
    print("test_geom_smooth_basic passed")

def test_geom_smooth_categorical():
    # Data with a categorical color
    df = pd.DataFrame({'x': np.tile(np.arange(10), 2), 'y': np.concatenate([np.arange(10), np.arange(10)[::-1]]), 'g': ['A']*10 + ['B']*10})
    p = ggplot(df, aes(x='x', y='y', color='g')).geom_point().geom_smooth(method='lm', se=False)
    fig = p.build()
    # Should have at least 4 traces (2 groups: point+line each)
    assert len(fig.data) >= 4, f"Expected at least 4 traces, got {len(fig.data)}"
    print("test_geom_smooth_categorical passed")

if __name__ == "__main__":
    test_geom_smooth_basic()
    test_geom_smooth_categorical()
    print("All geom_smooth tests passed.")
