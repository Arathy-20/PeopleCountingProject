import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

# Load model
model = load_model("models/people_counter.h5")

# Load test dataset

x_test = np.load("x_test.npy")
y_test = np.load("y_test.npy")

print("test images:", len(x_test))

predictions = model.predict(x_test)
print("predictions shape", predictions.shape)

mae = mean_absolute_error(y_test,
                          predictions)
print("MAE:", mae)

rmse = np.sqrt(mean_squared_error(y_test, predictions))
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