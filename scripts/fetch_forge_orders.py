import requests
import time
import psycopg2
from datetime import datetime

# ---- CONFIG ----
REGION_ID = 10000002  # The Forge
MAX_RETRIES = 5
SLEEP_BETWEEN_CALLS = 1  # seconds

# ---- DATABASE CONNECTION ----
conn = psycopg2.connect(
    dbname="eve_data",
    user="postgres",
    password="109009885",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# ---- CREATE STORAGE TABLE ----
cur.execute("""
    CREATE TABLE IF NOT EXISTS market_orders_snapshot (
        order_id BIGINT PRIMARY KEY,
        type_id INT,
        is_buy_order BOOLEAN,
        price NUMERIC,
        volume_remain INT,
        volume_total INT,
        issued TIMESTAMP,
        duration INT,
        system_id BIGINT,
        snapshot_time TIMESTAMP
    );
""")
conn.commit()

# ---- FETCH MARKET DATA PER PAGE ----
def fetch_page(region_id, page):
    url = f"https://esi.evetech.net/latest/markets/{region_id}/orders/"
    headers = {"User-Agent": "EVE-Liquidity-Fetcher"}
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, params={"order_type": "all", "page": page}, headers=headers)
            if response.status_code == 420:
                print("Rate limited. Sleeping...")
                time.sleep(10)
                continue
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error (attempt {attempt+1}):", e)
            time.sleep(2 * (attempt + 1))
    return []

# ---- FETCH AND INSERT ALL PAGES ----
print("Fetching market orders...")
snapshot_time = datetime.utcnow()
page = 1
inserted = 0

while True:
    print(f"Fetching page {page}...")
    orders = fetch_page(REGION_ID, page)
    if not orders:
        print("No more data.")
        break

    for order in orders:
        try:
            cur.execute("""
                INSERT INTO market_orders_snapshot (
                    order_id, type_id, is_buy_order, price, volume_remain,
                    volume_total, issued, duration, system_id, snapshot_time
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (order_id) DO NOTHING;
            """, (
                order["order_id"],
                order["type_id"],
                order["is_buy_order"],
                order["price"],
                order["volume_remain"],
                order["volume_total"],
                order["issued"],
                order["duration"],
                order["system_id"],
                snapshot_time
            ))
            inserted += 1
        except Exception as e:
            print("Error inserting order:", e)
            continue

    conn.commit()
    print(f"Inserted so far: {inserted}")
    page += 1
    time.sleep(SLEEP_BETWEEN_CALLS)

print(f"✅ Done fetching. Total inserted: {inserted}")
cur.close()
conn.close()
