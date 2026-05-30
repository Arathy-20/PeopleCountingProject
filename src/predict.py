"""Prediction script for people counting."""

import json
import numpy as np
from pathlib import Path
import tensorflow as tf
from tensorflow import keras

from utils import load_image, preprocess_image, denormalize_counts


class PeopleCounter:
    """Inference class for people counting."""
    
    def __init__(self, model_path, scaler_path):
        """
        Initialize predictor.
        
        Args:
            model_path: Path to trained model
            scaler_path: Path to scaler parameters
        """
        self.model = keras.models.load_model(model_path)
        
        with open(scaler_path, 'r') as f:
            self.scaler = json.load(f)
        
        print(f"Model loaded from {model_path}")
        print(f"Scaler loaded from {scaler_path}")
    
    def predict_image(self, image_path, target_size=(224, 224)):
        """
        Predict count for a single image.
        
        Args:
            image_path: Path to image
            target_size: Image size
        
        Returns:
            Predicted count
        """
        img = load_image(image_path, target_size)
        img = preprocess_image(img, normalize=True)
        img = np.expand_dims(img, axis=0)
        
        pred_norm = self.model.predict(img, verbose=0)[0, 0]
        pred = denormalize_counts(np.array([pred_norm]), self.scaler)[0]
        
        return float(pred)
    
    def predict_batch(self, image_paths, target_size=(224, 224)):
        """
        Predict counts for multiple images.
        
        Args:
            image_paths: List of image paths
            target_size: Image size
        
        Returns:
            Array of predicted counts
        """
        images = []
        for path in image_paths:
            img = load_image(path, target_size)
            img = preprocess_image(img, normalize=True)
            images.append(img)
        
        images = np.array(images)
        preds_norm = self.model.predict(images, verbose=0).flatten()
        preds = denormalize_counts(preds_norm, self.scaler)
        
        return preds
    
    def predict_directory(self, image_dir, target_size=(224, 224)):
        """
        Predict counts for all images in directory.
        
        Args:
            image_dir: Directory containing images
            target_size: Image size
        
        Returns:
            Dictionary mapping filename to count
        """
        image_dir = Path(image_dir)
        results = {}
        
        image_files = list(image_dir.glob('*.jpg')) + list(image_dir.glob('*.png'))
        
        if not image_files:
            print(f"No images found in {image_dir}")
            return results
        
        print(f"Processing {len(image_files)} images...")
        
        for img_file in image_files:
            try:
                count = self.predict_image(str(img_file), target_size)
                results[img_file.name] = float(count)
                print(f"{img_file.name}: {count:.2f}")
            except Exception as e:
                print(f"Error processing {img_file.name}: {e}")
        
        return results
    
    def get_model_info(self):
        """Get model architecture info."""
        self.model.summary()


def main():
    """Main prediction script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='People counting prediction')
    parser.add_argument('--model', required=True, help='Path to trained model')
    parser.add_argument('--scaler', required=True, help='Path to scaler')
    parser.add_argument('--image', help='Single image path')
    parser.add_argument('--directory', help='Directory of images')
    parser.add_argument('--output', default='predictions.json', help='Output JSON file')
    
    args = parser.parse_args()
    
    # Initialize counter
    counter = PeopleCounter(args.model, args.scaler)
    
    results = {}
    
    if args.image:
        print(f"Predicting for single image: {args.image}")
        count = counter.predict_image(args.image)
        results[Path(args.image).name] = count
        print(f"Predicted count: {count:.2f}")
    
    elif args.directory:
        print(f"Predicting for directory: {args.directory}")
        results = counter.predict_directory(args.directory)
    
    # Save results
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {args.output}")


if __name__ == '__main__':
    main()