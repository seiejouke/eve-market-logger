import pandas as pd
import glob
import os

# Build full path regardless of where you run it
script_dir = os.path.dirname(__file__)
batch_dir = os.path.abspath(os.path.join(script_dir, "..", "output", "market_history"))

all_files = glob.glob(os.path.join(batch_dir, "market_history_batch_*.csv"))

if not all_files:
    print("❌ No batch files found.")
else:
    df = pd.concat((pd.read_csv(f) for f in all_files)).drop_duplicates()
    output_path = os.path.abspath(os.path.join(script_dir, "..", "output", "market_data.csv"))
    df.to_csv(output_path, index=False)
    print(f"✅ Merged {len(all_files)} files into market_data.csv with {len(df)} rows.")
