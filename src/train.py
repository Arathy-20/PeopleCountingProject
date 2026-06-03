import numpy as np
from model import build_model
import json
import os

# Set up paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
x_train = np.load(os.path.join(project_root, "x.npy"))
y_train = np.load(os.path.join(project_root, "y.npy"))

x_test = np.load(os.path.join(project_root, "x_test.npy"))
y_test = np.load(os.path.join(project_root, "y_test.npy"))

print("Training data shape:", x_train.shape)
print("Training labels shape:", y_train.shape)

print("Testing data shape:", x_test.shape)
print("Testing labels shape:", y_test.shape)

indices = np.random.permutation(len(x_train))
x_train = x_train[indices]
y_train = y_train[indices]

model = build_model()

history = model.fit(
    x_train,
    y_train,
    epochs=100,
    batch_size=8,
    validation_data=(x_test, y_test)
)
# Create models directory if it doesn't exist
models_dir = os.path.join(project_root, "models")
os.makedirs(models_dir, exist_ok=True)

history_path = os.path.join(project_root, "history.json")

with open(history_path, "w") as f:
    json.dump(history.history,f)

print("history saved")

model_path = os.path.join(models_dir, "people_counter.h5")

model.save(model_path)
print("model saved!")
