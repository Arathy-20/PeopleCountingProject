import cv2
import numpy as np
import tensorflow as tf
import os

model = tf.keras.models.load_model("models/people_counter.h5")

folder_path = "dataset/test_images"

print("\nPrediction :\n")

for file in os.listdir(folder_path):
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
        img_path = os.path.join(folder_path, file)

        img = cv2.imread(img_path)

        if img is None:
            print(f"Could not read image: {img_path}")
            continue

        img = cv2.resize(img, (224, 224))
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)

        print("input shape", img.shape)

        prediction = model.predict(img, verbose=0)
        print(f"{file} -> Predicted count: {prediction[0][0]:.2f}people")