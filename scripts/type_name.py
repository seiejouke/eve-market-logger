import pandas as pd
import os

# --- Config ---
INPUT_CSV = "output/market_data_with_names_merged.csv"
OUTPUT_CSV = "output/market_data_with_names_merged.csv"

# --- PostgreSQL connection string ---
from sqlalchemy import create_engine

DB_URI = "postgresql+psycopg2://postgres:109009885@localhost:5432/eve_data"

# --- Ensure output directory exists ---
os.makedirs("output", exist_ok=True)

# --- Load your market data (auto-detect date col if present) ---
df = pd.read_csv(INPUT_CSV, parse_dates=["date"] if "date" in pd.read_csv(INPUT_CSV, nrows=1).columns else None)

# --- Connect and get mapping ---
engine = create_engine(DB_URI)
type_map = pd.read_sql("SELECT type_id, type_name FROM inv_types;", engine)

# --- Merge type names ---
if 'type_name' in df.columns:
    df = df.merge(type_map, on="type_id", how="left", suffixes=('', '_map'))
    if 'type_name_map' in df.columns:
        df['type_name'] = df['type_name'].combine_first(df['type_name_map'])
        df.drop(columns=['type_name_map'], inplace=True)
else:
    df = df.merge(type_map, on="type_id", how="left")

# --- Check for missing names ---
missing = df['type_name'].isna().sum()
print(f"Rows still missing item names: {missing}")
if missing > 0:
    print("Example missing rows:")
    print(df[df['type_name'].isna()].head())

# --- Save final output ---
df.to_csv(OUTPUT_CSV, index=False)
print(f"✅ {OUTPUT_CSV} created with item names.")
