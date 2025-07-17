import asyncio
import aiohttp
import pandas as pd
import os
from datetime import datetime, timezone

REGION_ID      = 10000002   # The Forge
DELAY          = 1.2
HISTORY_DAYS   = 365
OUTPUT_DIR     = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

MARKET_HISTORY_URL = f"https://esi.evetech.net/latest/markets/{REGION_ID}/history/?type_id={{}}"

async def fetch_history_for_type(session, type_id):
    url = MARKET_HISTORY_URL.format(type_id)
    await asyncio.sleep(DELAY)
    async with session.get(url, headers={'User-Agent': 'eve-market-history-pipeline'}) as resp:
        if resp.status != 200:
            print(f"[{resp.status}] Error for type_id {type_id}")
            return []
        data = await resp.json()
        if not data:
            print(f"No market data for type_id {type_id}")
            return []
        recent = data[-HISTORY_DAYS:]
        for d in recent:
            d['type_id'] = type_id
        return recent

async def main():
    type_ids = input("Enter one or more type IDs, separated by space: ").split()
    type_ids = [int(tid) for tid in type_ids]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_history_for_type(session, tid) for tid in type_ids]
        results = await asyncio.gather(*tasks)
        records = [item for sublist in results for item in sublist]
        if not records:
            print("No market data found.")
            return
        df = pd.DataFrame(records)
        finished = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M")
        outpath = os.path.join(OUTPUT_DIR, f"market_history_{'_'.join(map(str, type_ids))}_{finished}.csv")
        df.to_csv(outpath, index=False)
        print(f"Saved {len(df)} rows to {outpath}")

if __name__ == "__main__":
    asyncio.run(main())
