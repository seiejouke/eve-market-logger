#Data builder, keeping up with the market- non-auto, change as needed manually

#!/usr/bin/env python3
import asyncio
import aiohttp
import pandas as pd
import time
import os
from datetime import datetime

# ─── Configuration ─────────────────────────────────────────────
REGION_ID        = 10000002  # The Forge
MAX_CONCURRENT   = 5
DELAY            = 1.2       # seconds between requests per worker
HISTORY_DAYS     = 1         # Fetch last x days for update/backfill
INPUT_TYPE_IDS   = 'output/inv_types.csv'
OUTPUT_DIR       = 'output'
CANONICAL_CSV    = 'output/market_data_with_names_merged.csv'

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs('output', exist_ok=True)  # Ensure output/ always exists

# ─── Async Fetcher ─────────────────────────────────────────────
async def fetch_history(session, semaphore, type_id):
    url     = f"https://esi.evetech.net/latest/markets/{REGION_ID}/history/?type_id={type_id}"
    headers = {'User-Agent': 'eve-market-history-pipeline'}
    async with semaphore:
        await asyncio.sleep(DELAY)  # Space out requests to avoid bursts
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                print(f"[{resp.status}] Error for type_id {type_id}")
                return []
            data = await resp.json()
            recent = data[-HISTORY_DAYS:]
            return [
                {
                    'type_id':  type_id,
                    'date':     d['date'],
                    'volume':   d['volume'],
                    'average':  d['average'],
                    'highest':  d['highest'],
                    'lowest':   d['lowest'],
                }
                for d in recent
            ]

async def backfill(type_ids):
    sem = asyncio.Semaphore(MAX_CONCURRENT)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_history(session, sem, tid) for tid in type_ids]
        chunks = await asyncio.gather(*tasks)
    # flatten list of lists
    records = [r for chunk in chunks for r in chunk]
    return pd.DataFrame(records)

# ─── Helpers ───────────────────────────────────────────────────
def load_type_ids(path):
    df = pd.read_csv(path)
    return df['type_id'].astype(int).tolist()

# ─── Main ──────────────────────────────────────────────────────
def main():
    start = time.time()

    # Load item IDs
    type_ids = load_type_ids(INPUT_TYPE_IDS)
    print(f"→ Loaded {len(type_ids)} type IDs from {INPUT_TYPE_IDS}")

    # Fetch HISTORY_DAYS days of history for all items
    print(f"→ Fetching {HISTORY_DAYS}-day history for region {REGION_ID} with {MAX_CONCURRENT} workers…")
    df = asyncio.run(backfill(type_ids))

    # Write snapshot
    today = datetime.utcnow().strftime("%Y-%m-%d")
    snapshot = os.path.join(OUTPUT_DIR, f"update_{today}.csv")
    df.to_csv(snapshot, index=False)
    print(f"→ Saved snapshot ({len(df)} rows) to {snapshot}")

    # --- Merge with canonical backlog ---
    if os.path.exists(CANONICAL_CSV):
        df_canon = pd.read_csv(CANONICAL_CSV, parse_dates=['date'])
        combined = pd.concat([df_canon, df], ignore_index=True)
        combined.drop_duplicates(subset=['type_id', 'date'], keep='last', inplace=True)
        combined.sort_values(by=['type_id', 'date'], inplace=True)
    else:
        combined = df.copy()

    combined.to_csv(CANONICAL_CSV, index=False)
    print(f"Updated backlog saved as: {CANONICAL_CSV}")

    print(f"Done in {time.time() - start:.2f}s")

if __name__ == "__main__":
    main()
