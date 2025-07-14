#!/usr/bin/env python3
import asyncio
import aiohttp
import pandas as pd
import os
import difflib
from datetime import datetime, timezone

REGION_ID      = 10000002   # The Forge
MAX_CONCURRENT = 5
DELAY          = 1.2
HISTORY_DAYS   = 365
OUTPUT_DIR     = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

GROUPS_URL = "https://esi.evetech.net/latest/universe/groups/"
GROUP_DETAIL_URL = "https://esi.evetech.net/latest/universe/groups/{}"
TYPE_DETAIL_URL = "https://esi.evetech.net/latest/universe/types/{}"
MARKET_HISTORY_URL = f"https://esi.evetech.net/latest/markets/{REGION_ID}/history/?type_id={{}}"

async def get_json(session, url):
    async with session.get(url, headers={'User-Agent': 'eve-market-history-pipeline'}) as resp:
        if resp.status != 200:
            print(f"[{resp.status}] Error for URL: {url}")
            return None
        return await resp.json()

async def fetch_all_group_names(session):
    ids = await get_json(session, GROUPS_URL)
    group_names = []
    for gid in ids:
        group = await get_json(session, GROUP_DETAIL_URL.format(gid))
        group_names.append({'group_id': gid, 'group_name': group['name']})
        await asyncio.sleep(0.05)  # Fast, just names
    return pd.DataFrame(group_names)

async def get_types_in_group(session, group_id):
    group = await get_json(session, GROUP_DETAIL_URL.format(group_id))
    type_ids = group['types']
    items = []
    for tid in type_ids:
        typ = await get_json(session, TYPE_DETAIL_URL.format(tid))
        items.append({'type_id': tid, 'type_name': typ['name']})
        await asyncio.sleep(0.10)
    return pd.DataFrame(items)

async def fetch_history_for_type(session, semaphore, type_id, type_name, group_id, group_name):
    url = MARKET_HISTORY_URL.format(type_id)
    async with semaphore:
        await asyncio.sleep(DELAY)
        async with session.get(url, headers={'User-Agent': 'eve-market-history-pipeline'}) as resp:
            if resp.status != 200:
                print(f"[{resp.status}] Error for type_id {type_id} ({type_name})")
                return []
            data = await resp.json()
            if not data:
                print(f"No market data for {type_name} ({type_id})")
                return []
            recent = data[-HISTORY_DAYS:]
            return [
                {
                    'group_id': group_id,
                    'group_name': group_name,
                    'type_id':  type_id,
                    'type_name': type_name,
                    'date':     d['date'],
                    'volume':   d['volume'],
                    'average':  d['average'],
                    'highest':  d['highest'],
                    'lowest':   d['lowest'],
                }
                for d in recent
            ]

async def main():
    async with aiohttp.ClientSession() as session:
        print("Fetching group names (just names, fast)...")
        groups_df = await fetch_all_group_names(session)
        all_names = sorted(groups_df['group_name'].unique())

        # Prompt loop until valid and confirmed
        while True:
            group_name = input("Enter EVE group name to fetch (e.g. Isotopes, Ice Products, Minerals): ").strip()
            if group_name.startswith("'") and group_name.endswith("'"):
                group_name = group_name[1:-1]
            group_name = group_name.strip()
            found = groups_df[groups_df['group_name'].str.lower() == group_name.lower()]
            if not found.empty:
                group_id = int(found.iloc[0]['group_id'])
                print(f"Selected group: {group_name} (ID {group_id})")
                print("Fetching type names in group (preview only)...")
                items_df = await get_types_in_group(session, group_id)
                print(f"{len(items_df)} items in group:")
                # Print item names (up to 50 per screen, pause if needed)
                N = len(items_df)
                names = items_df['type_name'].tolist()
                for i, name in enumerate(names, 1):
                    print(f"  - {name}")
                    if i % 50 == 0 and i < N:
                        cont = input("Press Enter to see more, or 'q' to quit: ").strip().lower()
                        if cont == 'q':
                            break
                confirm = input("Fetch history for these items? (y/n): ").strip().lower()
                if confirm == 'y' or confirm == 'yes':
                    break
                else:
                    print("Cancelled. Try a different group.")
            else:
                # Show close matches
                matches = difflib.get_close_matches(group_name, all_names, n=5, cutoff=0.5)
                print(f"Group '{group_name}' not found.")
                if matches:
                    print("Did you mean:", ", ".join(matches))
                else:
                    print("No similar group names found. Try again.")

        # Fetch market history for all types
        print(f"Fetching {len(items_df)} market histories in group '{group_name}' ...")
        sem = asyncio.Semaphore(MAX_CONCURRENT)
        tasks = [
            fetch_history_for_type(session, sem, row['type_id'], row['type_name'], group_id, group_name)
            for _, row in items_df.iterrows()
        ]
        chunks = await asyncio.gather(*tasks)
        # flatten
        records = [r for chunk in chunks for r in chunk]
        if not records:
            print("No market data found for this group.")
            return
        df = pd.DataFrame(records)
        # Output file with finish time
        finished = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M")
        safe_group_name = group_name.replace(' ', '_')
        outpath = os.path.join(OUTPUT_DIR, f"market_history_{safe_group_name}_{finished}.csv")
        df.to_csv(outpath, index=False)
        print(f"Saved {len(df)} rows to {outpath}")

if __name__ == "__main__":
    asyncio.run(main())
