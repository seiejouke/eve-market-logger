import pandas as pd
from sqlalchemy import create_engine

# Connect to your PostgreSQL database
engine = create_engine("postgresql+psycopg2://postgres:109009885@localhost:5432/eve_data")

# Query to get daily liquidity per item
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

# Load and process
df = pd.read_sql(query, engine)
median_liquidity = df.groupby('type_id')['daily_liquidity'].median().reset_index()
median_liquidity.rename(columns={'daily_liquidity': 'median_daily_liquidity'}, inplace=True)

# Save to CSV or inspect
median_liquidity.to_csv("median_daily_liquidity.csv", index=False)
print(median_liquidity.head())
