#Update DB for potential missing id_type, item names, run to be on the safe side!
#Update DB for potential missing id_type, item names, run to be on the safe side!!
#Update DB for potential missing id_type, item names, run to be on the safe side!!!
#Update DB for potential missing id_type, item names, run to be on the safe side!!!!
#Update DB for potential missing id_type, item names, run to be on the safe side!!!!!

import requests
import time
import psycopg2

# ---- DATABASE CONFIG ----
conn = psycopg2.connect(
    dbname="eve_data",
    user="postgres",
    password="109009885",  # replace with your actual password
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# ---- CREATE TABLE IF NOT EXISTS ----
cur.execute("""
    CREATE TABLE IF NOT EXISTS inv_types (
        type_id INT PRIMARY KEY,
        type_name TEXT
    );
""")

# ---- PAGINATED FETCH OF ALL TYPE_IDS ----
print("Fetching all item type_ids from ESI (paginated)...")
type_ids_url = "https://esi.evetech.net/latest/universe/types/"
all_type_ids = []

# First page to discover total pages
resp = requests.get(type_ids_url, params={"page": 1})
resp.raise_for_status()
first_page_ids = resp.json()
all_type_ids.extend(first_page_ids)

# ESI tells you how many pages exist via the X-Pages header
total_pages = int(resp.headers.get("x-pages", 1))
print(f"ESI reports {total_pages} pages of results; each up to 1000 IDs.")

# Fetch pages 2…N
for page in range(2, total_pages + 1):
    resp = requests.get(type_ids_url, params={"page": page})
    resp.raise_for_status()
    batch_ids = resp.json()
    if not batch_ids:
        break
    all_type_ids.extend(batch_ids)
    print(f"  • fetched page {page}/{total_pages} ({len(batch_ids)} IDs)")
    time.sleep(0.2)  # small pause so you don't spike the API

print(f"Total type_ids gathered: {len(all_type_ids)}")

# ---- FETCH NAMES IN BATCHES (as before) ----
names_url   = "https://esi.evetech.net/latest/universe/names/"
batch_size  = 1000
inserted    = 0

for i in range(0, len(all_type_ids), batch_size):
    batch = all_type_ids[i : i + batch_size]
    try:
        r = requests.post(names_url, json=batch)
        r.raise_for_status()
        data = r.json()

        for entry in data:
            if entry["category"] == "inventory_type":
                cur.execute("""
                    INSERT INTO inv_types (type_id, type_name)
                    VALUES (%s, %s)
                    ON CONFLICT (type_id) DO NOTHING;
                """, (entry["id"], entry["name"]))

        conn.commit()
        inserted += len(data)
        print(f"Processed batch {i // batch_size + 1} — total inserted: {inserted}")
        time.sleep(1)

    except Exception as e:
        print(f"Error in batch {i // batch_size + 1}: {e}")
        time.sleep(5)

cur.close()
conn.close()
print("✅ Done loading all item names.")
# ---- END OF SCRIPT ----