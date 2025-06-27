import os
import glob
import pandas as pd
from pandas.errors import EmptyDataError

# ─── CONFIG ────────────────────────────────────────────────────────────────
BATCH_DIR     = "output/market_history"
BATCH_PATTERN = os.path.join(BATCH_DIR, "market_history_batch_*.csv")

# ─── 1) List batch files ────────────────────────────────────────────────────
files = sorted(glob.glob(BATCH_PATTERN), key=lambda f: int(os.path.basename(f).split("_")[-1].split(".")[0]))
batch_nums = [int(os.path.basename(f).split("_")[-1].split(".")[0]) for f in files]

print(f"Found {len(files)} batch files, numbered: {batch_nums}")

# Check for missing batch numbers
expected = set(range(1, max(batch_nums) + 1))
missing  = sorted(expected - set(batch_nums))
if missing:
    print(f"⚠️  Missing batches: {missing}")
else:
    print("✅ All batch numbers present")

# ─── 2) Read & summarize each batch ─────────────────────────────────────────
summary = []
all_ids = set()

for f in files:
    num = int(os.path.basename(f).split("_")[-1].split(".")[0])
    try:
        df = pd.read_csv(f)
        rows = len(df)
        uniq = df['type_id'].nunique() if 'type_id' in df.columns else 0
        ids = set(df['type_id']) if 'type_id' in df.columns else set()
    except EmptyDataError:
        # Empty file: zero rows, zero unique IDs
        rows = 0
        uniq = 0
        ids = set()
    # detect duplicates across batches
    dups = ids & all_ids
    all_ids |= ids

    if dups:
        print(f"⚠️  Batch {num}: {len(dups)} duplicate type_ids across batches")

    summary.append((num, rows, uniq, len(dups)))

# ─── 3) Build a DataFrame & print ───────────────────────────────────────────
sum_df = pd.DataFrame(summary, columns=["batch", "rows", "unique_ids", "dups_against_prev"])
print("\nBatch summary:")
print(sum_df.to_string(index=False))

# ─── 4) Totals ───────────────────────────────────────────────────────────────
total_rows   = sum(sum_df['rows'])
total_unique = len(all_ids)
print(f"\nTotal rows across all batches: {total_rows}")
print(f"Total unique type_ids fetched: {total_unique}")
