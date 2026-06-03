import tensorflow as tf
Sequential = tf.keras.Sequential
Dense = tf.keras.layers.Dense
Conv2D = tf.keras.layers.Conv2D
BatchNormalization = tf.keras.layers.BatchNormalization
MaxPooling2D = tf.keras.layers.MaxPooling2D
Dropout = tf.keras.layers.Dropout
GlobalAveragePooling2D = tf.keras.layers.GlobalAveragePooling2D

def build_model() -> tf.keras.Model:
    model = Sequential(name="CrowdCountingCNN")

    # Block1 : Low level features

    model.add(Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(224, 224, 3),name="Conv1"))
    model.add(BatchNormalization(name="bn1"))
    model.add(MaxPooling2D((2, 2), name="pool1"))
    
    # Block2 : Mid level features

    model.add(Conv2D(64, (3, 3), activation='relu', padding='same', name="Conv2"))
    model.add(BatchNormalization(name="bn2"))
    model.add(MaxPooling2D((2, 2), name="pool2"))
   
    # Block3 : High level features    

    model.add(Conv2D(128, (3, 3), activation='relu', padding='same', name="Conv3"   ))
    model.add(BatchNormalization(name="bn3"))
    model.add(MaxPooling2D((2, 2), name="pool3"))
    
    # Block4 : Abstract features

    model.add(Conv2D(256, (3, 3), activation='relu', padding='same', name="Conv4"   ))
    model.add(BatchNormalization(name="bn4"))
    model.add(MaxPooling2D((2, 2), name="pool4"))

    model.add(Conv2D(512, (3, 3), activation='relu', padding='same', name="Conv5"   ))
    model.add(BatchNormalization(name="bn5"))

    model.add(GlobalAveragePooling2D(name="gap"))

    # FC layers
    model.add(Dense(512, activation='relu', name="fc1"))
    model.add(Dropout(0.5, name="drop0"))
    model.add(Dense(256, activation='relu', name="fc2"))
    model.add(Dropout(0.4, name="drop1"))
    model.add(Dense(128, activation='relu', name="fc3"))
    model.add(Dropout(0.3, name="drop2"))
    model.add(Dense(64, activation='relu', name="fc4"))
    model.add(Dropout(0.2, name="drop3"))

    # Output layer
    model.add(Dense(1, activation='linear', name="output"))

    # Adam + MSE + MAE
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4), loss='mean_squared_error', metrics=['mean_absolute_error'])
    
    return model

if __name__ == "__main__":
    model = build_model()
    model.summary()