import pandas as pd

# 1. How EVE Online ESI History Works
#The ESI endpoint /markets/{region_id}/history/ returns one row per day, but with a time lag:
#The â€œmarket historyâ€ endpoint typically lags by 1â€“2 days behind the actual current day.
#When you fetch history, the â€œmost recentâ€ row is often yesterday or even the day before.
#The ESI API batches historical data and updates it once per day, usually with a delay.
#So, on July 12, the most recent history is almost always July 10 (sometimes July 11 if youâ€™re lucky, but July 12 will not appear until tomorrow or the day after).

# Load your CSV (adjust the file path if needed)
df = pd.read_csv(r'output/update_2025-07-13.csv')

# Robustly parse mixed date formats
df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True, errors='coerce')

# Report if any rows failed to parse
if df['date'].isnull().any():
    print("Warning: Some dates could not be parsed!")
    print(df[df['date'].isnull()])

# Get the latest date
latest_date = df['date'].max()
print("Latest date in CSV:", latest_date)

