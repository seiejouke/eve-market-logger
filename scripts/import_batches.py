import os
import glob
import psycopg2

# === CONFIGURATION: update these values! ===
DB_NAME     = "eve_data"
DB_USER     = "postgres"
DB_PASSWORD = "109009885"   # ← replace with your password
DB_HOST     = "localhost"
DB_PORT     = "5432"

BATCH_DIR   = "output/market_history"  # folder with your batch CSVs

def import_batches():
    # 1) Connect to Postgres
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    # 2) COPY SQL with correct column order
    copy_sql = """
        COPY market_history(
            average,
            date,
            highest,
            lowest,
            order_count,
            volume,
            type_id
        )
        FROM STDIN WITH (FORMAT csv, HEADER true)
    """

    # 3) Find and import each batch
    pattern = os.path.join(BATCH_DIR, "market_history_batch_*.csv")
    batch_files = sorted(glob.glob(pattern))

    for filepath in batch_files:
        filename = os.path.basename(filepath)
        # skip empty files
        if os.path.getsize(filepath) == 0:
            print(f"Skipping empty file: {filename}")
            continue

        print(f"Importing {filename}...")
        with open(filepath, "r") as f:
            cur.copy_expert(copy_sql, f)
        conn.commit()

    # 4) Close connection
    cur.close()
    conn.close()
    print("✅ All batches imported successfully.")

if __name__ == "__main__":
    import_batches()
