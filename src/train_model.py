"""Training script for CNN people counting model."""

import numpy as np
import json
import os
from pathlib import Path
from datetime import datetime
import tensorflow as tf
from tensorflow import keras

from cnn_model import create_cnn_model, create_lightweight_cnn
from utils import (
    create_image_dataset, split_dataset, 
    normalize_counts, denormalize_counts
)


class PeopleCountingTrainer:
    """Trainer for people counting CNN model."""
    
    def __init__(self, model_name='standard', input_shape=(224, 224, 3), 
                 learning_rate=0.001):
        """
        Initialize trainer.
        
        Args:
            model_name: 'standard' or 'lightweight'
            input_shape: Input image shape
            learning_rate: Learning rate for optimizer
        """
        if model_name == 'lightweight':
            self.model = create_lightweight_cnn(input_shape, learning_rate)
        else:
            self.model = create_cnn_model(input_shape, learning_rate)
        
        self.history = None
        self.scaler = None
        self.input_shape = input_shape
    
    def train(self, X_train, y_train, X_val, y_val, epochs=50, batch_size=32):
        """
        Train the model.
        
        Args:
            X_train: Training images
            y_train: Training counts
            X_val: Validation images
            y_val: Validation counts
            epochs: Number of training epochs
            batch_size: Batch size
        
        Returns:
            Training history
        """
        # Normalize targets
        y_train_norm, self.scaler = normalize_counts(y_train, method='minmax')
        y_val_norm, _ = normalize_counts(y_val, method='minmax')
        
        # Early stopping callback
        early_stop = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        # Learning rate reduction callback
        reduce_lr = keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6
        )
        
        # Train model
        self.history = self.model.fit(
            X_train, y_train_norm,
            validation_data=(X_val, y_val_norm),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stop, reduce_lr],
            verbose=1
        )
        
        return self.history
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate model on test set.
        
        Args:
            X_test: Test images
            y_test: Test counts
        
        Returns:
            Dictionary with evaluation metrics
        """
        y_test_norm, _ = normalize_counts(y_test, method='minmax')
        loss, mae, mse = self.model.evaluate(X_test, y_test_norm, verbose=0)
        
        rmse = np.sqrt(mse)
        
        # Make predictions
        y_pred_norm = self.model.predict(X_test, verbose=0).flatten()
        y_pred = denormalize_counts(y_pred_norm, self.scaler)
        
        # Calculate denormalized metrics
        mae_denorm = np.mean(np.abs(y_pred - y_test))
        mse_denorm = np.mean((y_pred - y_test) ** 2)
        rmse_denorm = np.sqrt(mse_denorm)
        
        metrics = {
            'loss': float(loss),
            'mae': float(mae),
            'mse': float(mse),
            'rmse': float(rmse),
            'mae_denormalized': float(mae_denorm),
            'mse_denormalized': float(mse_denorm),
            'rmse_denormalized': float(rmse_denorm)
        }
        
        return metrics, y_pred
    
    def predict(self, X):
        """
        Make predictions.
        
        Args:
            X: Input images
        
        Returns:
            Predicted counts
        """
        y_pred_norm = self.model.predict(X, verbose=0).flatten()
        y_pred = denormalize_counts(y_pred_norm, self.scaler)
        return y_pred
    
    def save_model(self, filepath):
        """Save model to file."""
        self.model.save(filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load model from file."""
        self.model = keras.models.load_model(filepath)
        print(f"Model loaded from {filepath}")
    
    def save_scaler(self, filepath):
        """Save scaler parameters."""
        with open(filepath, 'w') as f:
            json.dump(self.scaler, f)
        print(f"Scaler saved to {filepath}")
    
    def load_scaler(self, filepath):
        """Load scaler parameters."""
        with open(filepath, 'r') as f:
            self.scaler = json.load(f)
        print(f"Scaler loaded from {filepath}")


def main():
    """Main training script."""
    # Configuration
    config = {
        'image_dir': 'dataset/images',
        'counts_file': 'dataset/counts.json',
        'output_dir': 'models',
        'model_name': 'standard',
        'input_shape': (224, 224, 3),
        'learning_rate': 0.001,
        'epochs': 50,
        'batch_size': 32,
        'train_ratio': 0.7,
        'val_ratio': 0.15
    }
    
    # Create output directory
    Path(config['output_dir']).mkdir(exist_ok=True)
    
    print("Loading dataset...")
    
    # Load counts
    with open(config['counts_file'], 'r') as f:
        count_dict = json.load(f)
    
    # Create dataset
    images, counts = create_image_dataset(
        config['image_dir'],
        count_dict,
        target_size=config['input_shape'][:2],
        normalize=True
    )
    
    print(f"Dataset size: {len(images)} images")
    print(f"Count range: {counts.min():.1f} - {counts.max():.1f}")
    
    # Split dataset
    X_train, X_val, X_test, y_train, y_val, y_test = split_dataset(
        images, counts,
        train_ratio=config['train_ratio'],
        val_ratio=config['val_ratio']
    )
    
    print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
    
    # Create trainer
    print("\nTraining model...")
    trainer = PeopleCountingTrainer(
        model_name=config['model_name'],
        input_shape=config['input_shape'],
        learning_rate=config['learning_rate']
    )
    
    # Train
    trainer.train(
        X_train, y_train,
        X_val, y_val,
        epochs=config['epochs'],
        batch_size=config['batch_size']
    )
    
    # Evaluate
    print("\nEvaluating model...")
    metrics, predictions = trainer.evaluate(X_test, y_test)
    print(f"Test Metrics: {metrics}")
    
    # Save model and scaler
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f"{config['output_dir']}/people_counter_{timestamp}.h5"
    scaler_path = f"{config['output_dir']}/scaler_{timestamp}.json"
    
    trainer.save_model(model_path)
    trainer.save_scaler(scaler_path)
    
    # Save metrics
    metrics_path = f"{config['output_dir']}/metrics_{timestamp}.json"
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\nTraining complete!")
    print(f"Model saved to: {model_path}")
    print(f"Scaler saved to: {scaler_path}")
    print(f"Metrics saved to: {metrics_path}")


if __name__ == '__main__':
    main()