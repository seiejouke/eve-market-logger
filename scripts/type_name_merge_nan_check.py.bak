import pandas as pd

merged_df = pd.read_csv('output/update_2025-07-13.csv')

missing_names = merged_df[merged_df['type_name'].isnull()]

print(f"Number of missing type_name values: {len(missing_names)}")

