from typing import Dict, List, Optional
import re
import numpy as np

class QueryProcessor:
    def __init__(self):
        self.field_mapping = {
            # Your complete field mapping dictionary here
            "Stock Symbol": "Stock Symbol",
            "Volatility": "Annualized Volatility (%)",
            "Beta": "Beta",
            "P/E": "trailingPE",
            # Include all other field mappings from your original code
        }

    def process_query(self, query: str, stock_data: Dict, limit: int = 20) -> List[Dict]:
        """Process a natural language query and return matching stocks."""
        if not stock_data:
            return []

        conditions = self._parse_query_conditions(query)
        filtered_stocks = []

        for symbol, data in stock_data.items():
            if self._matches_conditions(data, conditions):
                filtered_stocks.append({
                    "symbol": symbol,
                    "name": data.get("shortName", ""),
                    **{k: data.get(k, None) for k in self._get_relevant_fields(data, conditions)}
                })

        sorted_stocks = self._sort_results(filtered_stocks, conditions)
        return sorted_stocks[:limit]

    def _sort_results(self, stocks: List[Dict], conditions: List[Dict]) -> List[Dict]:
        """Sort results based on the most important condition with None handling."""
        if not stocks:
            return []

        # Try to sort by the first numeric condition
        for condition in conditions:
            field = condition["field"]
            if field in stocks[0] and isinstance(stocks[0][field], (int, float)):
                reverse = condition["operator"] in ('>', '>=')
                return sorted(
                    [s for s in stocks if s.get(field) is not None],
                    key=lambda x: x.get(field, 0),
                    reverse=reverse
                )

        # Default sort by market cap (handling None values)
        return sorted(
            [s for s in stocks if s.get("Market Cap") is not None],
            key=lambda x: x.get("Market Cap", 0),
            reverse=True
        )

    def _parse_query_conditions(self, query: str) -> List[Dict]:
        """Parse query into individual conditions."""
        condition_strings = re.split(r',|\band\b|\bor\b', query, flags=re.IGNORECASE)
        conditions = []

        for cond_str in condition_strings:
            cond_str = cond_str.strip()
            if not cond_str:
                continue

            match = re.match(
                r'(.+?)\s*(>|>=|<|<=|=|==|!=)\s*([\d\.]+%?)', 
                cond_str, 
                flags=re.IGNORECASE
            )
            if match:
                field, operator, value = match.groups()
                field = self._map_field_name(field.strip())
                if field:
                    if '%' in value:
                        value = float(value.replace('%', '')) / 100
                    else:
                        try:
                            value = float(value)
                        except ValueError:
                            value = value

                    conditions.append({
                        "field": field,
                        "operator": operator,
                        "value": value,
                        "original": cond_str
                    })

        return conditions

    def _map_field_name(self, field_name: str) -> Optional[str]:
        """Map natural language field names to actual data fields."""
        for key, value in self.field_mapping.items():
            if key.lower() in field_name.lower():
                return value
        return None

    def _matches_conditions(self, stock_data: Dict, conditions: List[Dict]) -> bool:
        """Check if a stock matches all conditions."""
        for condition in conditions:
            field = condition["field"]
            operator = condition["operator"]
            target_value = condition["value"]

            actual_value = stock_data.get(field, None)
            if actual_value is None:
                return False

            if isinstance(actual_value, float) and np.isnan(actual_value):
                return False

            if operator == '>' and not (actual_value > target_value):
                return False
            elif operator == '>=' and not (actual_value >= target_value):
                return False
            elif operator == '<' and not (actual_value < target_value):
                return False
            elif operator == '<=' and not (actual_value <= target_value):
                return False
            elif operator in ('=', '==') and not (actual_value == target_value):
                return False
            elif operator == '!=' and not (actual_value != target_value):
                return False

        return True

    def _get_relevant_fields(self, stock_data: Dict, conditions: List[Dict]) -> set:
        """Get set of relevant fields to include in results."""
        relevant_fields = set()
        for condition in conditions:
            relevant_fields.add(condition["field"])

        basic_fields = {
            "Stock Symbol", "shortName", "Stock Industry", "sector",
            "Market Cap", "Current_Price", "CAGR", "Total_Score"
        }
        relevant_fields.update(basic_fields)

        return relevant_fields