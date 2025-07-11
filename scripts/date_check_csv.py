import pandas as pd

# Load your CSV (adjust the file path if needed)
df = pd.read_csv(r'output\market_data_with_names_merged.csv')

# Make sure your date column is parsed as datetime
df['date'] = pd.to_datetime(df['date'])

# Get the latest date
latest_date = df['date'].max()
print("Latest date in CSV:", latest_date)
