"""Transparent resale unit economics. Standard library only.
Run: python src/profitability_analysis.py
All amounts illustrative unless supported by verified cost and sales evidence.
"""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def profit_model(purchase_jpy, sale_gbp, jpy_per_gbp, shipping_gbp, fee_rate, other_cost_gbp=0, import_duty_gbp=0, nonrecoverable_vat_gbp=0, returns_reserve_gbp=0):
    if jpy_per_gbp<=0 or sale_gbp<=0: raise ValueError('Exchange rate and sale price must be positive')
    if not 0<=fee_rate<=1: raise ValueError('Fee rate must be between 0 and 1')
    costs=purchase_jpy/jpy_per_gbp+shipping_gbp+sale_gbp*fee_rate+other_cost_gbp+import_duty_gbp+nonrecoverable_vat_gbp+returns_reserve_gbp
    profit=sale_gbp-costs
    return {'net_profit_gbp':round(profit,2),'margin_pct':round(profit/sale_gbp*100,2),'total_cost_gbp':round(costs,2)}

def main():
    with (ROOT/'data/market_data.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
    print(f'Observed market rows: {len(rows)}')
    print('UK observations:',sum(r['market']=='UK' for r in rows))
    print('Verified completed transaction prices:',sum(r['price_type']=='verified_transaction' for r in rows))
    print('No profit ranking is generated without matched Japan/UK transaction evidence and validated costs.')
    print('Illustrative model ONLY:',profit_model(5000,80,200,15,0.13,10))
if __name__=='__main__':main()
