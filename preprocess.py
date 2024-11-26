import pandas as pd

# Load the data
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
