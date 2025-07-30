# api.py
from typing import Dict, List, Union, Optional
from .utils import (
    get_stock_by_symbol,
    get_stocks_by_industry,
    get_all_industries,
    get_all_symbols,
    extract_fields
)
from .constants import STOCK_FIELDS_MAPPING

class StockAPI:
    """API for accessing stock data."""
    
    @staticmethod
    def get_stock(symbol: str, fields: List[str] = None) -> Optional[Dict]:
        """
        Get data for a specific stock.
        
        Args:
            symbol: Stock symbol
            fields: List of fields to return (None returns all fields)
            
        Returns:
            Dictionary with stock data or None if not found
        """
        stock_data = get_stock_by_symbol(symbol)
        if stock_data is None:
            return None
            
        if fields is None:
            return stock_data
            
        return extract_fields(stock_data, fields, STOCK_FIELDS_MAPPING)
    
    @staticmethod
    def get_industry_stocks(industry: str, fields: List[str] = None) -> Dict[str, Dict]:
        """
        Get all stocks in a specific industry.
        
        Args:
            industry: Industry name
            fields: List of fields to return for each stock (None returns all fields)
            
        Returns:
            Dictionary with stock symbols as keys and stock data as values
        """
        stocks = get_stocks_by_industry(industry)
        
        if fields is None:
            return stocks
            
        return {
            symbol: extract_fields(stock, fields, STOCK_FIELDS_MAPPING)
            for symbol, stock in stocks.items()
        }
    
    @staticmethod
    def get_all_industries() -> List[str]:
        """Get list of all available industries."""
        return get_all_industries()
    
    @staticmethod
    def get_all_symbols() -> List[str]:
        """Get list of all available stock symbols."""
        return get_all_symbols()
    
    @staticmethod
    def search_stocks(search_term: str, fields: List[str] = None) -> Dict[str, Dict]:
        """
        Search stocks by symbol or company name.
        
        Args:
            search_term: Term to search for in symbol or company name
            fields: List of fields to return for each stock (None returns all fields)
            
        Returns:
            Dictionary with matching stocks
        """
        search_term = search_term.lower()
        data = get_stock_by_symbol('DUMMY')  # This will load all data
        if not isinstance(data, dict):
            data = {}
        
        matches = {}
        for symbol, stock in data.items():
            if (search_term in symbol.lower() or 
                search_term in stock.get('shortName', '').lower() or
                search_term in stock.get('longName', '').lower()):
                if fields is None:
                    matches[symbol] = stock
                else:
                    matches[symbol] = extract_fields(stock, fields, STOCK_FIELDS_MAPPING)
        
        return matches