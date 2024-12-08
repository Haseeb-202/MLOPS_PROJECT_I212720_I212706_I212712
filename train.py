import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import pickle
import os

def preprocess_data(file_path):
    """Load and preprocess the data from a CSV file."""
    # Load the CSV file
    data = pd.read_csv(file_path)

    # One-hot encode the 'Condition' column
    data = pd.get_dummies(data, columns=["Condition"], drop_first=True)

    # Define features and target
    X = data[["Humidity", "Wind Speed"] + [col for col in data.columns if col.startswith("Condition_")]]
    y = data["Temperature"]

    return X, y

def train_and_log_model(X_train, y_train, X_test, y_test):
    """Train the model, evaluate, and log it with MLflow, including storing a .pkl file."""
    with mlflow.start_run():
        # Log parameters
        fit_intercept = True
        mlflow.log_param("fit_intercept", fit_intercept)
        
        # Initialize and train the model
        model = LinearRegression(fit_intercept=fit_intercept)
        model.fit(X_train, y_train)

        # Evaluate metrics
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Log metrics
        mlflow.log_metric("mean_squared_error", mse)
        mlflow.log_metric("mean_absolute_error", mae)
        mlflow.log_metric("r2_score", r2)
        print(f"Metrics logged: MSE={mse}, MAE={mae}, R²={r2}")

        # Log the model with input/output signature
        signature = infer_signature(X_train, model.predict(X_train))
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="linear-regression-model",
            signature=signature,
            input_example=X_train.iloc[0:1]
        )
        print(f"Model logged with run ID: {mlflow.active_run().info.run_id}")

        # Save the model as a .pkl file
        pkl_file_path = "linear_regression_model.pkl"
        with open(pkl_file_path, "wb") as pkl_file:
            pickle.dump(model, pkl_file)
        
        # Log the .pkl file as an artifact
        mlflow.log_artifact(pkl_file_path, artifact_path="artifacts")
        print(f"Model saved and logged as artifact: {pkl_file_path}")

        # Clean up the .pkl file from the local directory if needed
        if os.path.exists(pkl_file_path):
            os.remove(pkl_file_path)

def main():
    # Setup MLflow
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("Temperature Prediction Experiment")
    
    # Path to the dataset
    file_path = "processed_forecast_data.csv"
    
    # Preprocess the data
    X, y = preprocess_data(file_path)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train and log the model
    train_and_log_model(X_train, y_train, X_test, y_test)

if __name__ == "__main__":
    main()
