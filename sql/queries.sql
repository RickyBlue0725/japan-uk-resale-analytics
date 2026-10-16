-- Coverage by category and market (do not treat sold listing displays as verified transaction prices)
SELECT p.category, o.market, o.price_type, COUNT(*) AS observations
FROM market_observations o JOIN products p ON p.product_id=o.product_id
GROUP BY p.category, o.market, o.price_type ORDER BY p.category,o.market;

-- Products lacking UK observations
SELECT p.product_id, p.product FROM products p
LEFT JOIN market_observations o ON p.product_id=o.product_id AND o.market='UK'
GROUP BY p.product_id HAVING COUNT(o.observation_id)=0;
