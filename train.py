import gdown
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn

def download_data(url, output_path):
    """Download a dataset from a Google Drive shareable link."""
    gdown.download(url, output_path, quiet=False)

def load_data(file_path):
    """Load dataset into a pandas DataFrame."""
    return pd.read_csv(file_path)

def train_model(X_train, y_train):
    """Train a logistic regression model with MLflow tracking."""
    with mlflow.start_run():
        model = LogisticRegression()
        model.fit(X_train, y_train)
        
        # Log model
        mlflow.sklearn.log_model(model, "logistic-regression-model")
        
        return model

def evaluate_model(model, X_test, y_test):
    """Evaluate the model's accuracy and log the metric with MLflow."""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    mlflow.log_metric("accuracy", accuracy)
    return accuracy

def main():
    # Setup MLflow connection and experiment
    mlflow.set_tracking_uri("http://localhost:5001")  # Modify with your MLflow server's URI
    mlflow.set_experiment("Temperature Prediction Experiment")
    
    # Google Drive shareable link and desired download path
    file_url = 'https://drive.google.com/uc?id=FILE_ID'  # change according to your drive on which data is uploaded 
    file_path = 'data.csv'
    
    # Download the data
    download_data(file_url, file_path)
    
    # Load the data
    data = load_data(file_path)
    
    # Assuming the target variable is the last column
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = train_model(X_train, y_train)
    
    # Evaluate the model
    accuracy = evaluate_model(model, X_test, y_test)
    print(f'Model Accuracy: {accuracy:.2%}')

if __name__ == "__main__":
    main()
