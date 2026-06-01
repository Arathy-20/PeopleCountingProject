import numpy as np
from model import build_model
import json
x_train = np.load("x.npy")
y_train = np.load("y.npy")

x_test = np.load("x_test.npy")
y_test = np.load("y_test.npy")

print("Train", x_train.shape)
print("Test",x_test.shape)

model = build_model()

history = model.fit(
    x_train,
    y_train,
    epochs=10,
    batch_size=8,
    validation_data=(x_test, y_test)
)
with open("history.json", "w") as f:
    json.dump(history.history,f)
print("history saved")
model.save("models/people_counter.h5" )
print("model saved!")
