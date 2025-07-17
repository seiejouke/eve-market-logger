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

INV_TYPES_CSV = os.path.join(OUTPUT_DIR, "inv_types.csv")

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
        await asyncio.sleep(0.05)
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
    print("Select mode:\n  1. Fetch by EVE group name (interactive)\n  2. Fetch from item names in a CSV file")
    mode = input("Enter 1 or 2: ").strip()
    use_csv = (mode == "2")

    async with aiohttp.ClientSession() as session:
        if not use_csv:
            print("Fetching group names (just names, fast)...")
            groups_df = await fetch_all_group_names(session)
            all_names = sorted(groups_df['group_name'].unique())

            while True:
                print("\nTip: Enter '?' to see all available group names.")
                group_name = input("Enter EVE group name to fetch (e.g. Battleships, Minerals, Isotopes): ").strip()
                if group_name == "?":
                    print("\nAll group names:")
                    for name in all_names:
                        print("  -", name)
                    print()
                    continue

                # Try exact match first
                found = groups_df[groups_df['group_name'].str.lower() == group_name.lower()]
                if not found.empty:
                    group_id = int(found.iloc[0]['group_id'])
                    group_real_name = found.iloc[0]['group_name']
                    print(f"Selected group: {group_real_name} (ID {group_id})")
                else:
                    # Fuzzy match
                    matches = difflib.get_close_matches(group_name, all_names, n=5, cutoff=0.5)
                    if matches:
                        print(f"\nGroup '{group_name}' not found.")
                        print("Did you mean:")
                        for i, match in enumerate(matches, 1):
                            print(f"  {i}. {match}")
                        choice = input(f"Select 1-{len(matches)} or 'n' to try again: ").strip()
                        if choice.isdigit() and 1 <= int(choice) <= len(matches):
                            match_name = matches[int(choice)-1]
                            found = groups_df[groups_df['group_name'] == match_name]
                            group_id = int(found.iloc[0]['group_id'])
                            group_real_name = found.iloc[0]['group_name']
                            print(f"Selected group: {group_real_name} (ID {group_id})")
                        else:
                            print("Try again.")
                            continue
                    else:
                        # --- New logic: if no group and no fuzzy matches, offer to search CSV ---
                        print(f"Group '{group_name}' not found and no close matches.")
                        # Try searching the CSV for items that contain the input in their name
                        if os.path.isfile(INV_TYPES_CSV):
                            df = pd.read_csv(INV_TYPES_CSV)
                            mask = df['type_name'].str.contains(group_name, case=False, na=False)
                            matches = df[mask]
                            if not matches.empty:
                                print(f"Found {len(matches)} items in CSV matching '{group_name}':")
                                preview = matches.head(50)
                                for i, row in preview.iterrows():
                                    print(f"  - {row['type_name']} (ID {row['type_id']})")
                                if len(matches) > 50:
                                    print("  ... (more not shown)")
                                confirm = input(f"Fetch history for these {len(matches)} items? (y/n): ").strip().lower()
                                if confirm.startswith('y'):
                                    group_id = -1
                                    group_real_name = f"CSV_search_{group_name}"
                                    items_df = matches[['type_id', 'type_name']]
                                    break
                                else:
                                    print("Cancelled. Try a different group or search.")
                                    continue
                            else:
                                print(f"No item names in {INV_TYPES_CSV} matched '{group_name}'. Try again.")
                                continue
                        else:
                            print(f"CSV file not found: {INV_TYPES_CSV}. Try again.")
                            continue

                if 'items_df' not in locals():
                    print("Fetching type names in group (preview only)...")
                    items_df = await get_types_in_group(session, group_id)
                    print(f"{len(items_df)} items in group:")
                    N = len(items_df)
                    names = items_df['type_name'].tolist()
                    for i, name in enumerate(names, 1):
                        print(f"  - {name}")
                        if i % 50 == 0 and i < N:
                            cont = input("Press Enter to see more, or 'q' to quit: ").strip().lower()
                            if cont == 'q':
                                break
                    confirm = input("Fetch history for these items? (y/n): ").strip().lower()
                    if not (confirm == 'y' or confirm == 'yes'):
                        print("Cancelled. Try a different group.")
                        continue

            records_meta = []
            for _, row in items_df.iterrows():
                records_meta.append( (row['type_id'], row['type_name'], group_id, group_real_name) )
        else:
            # CSV loader mode
            csv_path = input("Enter CSV path (default: output/inv_types.csv): ").strip()
            if not csv_path:
                csv_path = INV_TYPES_CSV
            if not os.path.isfile(csv_path):
                print(f"File not found: {csv_path}")
                return
            df = pd.read_csv(csv_path)
            if 'type_id' not in df.columns or 'type_name' not in df.columns:
                print("CSV must contain 'type_id' and 'type_name' columns!")
                return
            print(f"Loaded {len(df)} items from {csv_path}.")
            group_id = -1
            group_real_name = os.path.splitext(os.path.basename(csv_path))[0]
            records_meta = []
            for _, row in df.iterrows():
                records_meta.append( (row['type_id'], row['type_name'], group_id, group_real_name) )

        # Fetch market history for all items
        print(f"Fetching {len(records_meta)} market histories ...")
        sem = asyncio.Semaphore(MAX_CONCURRENT)
        tasks = [
            fetch_history_for_type(session, sem, tid, tname, gid, gname)
            for tid, tname, gid, gname in records_meta
        ]
        chunks = await asyncio.gather(*tasks)
        records = [r for chunk in chunks for r in chunk]
        if not records:
            print("No market data found.")
            return
        df = pd.DataFrame(records)
        finished = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M")
        safe_name = group_real_name.replace(' ', '_')
        outpath = os.path.join(OUTPUT_DIR, f"market_history_{safe_name}_{finished}.csv")
        df.to_csv(outpath, index=False)
        print(f"Saved {len(df)} rows to {outpath}")

if __name__ == "__main__":
    asyncio.run(main())
