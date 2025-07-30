# utils.py
import json
import os
from typing import Dict, List, Union, Optional

def load_stock_data() -> Dict:
    """Load the stock data from the JSON file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data', 'all_stocks.json')
    
    with open(data_path, 'r') as file:
        return json.load(file)

def get_stock_by_symbol(symbol: str) -> Optional[Dict]:
    """Get stock data by symbol."""
    data = load_stock_data()
    return data.get(symbol.upper())

def get_stocks_by_industry(industry: str) -> Dict[str, Dict]:
    """Get all stocks in a specific industry."""
    data = load_stock_data()
    return {symbol: stock for symbol, stock in data.items() 
            if stock.get('Stock Industry', '').lower() == industry.lower()}

def get_all_industries() -> List[str]:
    """Get list of all unique industries."""
    data = load_stock_data()
    industries = set()
    for stock in data.values():
        if 'Stock Industry' in stock:
            industries.add(stock['Stock Industry'])
    return sorted(industries)

def get_all_symbols() -> List[str]:
    """Get list of all stock symbols."""
    data = load_stock_data()
    return list(data.keys())

def extract_fields(stock_data: Dict, fields: List[str], mapping: Dict) -> Dict:
    """Extract specified fields from stock data using the mapping."""
    result = {}
    for field in fields:
        mapped_field = mapping.get(field, field)
        if mapped_field in stock_data:
            result[field] = stock_data[mapped_field]
        else:
            result[field] = None
    return result