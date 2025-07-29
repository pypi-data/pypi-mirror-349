# filepath: /home/essi/Documents/gitlab/ggly/src/ggly/stats/smooth.py
from .base import Stat
import numpy as np
import pandas as pd
from scipy import stats

class StatSmooth(Stat):
    """Smoothing function similar to ggplot2's stat_smooth"""
    def __init__(self, data=None, mapping=None, method="lm", span=0.75, 
                 level=0.95, n=80, **params):
        super().__init__(data, mapping, **params)
        self.method = method  # "lm" for linear model or "loess" for local regression
        self.span = span      # smoothing parameter for loess
        self.level = level    # confidence level
        self.n = n            # number of points to evaluate smoothed function at
        
    def compute(self):
        """Compute the smoothed function"""
        if self.data is None or len(self.data) < 2:
            return None
            
        # Get x and y data
        x_col = self.mapping.get('x')
        y_col = self.mapping.get('y')
        
        if x_col is None or y_col is None:
            return None
            
        x = self.data[x_col].values
        y = self.data[y_col].values
        
        # Ensure we have valid data
        valid_mask = ~(np.isnan(x) | np.isnan(y))
        x = x[valid_mask]
        y = y[valid_mask]
        
        if len(x) < 2:
            return None
            
        # Process based on selected method
        if self.method == "lm":
            return self._compute_linear_model(x, y)
        elif self.method == "loess":
            return self._compute_loess(x, y)
        else:
            # Default to linear model
            return self._compute_linear_model(x, y)
    
    def _compute_linear_model(self, x, y):
        """Compute linear regression model"""
        # Simple linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Generate points along x-axis
        x_range = np.linspace(min(x), max(x), self.n)
        y_fit = intercept + slope * x_range
        
        # Confidence intervals
        if self.level > 0:
            # Simplified confidence interval calculation
            # In a real implementation, we would use proper prediction intervals
            conf_interval = std_err * stats.t.ppf((1 + self.level) / 2, len(x) - 2) * np.sqrt(1/len(x))
            y_upper = y_fit + conf_interval
            y_lower = y_fit - conf_interval
        else:
            y_upper = y_fit
            y_lower = y_fit
        
        # Return dataframe with smoothed values
        result = pd.DataFrame({
            'x': x_range,
            'y': y_fit,
            'ymin': y_lower,
            'ymax': y_upper
        })
        
        return result
    
    def _compute_loess(self, x, y):
        """Compute local regression smoothing"""
        # This is a simplified version - real LOESS is more complex
        # Would typically use statsmodels or another library for full LOESS implementation
        
        # Sort data by x
        sort_idx = np.argsort(x)
        x = x[sort_idx]
        y = y[sort_idx]
        
        # Generate evenly spaced x points for prediction
        x_range = np.linspace(min(x), max(x), self.n)
        y_fit = np.zeros_like(x_range)
        
        # Simplified local regression (moving average)
        # This is not true LOESS but a simple approximation
        span_points = int(len(x) * self.span)
        for i, xi in enumerate(x_range):
            # Find nearest points
            dists = np.abs(x - xi)
            idx = np.argsort(dists)[:span_points]
            
            # Weighted average based on distance (triangular kernel)
            weights = 1 - (dists[idx] / dists[idx].max())
            y_fit[i] = np.average(y[idx], weights=weights)
        
        # For confidence intervals - just approximate
        # Real implementation would be more complex
        y_err = np.std(y) / np.sqrt(span_points)
        conf_factor = stats.norm.ppf((1 + self.level) / 2)
        
        result = pd.DataFrame({
            'x': x_range,
            'y': y_fit,
            'ymin': y_fit - y_err * conf_factor,
            'ymax': y_fit + y_err * conf_factor
        })
        
        return result