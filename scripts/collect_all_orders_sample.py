import requests
import pandas as pd
import time

REGION_ID = 10000002  # The Forge
ITEM_LIMIT = 100
BASE_URL = "https://esi.evetech.net/latest"
HEADERS = {"User-Agent": "EVE-Market-Logger/1.0"}

# Step 1: Get type IDs (tradable market types)
type_url = f"{BASE_URL}/markets/{REGION_ID}/types/"
res = requests.get(type_url, headers=HEADERS)
type_ids = res.json()[:ITEM_LIMIT]  # limit to first 100 for testing

all_orders = []

# Step 2: Fetch ALL buy/sell orders for each item
for idx, type_id in enumerate(type_ids, 1):
    print(f"[{idx}/{ITEM_LIMIT}] Fetching orders for type_id: {type_id}")
    
    order_url = f"{BASE_URL}/markets/{REGION_ID}/orders/?type_id={type_id}"
    response = requests.get(order_url, headers=HEADERS)

    if response.status_code != 200:
        print(f"  Error fetching type_id {type_id}")
        continue

    orders = response.json()

    for order in orders:
        all_orders.append({
            "type_id": type_id,
            "order_id": order.get("order_id"),
            "is_buy_order": order.get("is_buy_order"),
            "price": order.get("price"),
            "volume_remain": order.get("volume_remain"),
            "volume_total": order.get("volume_total"),
            "location_id": order.get("location_id"),
            "duration": order.get("duration"),
            "issued": order.get("issued"),
            "min_volume": order.get("min_volume"),
            "range": order.get("range"),
            "system_id": order.get("system_id"),
            "type_id_confirmed": order.get("type_id")  # confirm ESI echoes it
        })

    time.sleep(0.3)  # to avoid rate limiting

# Step 3: Save all orders to CSV
df = pd.DataFrame(all_orders)
df.to_csv("forge_region_orders_sample.csv", index=False)

print(f"Saved {len(df)} total orders for {ITEM_LIMIT} items to 'forge_region_orders_sample.csv'")