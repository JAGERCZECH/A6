import os
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

# Load and preprocess data
def load_data():
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    X_train = X_train.reshape((X_train.shape[0], 28 * 28)).astype("float32") / 255
    X_test = X_test.reshape((X_test.shape[0], 28 * 28)).astype("float32") / 255
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)
    return X_train, X_test, y_train, y_test

# Build the model
def build_model():
    model = models.Sequential([
        layers.Dense(128, activation="relu", input_shape=(28 * 28,)),
        layers.Dense(64, activation="relu"),
        layers.Dense(10, activation="softmax")
    ])
    model.compile(optimizer="adam",
                  loss="categorical_crossentropy",
                  metrics=["accuracy"])
    return model

# Train the model
def train_model(model, X_train, y_train):
    model.fit(X_train, y_train, epochs=5, batch_size=64, validation_split=0.2)

# Evaluate the model
def evaluate_model(model, X_test, y_test):
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {test_acc}")

# Make predictions
def make_predictions(model, X_test):
    predictions = model.predict(X_test)
    print("Predictions for the first test sample:")
    print(predictions[0])

#main menu
def main():
    X_train, X_test, y_train, y_test = load_data()
    model = None

    while True:
        print("\n--- MENU ---")
        print("1. Train the Model")
        print("2. Evaluate the Model")
        print("3. Make Predictions")
        print("4. Visualize Prediction")
        print("5. Save the Model")
        print("6. Load the Model")
        print("7. Configure Hyperparameters")
        print("8. Export Predictions")
        print("9. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("Training the model...")
            model = build_model()
            train_model(model, X_train, y_train)
        elif choice == "2":
            if model:
                print("Evaluating the model...")
                evaluate_model(model, X_test, y_test)
            else:
                print("Error: No model loaded. Please train or load a model first.")
        elif choice == "3":
            if model:
                print("Making predictions...")
                make_predictions(model, X_test)
            else:
                print("Error: No model loaded. Please train or load a model first.")
        elif choice == "4":
            if model:
                index = int(input("Enter the index of the test sample (0-9999): "))
                visualize_prediction(model, X_test, y_test, index)
            else:
                print("Error: No model loaded. Please train or load a model first.")
        elif choice == "5":
            if model:
                save_model(model)
            else:
                print("Error: No model loaded. Please train or load a model first.")
        elif choice == "6":
            model = load_model()
        elif choice == "7":
            hidden_units = int(input("Enter the number of hidden units: "))
            learning_rate = float(input("Enter the learning rate: "))
            model = build_custom_model(28 * 28, 10, hidden_units, learning_rate)
            print("Model configured with custom hyperparameters.")
        elif choice == "8":
            if model:
                export_predictions(model, X_test)
            else:
                print("Error: No model loaded. Please train or load a model first.")
        elif choice == "9":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Visualization
def visualize_prediction(model, X_test, y_test, index=0):
    # Get the image and label
    image = X_test[index].reshape(28, 28)
    true_label = tf.argmax(y_test[index]).numpy()

    # Make a prediction
    prediction = model.predict(tf.expand_dims(X_test[index], axis=0))
    predicted_label = tf.argmax(prediction).numpy()

    # Display the image and prediction
    plt.imshow(image, cmap="gray")
    plt.title(f"True Label: {true_label}, Predicted Label: {predicted_label}")
    plt.show()

# Save the model
def save_model(model, filename="mnist_model.keras"):
    model.save(filename)
    print(f"Model saved to {filename}")

# Load the model
def load_model(filename="mnist_model.keras"):
    if os.path.exists(filename):
        model = tf.keras.models.load_model(filename)
        print(f"Model loaded from {filename}")
        return model
    else:
        print(f"Error: File {filename} not found.")
        return None

#Hyperparameter Tuning
def build_custom_model(input_shape, num_classes, hidden_units=128, learning_rate=0.001):
    model = models.Sequential([
        layers.Dense(hidden_units, activation="relu", input_shape=(input_shape,)),
        layers.Dense(hidden_units // 2, activation="relu"),
        layers.Dense(num_classes, activation="softmax")
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                  loss="categorical_crossentropy",
                  metrics=["accuracy"])
    return model

def export_predictions(model, X_test, filename="predictions.csv"):
    predictions = model.predict(X_test)
    predicted_labels = tf.argmax(predictions, axis=1).numpy()
    df = pd.DataFrame({"Predicted Label": predicted_labels})
    df.to_csv(filename, index=False)
    print(f"Predictions exported to {filename}")

# Run the program
if __name__ == "__main__":
    main()
