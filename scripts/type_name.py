import pandas as pd
import psycopg2

# Step 1: Load your CSV
df = pd.read_csv("output/market_data.csv", parse_dates=["date"])

# Step 2: Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="eve_data",
    user="postgres",
    password="109009885",  # Replace if needed
    host="localhost",
    port="5432"
)

# Step 3: Load type_id → type_name mapping from DB
type_map = pd.read_sql("SELECT type_id, type_name FROM inv_types;", conn)

# Step 4: Merge item names into your CSV data
df = df.merge(type_map, on="type_id", how="left")

# Step 5: Save updated CSV (optional)
df.to_csv("output/market_data_with_names.csv", index=False)

conn.close()

print("✅ market_data_with_names.csv created with item names.")
