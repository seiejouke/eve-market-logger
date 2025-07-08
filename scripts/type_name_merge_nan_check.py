import pandas as pd

merged_df = pd.read_csv('output/market_data_with_names_merged.csv')

missing_names = merged_df[merged_df['type_name'].isnull()]

print(f"Number of missing type_name values: {len(missing_names)}")

