import json
from pathlib import Path
from typing import Dict, List, Optional, Union
from .data_loader import DataLoader
from .query_processor import QueryProcessor
from .utils import export_to_excel, visualize_data

class StockAPI:
    def __init__(self):
        """Initialize the StockAPI with data loading and query processing capabilities."""
        self.data_loader = DataLoader()
        self.query_processor = QueryProcessor()
        self.stock_data = self.data_loader.load_data()
        
    def get_stock(self, symbol: str) -> Optional[Dict]:
        """Get all data for a specific stock by its symbol."""
        return self.stock_data.get(symbol.upper())
    
    def get_field(self, symbol: str, field: str) -> Optional[Union[str, float, int]]:
        """Get a specific field for a given stock symbol."""
        stock = self.get_stock(symbol)
        if not stock:
            return None
        
        # Handle nested fields
        keys = field.split('.')
        value = stock
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        return value
    
    def get_industry(self, industry: str) -> Dict[str, Dict]:
        """Get all stocks in a specific industry."""
        return {symbol: data for symbol, data in self.stock_data.items() 
                if data.get("Stock Industry", "").lower() == industry.lower()}
    
    def query(self, query: str, limit: int = 20) -> List[Dict]:
        """Execute a natural language query against the stock data."""
        return self.query_processor.process_query(query, self.stock_data, limit)
    
    def visualize(self, instruction: str, save_path: Optional[str] = None):
        """Generate a visualization based on the instruction."""
        return visualize_data(instruction, self.stock_data, save_path)
    
    def export(self, query: str, filename: str):
        """Export query results to a file."""
        results = self.query(query)
        export_to_excel(results, filename)
        return f"Results exported to {filename}"
    
    def list_all_stocks(self) -> List[str]:
        """List all available stock symbols."""
        return list(self.stock_data.keys())
    
    def list_all_industries(self) -> List[str]:
        """List all available industries."""
        industries = set()
        for data in self.stock_data.values():
            if "Stock Industry" in data:
                industries.add(data["Stock Industry"])
        return sorted(list(industries))