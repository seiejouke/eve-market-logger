# Don't forget a NaN check post-merge

import pandas as pd

market_df = pd.read_csv('output/market_data_with_names_merged.csv')

type_map = pd.read_csv('output/inv_types.csv')

print(market_df.columns)
print(type_map.columns)

# Standardize column names if needed
# type_map = type_map.rename(columns={'typeID': 'type_id', 'typeName': 'type_name'}) # GPT bloatware!

# Merge on type_id
merged_df = market_df.merge(type_map[['type_id', 'type_name']], on='type_id', how='left')


merged_df.to_csv('output/market_data_with_names_merged.csv', index=False)
