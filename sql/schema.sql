CREATE TABLE IF NOT EXISTS products (product_id TEXT PRIMARY KEY, category TEXT NOT NULL, product TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS market_observations (observation_id TEXT PRIMARY KEY, product_id TEXT NOT NULL REFERENCES products(product_id), market TEXT NOT NULL, platform TEXT, listing_price REAL CHECK(listing_price >= 0), currency TEXT NOT NULL, price_type TEXT NOT NULL, listing_status TEXT, condition TEXT, source_url TEXT, observation_date TEXT, source_checked TEXT, notes TEXT);
CREATE INDEX IF NOT EXISTS idx_obs_product_market ON market_observations(product_id,market);
