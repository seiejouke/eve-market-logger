import pandas as pd
import os

# --- Paths ---
recent_path = os.path.join('output', 'market_history', 'update_2025-06-30.csv')
full_path   = os.path.join('output', 'market_data_with_names.csv')
output_path = os.path.join('output', 'market_data_with_names_merged.csv')

# --- Load dataframes ---
try:
    df_recent = pd.read_csv(recent_path, parse_dates=['date'])
except FileNotFoundError:
    print(f"❌ Recent 7-day file not found: {recent_path}")
    exit(1)

try:
    df_full = pd.read_csv(full_path, parse_dates=['date'])
except FileNotFoundError:
    print(f"❌ 365-day (full) file not found: {full_path}")
    exit(1)

# --- Attach names to recent data if missing ---
if 'name' not in df_recent.columns and 'name' in df_full.columns:
    df_recent = df_recent.merge(
        df_full[['type_id', 'name']].drop_duplicates(),
        on='type_id',
        how='left'
    )

# --- Combine and deduplicate ---
combined = pd.concat([df_full, df_recent], ignore_index=True)
combined.drop_duplicates(subset=['type_id', 'date'], keep='last', inplace=True)
combined.sort_values(by=['type_id', 'date'], inplace=True)

# --- Save merged file ---
combined.to_csv(output_path, index=False)
print(f"✅ Merged history with names saved as: {output_path}")
print(f"Total unique rows: {len(combined)}")

# --- Optional: report missing names, if any ---
if 'name' in combined.columns:
    missing_names = combined['name'].isna().sum()
    if missing_names > 0:
        print(f"⚠️ {missing_names} rows have missing names.")
