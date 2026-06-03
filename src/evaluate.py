import numpy as np
import tensorflow as tf
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
import os

# Set up paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load model
model_path = os.path.join(project_root, "models", "people_counter.h5")
model = tf.keras.models.load_model(model_path)

# Load test dataset
x_test = np.load(os.path.join(project_root, "x_test.npy"))
y_test = np.load(os.path.join(project_root, "y_test.npy"))

print("test images:", len(x_test))

predictions = model.predict(x_test)
print("predictions shape", predictions.shape)

# Flatten predictions if needed
predictions_flat = predictions.flatten() if len(predictions.shape) > 1 else predictions
mae = mean_absolute_error(y_test, predictions_flat)
print("MAE:", mae)

rmse = np.sqrt(mean_squared_error(y_test, predictions_flat))
print("RMSE:", rmse)

for i in range(10):
    print(
        "Actual:",
        y_test[i],
        "predicted",
        int(predictions[i][0])
    )

#Record results

print("\n FINAL RESULTS")
print("MAE:",mae)
print("RMSE:", rmse)