from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG with the new name
dag = DAG(
    'weather_forecast',
    default_args=default_args,
    description='DAG for preprocessing weather data',
    schedule_interval=timedelta(days=1),
    catchup=False
)

# Define the task for data preprocessing
def preprocess_data():
    df = pd.read_csv('forecast_data.csv')

    # Select numeric columns for handling missing values with mean
    numeric_cols = ['Temperature', 'Humidity', 'Wind Speed']  # adjust this list based on your actual numeric columns
    df[numeric_cols] = df[numeric_cols].apply(lambda x: x.fillna(x.mean()), axis=0)

    # If there are non-numeric columns like 'Date and Time' or 'Condition', handle them separately if needed
    # For example, for categorical data like 'Condition', you might want to fill missing values with the mode:
    if 'Condition' in df.columns:
        df['Condition'] = df['Condition'].fillna(df['Condition'].mode()[0])

    # Save the preprocessed data
    df.to_csv('processed_forecast_data.csv', index=False)
    print("Processed data saved.")

# Create a PythonOperator to run the preprocessing task
preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag,
)

# Since it's a single task DAG, no need to set dependencies
