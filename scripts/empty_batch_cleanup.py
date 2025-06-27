#!/usr/bin/env python3
import csv
import os
from pathlib import Path

# 1) Locate your project root and the market_history folder
project_root = Path(__file__).parent.parent
hist_dir = project_root / "output" / "market_history"

# 2) Glob inside that directory
for fpath in hist_dir.glob("market_history_batch_*.csv"):
    try:
        size = fpath.stat().st_size
        print(f"Checking {fpath.name}: {size} bytes")

        # a) Truly empty / whitespace-only files
        text = fpath.read_text(encoding="utf-8")
        if not text.strip():
            fpath.unlink()
            print("  → removed (blank/whitespace-only)")
            continue

        # b) Header-only CSVs
        with fpath.open(newline="", encoding="utf-8") as f:
            rows = [r for r in csv.reader(f) if any(cell.strip() for cell in r)]
        if len(rows) <= 1:
            fpath.unlink()
            print("  → removed (header-only)")
    except Exception as e:
        print(f"  ✗ could not process {fpath.name}: {e}")
