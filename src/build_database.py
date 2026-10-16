"""Rebuild the SQLite database from tracked CSV files."""
import csv,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
conn=sqlite3.connect(ROOT/'resale_analysis.db')
conn.execute('PRAGMA foreign_keys=ON')
conn.executescript((ROOT/'sql/schema.sql').read_text())
conn.execute('DELETE FROM market_observations')
conn.execute('DELETE FROM products')
with (ROOT/'data/products.csv').open(encoding='utf-8',newline='') as f:
 for r in csv.DictReader(f):conn.execute('INSERT INTO products VALUES(?,?,?)',(r['product_id'],r['category'],r['product']))
with (ROOT/'data/market_data.csv').open(encoding='utf-8',newline='') as f:
 for r in csv.DictReader(f):
  conn.execute('INSERT INTO market_observations VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',(r['observation_id'],r['product_id'],r['market'],r['platform'],float(r['listing_price']),r['currency'],r['price_type'],r['listing_status'],r['condition'],(r['source_url'] or None),r['observation_date'],r['source_checked'],r['notes']))
conn.commit();print('Built',ROOT/'resale_analysis.db');conn.close()
