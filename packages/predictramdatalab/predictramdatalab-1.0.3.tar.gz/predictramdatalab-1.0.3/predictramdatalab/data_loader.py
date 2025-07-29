import json
from pathlib import Path
from typing import Dict

class DataLoader:
    def __init__(self):
        self.data_file = Path(__file__).parent / "data" / "all_stocks.json"
        
    def load_data(self) -> Dict:
        """Load stock data from JSON file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Stock data file not found. Please ensure all_stocks.json exists in the data directory.")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON data in all_stocks.json file.")