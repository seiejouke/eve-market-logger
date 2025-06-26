import os
import time
import math
import requests
import pandas as pd
from datetime import datetime

# === DEBUG: Print current working directory ===
print(f"[DEBUG] Current working directory: {os.getcwd()}")

# === CONFIGURATION ===
FORGE_REGION_ID   = 10000002         # The Forge region
BATCH_SIZE        = 1000             # Number of type_ids per CSV batch
SLEEP_BETWEEN     = 1.0              # Minimum seconds between API requests
MAX_RETRIES       = 5                # Max retries on errors/rate limits
BACKOFF_FACTOR    = 2                # Exponential backoff multiplier
OUTPUT_DIR        = "output/market_history"
INPUT_CSV         = "output/all_item_type_ids.csv"  # CSV with 'type_id' column

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
abs_output_dir = os.path.abspath(OUTPUT_DIR)
print(f"[DEBUG] Output directory: {abs_output_dir}")

# === LOAD ITEM TYPE IDs ===
print(f"[{datetime.now()}] Loading type IDs from {INPUT_CSV}")
df_ids = pd.read_csv(INPUT_CSV)
all_type_ids = df_ids['type_id'].tolist()
print(f"[{datetime.now()}] Loaded {len(all_type_ids)} type IDs")

# === ESI Endpoint Configuration ===
base_url = f"https://esi.evetech.net/latest/markets/{FORGE_REGION_ID}/history/"
headers  = {
    "Accept": "application/json",
    "User-Agent": "eve-market-logger by joukeseinstra"
}

# === HELPER: Save Batch to CSV ===
def save_batch(batch_no, data):
    df = pd.DataFrame(data)
    filename = os.path.join(abs_output_dir, f"market_history_batch_{batch_no}.csv")
    df.to_csv(filename, index=False)
    print(f"[{datetime.now()}] Saved batch {batch_no} with {len(df)} rows to: {filename}")
    print(f"[DEBUG] Files now in output dir: {os.listdir(abs_output_dir)}")

# === PROCESS IN BATCHES ===
total_batches = math.ceil(len(all_type_ids) / BATCH_SIZE)
print(f"[{datetime.now()}] Total batches to process: {total_batches}")

for batch_idx in range(total_batches):
    start = batch_idx * BATCH_SIZE
    batch_ids = all_type_ids[start:start + BATCH_SIZE]
    results = []
    print(f"\n[{datetime.now()}] Starting batch {batch_idx+1}/{total_batches} (type_id {batch_ids[0]}–{batch_ids[-1]})")

    for type_id in batch_ids:
        retries = 0
        while True:
            try:
                # Correctly pass type_id as query parameter
                resp = requests.get(
                    base_url,
                    params={"type_id": type_id},
                    headers=headers
                )
                status = resp.status_code
                if status == 404:
                    print(f"  [Warn] type_id {type_id}: 404 Not Found (no history)")
                    break
                if status in (420, 429):
                    retry_after = int(resp.headers.get("Retry-After", "10"))
                    print(f"  [Rate] type_id {type_id}: {status}, sleeping {retry_after}s")
                    time.sleep(retry_after)
                    retries += 1
                    if retries > MAX_RETRIES:
                        print(f"  [Error] type_id {type_id} exceeded max retries on rate limit")
                        break
                    continue
                resp.raise_for_status()
                # Parse JSON history data
                history = resp.json()
                for entry in history:
                    entry['type_id'] = type_id
                    results.append(entry)
                break

            except Exception as e:
                retries += 1
                wait = BACKOFF_FACTOR ** (retries - 1)
                print(f"  [Error] type_id {type_id}: {e} (retry {retries}/{MAX_RETRIES}), sleeping {wait}s")
                time.sleep(wait)
                if retries >= MAX_RETRIES:
                    print(f"  [Error] type_id {type_id} aborted after {MAX_RETRIES} retries")
                    break

        # Enforce minimum pacing
        time.sleep(SLEEP_BETWEEN)

    # Save this batch, even if results is empty
    save_batch(batch_idx+1, results)

print(f"[{datetime.now()}] ✅ Completed all {total_batches} batches.")
