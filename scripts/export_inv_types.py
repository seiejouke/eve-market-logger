#The csv equivalant of your DB! 

import pandas as pd
from sqlalchemy import create_engine

# --- Database config ---
DB_URI = "postgresql+psycopg2://postgres:109009885@localhost:5432/eve_data"

# --- Connect & load inv_types ---
engine = create_engine(DB_URI)
df = pd.read_sql("SELECT type_id, type_name FROM inv_types ORDER BY type_id;", engine)

# --- Save to CSV ---
output_csv = "output/inv_types.csv"
df.to_csv(output_csv, index=False)
print(f"✅ Exported {len(df)} rows to {output_csv}")
