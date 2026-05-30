"""Utility functions for data preprocessing and loading."""

import numpy as np
import cv2
import os
from pathlib import Path


def load_image(image_path, target_size=(224, 224)):
    """
    Load and preprocess an image.
    
    Args:
        image_path: Path to image file
        target_size: Desired output size (height, width)
    
    Returns:
        Preprocessed image as numpy array
    """
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (target_size[1], target_size[0]))
    
    return img


def preprocess_image(image, normalize=True):
    """
    Preprocess image for model input.
    
    Args:
        image: Image as numpy array
        normalize: Whether to normalize to [0, 1]
    
    Returns:
        Preprocessed image
    """
    if normalize:
        image = image.astype('float32') / 255.0
    else:
        image = image.astype('float32')
    
    return image


def load_batch_images(image_paths, target_size=(224, 224), normalize=True):
    """
    Load a batch of images.
    
    Args:
        image_paths: List of image file paths
        target_size: Desired output size
        normalize: Whether to normalize images
    
    Returns:
        Batch of images as numpy array (N, H, W, C)
    """
    images = []
    for path in image_paths:
        img = load_image(path, target_size)
        img = preprocess_image(img, normalize)
        images.append(img)
    
    return np.array(images)


def normalize_counts(counts, method='standard'):
    """
    Normalize count values.
    
    Args:
        counts: Array of count values
        method: 'standard' for z-score, 'minmax' for [0,1]
    
    Returns:
        Normalized counts, scaler dict for denormalization
    """
    counts = np.array(counts, dtype='float32')
    
    if method == 'standard':
        mean = np.mean(counts)
        std = np.std(counts)
        normalized = (counts - mean) / (std + 1e-7)
        scaler = {'mean': mean, 'std': std, 'method': 'standard'}
    elif method == 'minmax':
        min_val = np.min(counts)
        max_val = np.max(counts)
        normalized = (counts - min_val) / (max_val - min_val + 1e-7)
        scaler = {'min': min_val, 'max': max_val, 'method': 'minmax'}
    else:
        raise ValueError(f"Unknown normalization method: {method}")
    
    return normalized, scaler


def denormalize_counts(counts, scaler):
    """
    Denormalize count predictions using scaler.
    
    Args:
        counts: Normalized count values
        scaler: Dictionary with normalization parameters
    
    Returns:
        Denormalized counts
    """
    method = scaler.get('method', 'standard')
    
    if method == 'standard':
        return counts * scaler['std'] + scaler['mean']
    elif method == 'minmax':
        return counts * (scaler['max'] - scaler['min']) + scaler['min']
    else:
        raise ValueError(f"Unknown denormalization method: {method}")


def augment_image(image, flip=True, rotate=True, brightness=True):
    """
    Apply data augmentation to image.
    
    Args:
        image: Input image (numpy array)
        flip: Whether to apply horizontal flip
        rotate: Whether to apply rotation
        brightness: Whether to adjust brightness
    
    Returns:
        Augmented image
    """
    img = image.copy()
    
    if flip and np.random.rand() > 0.5:
        img = cv2.flip(img, 1)
    
    if rotate and np.random.rand() > 0.5:
        angle = np.random.uniform(-15, 15)
        h, w = img.shape[:2]
        M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
        img = cv2.warpAffine(img, M, (w, h))
    
    if brightness and np.random.rand() > 0.5:
        factor = np.random.uniform(0.8, 1.2)
        img = np.clip(img * factor, 0, 255).astype(img.dtype)
    
    return img


def create_image_dataset(image_dir, count_dict, target_size=(224, 224), 
                        normalize=True, augment=False):
    """
    Create dataset from image directory and counts.
    
    Args:
        image_dir: Directory containing images
        count_dict: Dict mapping image filename to count
        target_size: Image size
        normalize: Whether to normalize
        augment: Whether to apply augmentation
    
    Returns:
        Tuple of (images, counts)
    """
    images = []
    counts = []
    
    image_dir = Path(image_dir)
    for img_file in image_dir.glob('*'):
        if img_file.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
            continue
        
        filename = img_file.name
        if filename not in count_dict:
            continue
        
        try:
            img = load_image(str(img_file), target_size)
            img = preprocess_image(img, normalize)
            
            if augment:
                img = augment_image(img)
            
            images.append(img)
            counts.append(count_dict[filename])
        except Exception as e:
            print(f"Error loading {filename}: {e}")
    
    return np.array(images), np.array(counts, dtype='float32')


def split_dataset(images, counts, train_ratio=0.7, val_ratio=0.15):
    """
    Split dataset into train, validation, and test sets.
    
    Args:
        images: Array of images
        counts: Array of counts
        train_ratio: Proportion for training
        val_ratio: Proportion for validation
    
    Returns:
        Tuple of (X_train, X_val, X_test, y_train, y_val, y_test)
    """
    n_samples = len(images)
    indices = np.random.permutation(n_samples)
    
    train_idx = int(n_samples * train_ratio)
    val_idx = int(n_samples * (train_ratio + val_ratio))
    
    train_indices = indices[:train_idx]
    val_indices = indices[train_idx:val_idx]
    test_indices = indices[val_idx:]
    
    X_train = images[train_indices]
    X_val = images[val_indices]
    X_test = images[test_indices]
    
    y_train = counts[train_indices]
    y_val = counts[val_indices]
    y_test = counts[test_indices]
    
    return X_train, X_val, X_test, y_train, y_val, y_test