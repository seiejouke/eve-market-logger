import pandas as pd
import glob
import os

output_dir = "output/"
# ONLY merge market history files—exclude mapping/statistics if needed!
csvs = [
    f for f in glob.glob(os.path.join(output_dir, "*.csv"))
    if "liquidity" not in f.lower()
    and "all_item_type" not in f.lower()
    and "type_id_to_name" not in f.lower()
    and "median" not in f.lower()
]

print("Merging these files:")
for f in csvs:
    print(" -", os.path.basename(f))

dfs = [pd.read_csv(f) for f in csvs]
merged = pd.concat(dfs, ignore_index=True)

# Remove duplicates: by type_id and date (recommended)
if "date" in merged.columns:
    merged.drop_duplicates(subset=['type_id', 'date'], keep='last', inplace=True)
    merged.sort_values(by=['type_id', 'date'], inplace=True)
else:
    # If no date column, just by type_id
    merged.drop_duplicates(subset=['type_id'], keep='last', inplace=True)
    merged.sort_values(by=['type_id'], inplace=True)

merged_file = os.path.join(output_dir, "market_data_with_names_merged.csv")
merged.to_csv(merged_file, index=False)

print(f"\n✅ Done! Merged CSV saved as: {merged_file}")
print(f"Rows in merged file: {len(merged)}")
print(f"Columns: {merged.columns.tolist()}")
