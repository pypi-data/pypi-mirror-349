import json
from pathlib import Path
from typing import Dict, Any

class DataLoader:
    def __init__(self):
        self.data_file = Path(__file__).parent / "data" / "all_stocks.json"
        
    def load_data(self) -> Dict[str, Dict[str, Any]]:
        """Load stock data from JSON file and convert to dictionary with symbols as keys."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # If data is a list, convert to dictionary with symbols as keys
            if isinstance(data, list):
                return {item["Stock Symbol"]: item for item in data}
            return data
        except FileNotFoundError:
            raise FileNotFoundError("Stock data file not found. Please ensure all_stocks.json exists in the data directory.")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON data in all_stocks.json file.")
        except KeyError:
            raise ValueError("JSON data must contain 'Stock Symbol' field if provided as a list")