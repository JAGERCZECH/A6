import tensorflow as tf
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

# Main menu
def main():
    X_train, X_test, y_train, y_test = load_data()
    model = build_model()

    while True:
        print("\n--- MENU ---")
        print("1. Train the Model")
        print("2. Evaluate the Model")
        print("3. Make Predictions")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("Training the model...")
            train_model(model, X_train, y_train)
        elif choice == "2":
            print("Evaluating the model...")
            evaluate_model(model, X_test, y_test)
        elif choice == "3":
            print("Making predictions...")
            make_predictions(model, X_test)
        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()
