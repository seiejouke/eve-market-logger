import pandas as pd
import os
from glob import glob

# ---------- CONFIGURATION ----------
INV_TYPES_CSV = r"C:\Users\Jouke\Documents\evedata-logger\output\inv_types.csv"
INPUT_FOLDER  = r"C:\Users\Jouke\Documents\evedata-logger\output\market_groups\Hypercore"
OUTPUT_FOLDER = r"C:\Users\Jouke\Documents\evedata-logger\output\market_groups\PLEX"
CSV_GLOB      = "*.csv"   # All CSVs in the input folder
# -----------------------------------

# Load type_id → type_name mapping
inv_types = pd.read_csv(INV_TYPES_CSV, dtype={'type_id': int, 'type_name': str})
id_to_name = dict(zip(inv_types['type_id'], inv_types['type_name']))

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Batch process each CSV
input_csvs = glob(os.path.join(INPUT_FOLDER, CSV_GLOB))
print(f"Found {len(input_csvs)} CSV files to process.")

for input_csv in input_csvs:
    try:
        df = pd.read_csv(input_csv)
        if 'type_id' not in df.columns:
            print(f"Skipping {input_csv}: no type_id column.")
            continue
        # Get type_id from the file (assume it's the same for all rows)
        type_id = df['type_id'].iloc[0]
        type_name = id_to_name.get(type_id, "Unknown")
        df['type_name'] = type_name

        # Reorder/select columns
        output_columns = ['type_id', 'type_name', 'date', 'volume', 'average', 'highest', 'lowest']
        for col in output_columns:
            if col not in df.columns:
                print(f"Skipping {input_csv}: missing column {col}.")
                break
        else:
            # Write to output with same filename
            base = os.path.basename(input_csv)
            output_csv = os.path.join(OUTPUT_FOLDER, base)
            df_out = df[output_columns]
            df_out.to_csv(output_csv, index=False)
            print(f"Processed: {input_csv} → {output_csv}")
    except Exception as e:
        print(f"Error processing {input_csv}: {e}")

print("Batch cleanup complete.")
