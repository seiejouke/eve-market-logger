import glob
import os
import pandas as pd

# Directory where your batch CSVs live
BATCH_DIR = "output/market_history"
OUT_FILE  = "output/market_history_all.csv"

# Find all batch files
batch_files = sorted(glob.glob(os.path.join(BATCH_DIR, "market_history_batch_*.csv")))

# Optionally filter out any remaining empty files
batch_files = [f for f in batch_files if os.path.getsize(f) > 0]

print(f"Combining {len(batch_files)} batch files...")

# Read and concatenate
df_list = []
for f in batch_files:
    df = pd.read_csv(f)
    df_list.append(df)

df_all = pd.concat(df_list, ignore_index=True)

# Write the combined CSV
os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
df_all.to_csv(OUT_FILE, index=False)

print(f"✅ Wrote combined market history ({len(df_all)} rows) to `{OUT_FILE}`")
