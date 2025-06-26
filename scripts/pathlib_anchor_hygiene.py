#!/usr/bin/env python3
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

# --- DB CONFIG ---
engine = create_engine(
    "postgresql+psycopg2://postgres:109009885@localhost:5432/eve_data"
)

# --- SQL QUERY ---
query = """
SELECT 
    type_id,
    DATE(snapshot_time) AS snapshot_date,
    SUM(volume_remain * price) AS daily_liquidity
FROM 
    market_orders_snapshot
GROUP BY 
    type_id, snapshot_date
"""

# --- RUN QUERY ---
print("Running query to fetch and aggregate daily liquidity...")
df = pd.read_sql(query, engine)

# --- COMPUTE MEDIAN ---
median_liquidity = (
    df.groupby("type_id")["daily_liquidity"]
      .median()
      .reset_index()
      .rename(columns={"daily_liquidity": "median_daily_liquidity"})
)

# --- DETERMINE PROJECT ROOT & OUTPUT PATH ---
# __file__ is scripts/analyze_median_liquidity.py → go up two levels to project root
BASE_DIR = Path(__file__).resolve().parent.parent
output_dir = BASE_DIR / "output"
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "median_daily_liquidity.csv"

# --- SAVE TO CSV ---
median_liquidity.to_csv(output_path, index=False)
print(f"✅ Saved: {output_path.resolve()}")

# --- SHOW TOP 10 ---
print("\nTop 10 items by median liquidity:")
print(
    median_liquidity
    .sort_values(by="median_daily_liquidity", ascending=False)
    .head(10)
)
