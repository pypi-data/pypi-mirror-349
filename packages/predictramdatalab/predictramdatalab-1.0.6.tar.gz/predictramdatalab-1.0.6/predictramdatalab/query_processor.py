from typing import Dict, List, Optional
import re
import numpy as np

class QueryProcessor:
    def __init__(self):
        self.field_mapping = {
            # Basic metrics
            "Stock Symbol": "Stock Symbol",
            "Stock Industry": "Stock Industry",
            "Dividend Payout Ratio": "Dividend Payout Ratio",
            "Five Year Avg Dividend Yield": "Five Year Avg Dividend Yield",
            "Price to Sales Trailing 12 Months": "Price to Sales Trailing 12 Months",
            "Trailing Annual Dividend Rate": "Trailing Annual Dividend Rate",
            "Profit Margins": "Profit Margins",
            "% Held by Insiders": "% Held by Insiders",
            "% Held by Institutions": "% Held by Institutions",
            "Volume": "Volume",
            "Regular Market Volume": "Regular Market Volume",
            "Average Volume": "Average Volume",
            "Average Volume 10 days": "Average Volume 10days",
            "Average Daily Volume 10 Day": "Average Daily Volume 10 Day",
            "Return on Assets": "Return on Assets (ttm)",
            "Return on Equity (ttm)": "Return on Equity (ttm)",
            "Total Value": "Total Value",
            "Correlation with NSEI": "Correlation with ^NSEI",
            "Annualized Alpha (%)": "Annualized Alpha (%)",
            "Annualized Volatility (%)": "Annualized Volatility (%)",
            "Sharpe Ratio": "Sharpe Ratio",
            "Treynor Ratio": "Treynor Ratio",
            "Sortino Ratio": "Sortino Ratio",
            "Maximum Drawdown": "Maximum Drawdown",
            "R-Squared": "R-Squared",
            "Downside Deviation": "Downside Deviation",
            "Annualized Tracking Error (%)": "Annualized Tracking Error (%)",
            "VaR (95%)": "VaR (95%)",
            "50-Day Moving Average": "50-Day Moving Average",
            "200-Day Moving Average": "200-Day Moving Average",
            "New Haircut Margin": "New Haircut Margin",
            "Rating": "Rating",
            "Combined Score": "Combined Score",
            "New Collateral Value Percentage": "New Collateral Value Percentage",
            "Market Cap": "Market Cap",
            "Enterprise Value": "Enterprise Value",
            "Trailing P/E": "trailingPE",
            "Forward P/E": "forwardPE",
            "PEG Ratio": "trailingPegRatio",
            "Price/Sales": "Price to Sales Trailing 12 Months",
            "Price/Book": "P/B_Ratio",
            "Enterprise Value/Revenue": "enterpriseToRevenue",
            "Enterprise Value/EBITDA": "enterpriseToEbitda",
            "Beta": "Beta",
            "52-Week High": "fiftyTwoWeekHigh",
            "52-Week Low": "fiftyTwoWeekLow",
            "50-Day Average": "fiftyDayAverage",
            "200-Day Average": "twoHundredDayAverage",
            "Shares Outstanding": "sharesOutstanding",
            "Float": "floatShares",
            "Book Value": "bookValue",
            "EBITDA": "ebitda",
            "Revenue": "totalRevenue",
            "Revenue Per Share": "revenuePerShare",
            "Gross Profit": "grossProfit",
            "Free Cash Flow": "freeCashflow",
            "Operating Cash Flow": "operatingCashflow",
            "Revenue Growth": "revenueGrowth",
            "Current Ratio": "currentRatio",
            "Quick Ratio": "quickRatio",
            "Debt to Equity": "Debt_to_Equity_Ratio",
            "Total Debt": "totalDebt",
            "Total Cash": "totalCash",
            "Total Cash Per Share": "totalCashPerShare",
            "CAGR": "CAGR",
            "EPS": "EPS",
            # Interpretations
            "Correlation with NSEI Interpretation": "Correlation with ^NSEI Interpretation",
            "Alpha Interpretation": "Annualized Alpha (%) Interpretation",
            "Volatility Interpretation": "Annualized Volatility (%) Interpretation",
            "Sharpe Ratio Interpretation": "Sharpe Ratio Interpretation",
            "Treynor Ratio Interpretation": "Treynor Ratio Interpretation",
            "Sortino Ratio Interpretation": "Sortino Ratio Interpretation",
            "Maximum Drawdown Interpretation": "Maximum Drawdown Interpretation",
            "R-Squared Interpretation": "R-Squared Interpretation",
            "Downside Deviation Interpretation": "Downside Deviation Interpretation",
            "Tracking Error Interpretation": "Annualized Tracking Error (%) Interpretation",
            "VaR Interpretation": "VaR (95%) Interpretation",
            # Company Info
            "Address": "address1",
            "City": "city",
            "Zip": "zip",
            "Country": "country",
            "Website": "website",
            "Sector": "sector",
            "Industry": "industry",
            "Business Summary": "longBusinessSummary",
            "Company Name": "shortName",
            "Exchange": "exchange",
            "Currency": "currency",
            # Industry Comparisons
            "Industry Forward PE": "industry_forwardPE",
            "Industry Trailing PE": "industry_trailingPE",
            "Industry Debt to Equity": "industry_debtToEquity",
            "Industry Current Ratio": "industry_currentRatio",
            "Industry Quick Ratio": "industry_quickRatio",
            "Industry EBITDA": "industry_ebitda",
            "Industry Total Debt": "industry_totalDebt",
            "Industry Return on Assets": "industry_returnOnAssets",
            "Industry Return on Equity": "industry_returnOnEquity",
            "Industry Revenue Growth": "industry_revenueGrowth",
            "Industry Gross Margins": "industry_grossMargins",
            "Industry EBITDA Margins": "industry_ebitdaMargins",
            "Industry Operating Margins": "industry_operatingMargins",
        }
        
    def process_query(self, query: str, stock_data: Dict, limit: int = 20) -> List[Dict]:
        """Process a natural language query and return matching stocks."""
        # Parse the query to extract conditions
        conditions = self._parse_query_conditions(query)
        
        # Filter stocks based on conditions
        filtered_stocks = []
        for symbol, data in stock_data.items():
            if self._matches_conditions(data, conditions):
                filtered_stocks.append({
                    "symbol": symbol,
                    "name": data.get("shortName", ""),
                    **{k: data.get(k, None) for k in self._get_relevant_fields(data, conditions)}
                })
        
        # Sort and limit results
        sorted_stocks = self._sort_results(filtered_stocks, conditions)
        return sorted_stocks[:limit]
    
    def _parse_query_conditions(self, query: str) -> List[Dict]:
        """Parse query into individual conditions."""
        # Split query into individual conditions
        condition_strings = re.split(r',|\band\b|\bor\b', query, flags=re.IGNORECASE)
        conditions = []
        
        for cond_str in condition_strings:
            cond_str = cond_str.strip()
            if not cond_str:
                continue
                
            # Extract field, operator, and value
            match = re.match(
                r'(.+?)\s*(>|>=|<|<=|=|==|!=)\s*([\d\.]+%?)', 
                cond_str, 
                flags=re.IGNORECASE
            )
            if match:
                field, operator, value = match.groups()
                field = self._map_field_name(field.strip())
                if field:
                    # Convert percentage values to decimals
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
            
            # Get actual value from stock data
            actual_value = stock_data.get(field, None)
            if actual_value is None:
                return False
                
            # Handle NaN values
            if isinstance(actual_value, float) and np.isnan(actual_value):
                return False
                
            # Compare values based on operator
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
        
        # Always include some basic fields
        basic_fields = {
            "Stock Symbol", "shortName", "Stock Industry", "sector",
            "Market Cap", "Current_Price", "CAGR", "Total_Score"
        }
        relevant_fields.update(basic_fields)
        
        return relevant_fields
    
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