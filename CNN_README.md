# CNN Architecture for People Counting

Custom CNN model for predicting the number of people in images using regression.

## Architecture Overview

### Model Layers
- **Conv Block 1**: 32 filters → MaxPool → Dropout(0.25)
- **Conv Block 2**: 64 filters → MaxPool → Dropout(0.25)
- **Conv Block 3**: 128 filters → MaxPool → Dropout(0.25)
- **Conv Block 4**: 256 filters → MaxPool → Dropout(0.25)
- **Global Average Pooling**
- **Dense Layers**: 512 → 256 → 128 → 1 (output)
- **Activation**: ReLU (hidden), Linear (output)
- **Loss**: Mean Squared Error (MSE)
- **Optimizer**: Adam

### Lightweight Model
For faster training/inference with fewer parameters:
- 3 Conv blocks instead of 4
- Fewer dense layers
- Same regression output

## Files

- `cnn_model.py` - Model architecture definitions
- `utils.py` - Data loading and preprocessing utilities
- `train_model.py` - Training pipeline and trainer class
- `predict.py` - Inference and prediction script
- `evaluate.py` - Evaluation metrics and visualization

## Usage

### 1. Prepare Dataset

Create `dataset/images/` directory with images and `dataset/counts.json`:

```json
{
  "image1.jpg": 25,
  "image2.jpg": 42,
  "image3.jpg": 18
}
```

### 2. Training

```python
python src/train_model.py
```

Trains the model and saves:
- `models/people_counter_YYYYMMDD_HHMMSS.h5` - Trained model
- `models/scaler_YYYYMMDD_HHMMSS.json` - Normalization parameters
- `models/metrics_YYYYMMDD_HHMMSS.json` - Training metrics

### 3. Prediction

Single image:
```bash
python src/predict.py --model models/people_counter_YYYYMMDD_HHMMSS.h5 \
                      --scaler models/scaler_YYYYMMDD_HHMMSS.json \
                      --image path/to/image.jpg \
                      --output predictions.json
```

Directory of images:
```bash
python src/predict.py --model models/people_counter_YYYYMMDD_HHMMSS.h5 \
                      --scaler models/scaler_YYYYMMDD_HHMMSS.json \
                      --directory path/to/images/ \
                      --output predictions.json
```

### 4. Evaluation

```python
from evaluate import evaluate_predictions
import numpy as np

y_true = np.array([10, 25, 30, 45])
y_pred = np.array([12, 24, 32, 44])

metrics = evaluate_predictions(
    y_true, y_pred,
    output_json='metrics.json',
    plot_output='evaluation.png'
)
```

## Python API

### Training

```python
from train_model import PeopleCountingTrainer
from utils import create_image_dataset, split_dataset

# Create trainer
trainer = PeopleCountingTrainer(model_name='standard', learning_rate=0.001)

# Load and split data
images, counts = create_image_dataset('dataset/images', count_dict)
X_train, X_val, X_test, y_train, y_val, y_test = split_dataset(images, counts)

# Train
trainer.train(X_train, y_train, X_val, y_val, epochs=50, batch_size=32)

# Evaluate
metrics, predictions = trainer.evaluate(X_test, y_test)

# Save
trainer.save_model('model.h5')
trainer.save_scaler('scaler.json')
```

### Prediction

```python
from predict import PeopleCounter

counter = PeopleCounter('model.h5', 'scaler.json')

# Single image
count = counter.predict_image('image.jpg')
print(f"Predicted count: {count:.2f}")

# Multiple images
counts = counter.predict_batch(['img1.jpg', 'img2.jpg'])

# Directory
results = counter.predict_directory('path/to/images/')
```

## Evaluation Metrics

- **MAE** (Mean Absolute Error): Average prediction error
- **MSE** (Mean Squared Error): Penalizes larger errors
- **RMSE** (Root Mean Squared Error): Same units as target
- **MAPE** (Mean Absolute Percentage Error): Percentage error
- **R²** (Coefficient of Determination): Model fit quality

## Configuration

Modify in `train_model.py`:
- `image_dir`: Path to images
- `input_shape`: Image size (default: 224×224×3)
- `learning_rate`: Optimizer learning rate
- `epochs`: Number of training epochs
- `batch_size`: Batch size for training
- `train_ratio`: Train/val/test split ratios

## Dependencies

- TensorFlow/Keras ≥ 2.21
- NumPy ≥ 2.4
- OpenCV ≥ 4.13
- Matplotlib ≥ 3.10