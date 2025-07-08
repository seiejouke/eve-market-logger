import json
with open('.secrets.baseline', 'r', encoding='utf-8') as f:
    data = json.load(f)
print("Success! Baseline loaded.")
