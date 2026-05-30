"""Evaluation metrics for people counting model."""

import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path


class ModelEvaluator:
    """Evaluate model predictions."""
    
    def __init__(self, y_true, y_pred):
        """
        Initialize evaluator.
        
        Args:
            y_true: Ground truth counts
            y_pred: Predicted counts
        """
        self.y_true = np.array(y_true)
        self.y_pred = np.array(y_pred)
    
    def mae(self):
        """Mean Absolute Error."""
        return np.mean(np.abs(self.y_true - self.y_pred))
    
    def mse(self):
        """Mean Squared Error."""
        return np.mean((self.y_true - self.y_pred) ** 2)
    
    def rmse(self):
        """Root Mean Squared Error."""
        return np.sqrt(self.mse())
    
    def mape(self):
        """Mean Absolute Percentage Error."""
        # Avoid division by zero
        mask = self.y_true != 0
        if np.sum(mask) == 0:
            return np.nan
        return np.mean(np.abs((self.y_true[mask] - self.y_pred[mask]) / self.y_true[mask])) * 100
    
    def r_squared(self):
        """R-squared (coefficient of determination)."""
        ss_res = np.sum((self.y_true - self.y_pred) ** 2)
        ss_tot = np.sum((self.y_true - np.mean(self.y_true)) ** 2)
        return 1 - (ss_res / ss_tot)
    
    def max_error(self):
        """Maximum absolute error."""
        return np.max(np.abs(self.y_true - self.y_pred))
    
    def median_error(self):
        """Median absolute error."""
        return np.median(np.abs(self.y_true - self.y_pred))
    
    def get_all_metrics(self):
        """Get all evaluation metrics."""
        return {
            'mae': float(self.mae()),
            'mse': float(self.mse()),
            'rmse': float(self.rmse()),
            'mape': float(self.mape()),
            'r_squared': float(self.r_squared()),
            'max_error': float(self.max_error()),
            'median_error': float(self.median_error()),
            'count_samples': int(len(self.y_true))
        }
    
    def print_metrics(self):
        """Print evaluation metrics."""
        print("\n" + "="*50)
        print("MODEL EVALUATION METRICS")
        print("="*50)
        print(f"MAE (Mean Absolute Error):     {self.mae():.4f}")
        print(f"MSE (Mean Squared Error):      {self.mse():.4f}")
        print(f"RMSE (Root Mean Squared Error): {self.rmse():.4f}")
        print(f"MAPE (Mean Absolute % Error):  {self.mape():.2f}%")
        print(f"R² (Coefficient of Determination): {self.r_squared():.4f}")
        print(f"Max Error:                     {self.max_error():.4f}")
        print(f"Median Error:                  {self.median_error():.4f}")
        print(f"Number of Samples:             {len(self.y_true)}")
        print("="*50 + "\n")
    
    def plot_predictions(self, output_path='evaluation.png'):
        """
        Plot predicted vs actual counts.
        
        Args:
            output_path: Path to save plot
        """
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Scatter plot: Predicted vs Actual
        axes[0, 0].scatter(self.y_true, self.y_pred, alpha=0.6)
        min_val = min(self.y_true.min(), self.y_pred.min())
        max_val = max(self.y_true.max(), self.y_pred.max())
        axes[0, 0].plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)
        axes[0, 0].set_xlabel('True Count')
        axes[0, 0].set_ylabel('Predicted Count')
        axes[0, 0].set_title('Predicted vs Actual Counts')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Error distribution
        errors = self.y_true - self.y_pred
        axes[0, 1].hist(errors, bins=20, edgecolor='black', alpha=0.7)
        axes[0, 1].axvline(x=0, color='r', linestyle='--', linewidth=2)
        axes[0, 1].set_xlabel('Prediction Error')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('Error Distribution')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Residuals plot
        axes[1, 0].scatter(self.y_pred, errors, alpha=0.6)
        axes[1, 0].axhline(y=0, color='r', linestyle='--', linewidth=2)
        axes[1, 0].set_xlabel('Predicted Count')
        axes[1, 0].set_ylabel('Residuals')
        axes[1, 0].set_title('Residuals Plot')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Absolute error plot
        abs_errors = np.abs(errors)
        axes[1, 1].scatter(self.y_true, abs_errors, alpha=0.6)
        axes[1, 1].set_xlabel('True Count')
        axes[1, 1].set_ylabel('Absolute Error')
        axes[1, 1].set_title('Absolute Error vs True Count')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=100)
        print(f"Evaluation plot saved to {output_path}")
        plt.close()


def evaluate_predictions(y_true, y_pred, output_json=None, plot_output=None):
    """
    Evaluate predictions and optionally save results.
    
    Args:
        y_true: Ground truth values
        y_pred: Predicted values
        output_json: Path to save JSON metrics
        plot_output: Path to save evaluation plot
    
    Returns:
        Dictionary of metrics
    """
    evaluator = ModelEvaluator(y_true, y_pred)
    metrics = evaluator.get_all_metrics()
    
    evaluator.print_metrics()
    
    if output_json:
        with open(output_json, 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"Metrics saved to {output_json}")
    
    if plot_output:
        evaluator.plot_predictions(plot_output)
    
    return metrics


def compare_predictions(results_dict):
    """
    Compare predictions with ground truth from results dictionary.
    
    Args:
        results_dict: Dict with 'true' and 'pred' keys
    
    Returns:
        Metrics dictionary
    """
    y_true = results_dict.get('true', [])
    y_pred = results_dict.get('pred', [])
    
    if len(y_true) != len(y_pred):
        raise ValueError("True and predicted counts have different lengths")
    
    return evaluate_predictions(y_true, y_pred)


if __name__ == '__main__':
    # Sample data
    y_true = np.array([10, 25, 30, 5, 45, 20, 15, 35, 40, 50])
    y_pred = np.array([12, 24, 32, 6, 44, 19, 16, 34, 42, 48])
    
    # Evaluate
    metrics = evaluate_predictions(
        y_true, y_pred,
        output_json='metrics.json',
        plot_output='evaluation.png'
    )