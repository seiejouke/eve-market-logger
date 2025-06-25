import requests
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from datetime import datetime
import os

# Load .env config
load_dotenv()

DB_CONFIG = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASS"),
    'host': os.getenv("DB_HOST", "localhost"),
    'port': os.getenv("DB_PORT", "5432")
}

# Example item: Tritanium (type_id=34), The Forge region (region_id=10000002)
TYPE_ID = 34
ITEM_NAME = "Tritanium"
REGION_ID = 10000002
API_URL = f"https://esi.evetech.net/latest/markets/{REGION_ID}/orders/?order_type=sell&type_id={TYPE_ID}"

def fetch_market_data():
    print(f"📦 Fetching {ITEM_NAME} sell orders from The Forge…")
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Failed to fetch data: {e}")
        return []

def insert_data(entries):
    if not entries:
        print("⚠️ No data to insert.")
        return

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        for entry in entries:
            cur.execute(
                sql.SQL("""
                    INSERT INTO market_orders (item_name, price, volume, location, order_type, issued_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """),
                (
                    ITEM_NAME,
                    entry.get("price"),
                    entry.get("volume_remain"),
                    entry.get("location_id"),
                    entry.get("is_buy_order", False) and "buy" or "sell",
                    entry.get("issued")
                )
            )

        conn.commit()
        print(f"✅ Inserted {len(entries)} rows into market_orders.")
        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ DB Error: {e}")

if __name__ == "__main__":
    data = fetch_market_data()
    insert_data(data)
