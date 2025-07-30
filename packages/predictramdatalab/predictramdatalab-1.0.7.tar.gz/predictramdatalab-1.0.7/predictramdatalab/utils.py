from typing import Dict, Optional, List
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def export_to_excel(data: List[Dict], filename: str):
    """Export data to Excel file."""
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def visualize_data(instruction: str, stock_data: Dict, save_path: Optional[str] = None):
    """Generate visualization based on instruction."""
    try:
        # Extract x and y axis from instruction
        x_axis, y_axis = None, None
        instruction_lower = instruction.lower()
        
        if "vs" in instruction_lower:
            parts = instruction_lower.split("vs")
            y_axis_part = parts[0].strip()
            x_axis_part = parts[1].strip()
        
        # Try to map these to actual fields
        field_mapping = {
            "sharpe ratio": "Sharpe Ratio",
            "volatility": "Annualized Volatility (%)",
            "return": "CAGR",
            "cagr": "CAGR",
            "roi": "Return_on_Investment",
            "pe ratio": "trailingPE",
            "price to book": "P/B_Ratio",
            "market cap": "Market Cap",
            "beta": "Beta",
            "alpha": "Annualized Alpha (%)",
            "debt to equity": "Debt_to_Equity_Ratio",
            "current ratio": "currentRatio",
            "dividend yield": "Dividend_Yield"
        }
        
        y_axis = field_mapping.get(y_axis_part, y_axis_part)
        x_axis = field_mapping.get(x_axis_part, x_axis_part)
    
    # Prepare data for plotting
        plot_data = []
        for symbol, data in stock_data.items():
            x_val = data.get(x_axis, None) if x_axis else None
            y_val = data.get(y_axis, None) if y_axis else None
            
            if x_val is not None and y_val is not None and not np.isnan(x_val) and not np.isnan(y_val):
                plot_data.append({
                    "symbol": symbol,
                    "name": data.get("shortName", symbol),
                    "x": x_val,
                    "y": y_val,
                    "market_cap": data.get("Market Cap", 0)
                })
        
        if not plot_data:
            return "Not enough data to generate visualization"
        
        df = pd.DataFrame(plot_data)
        
        # Create scatter plot
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(
            df["x"], df["y"],
            s=df["market_cap"]/1e9,
            alpha=0.6
        )
        
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title(f"{y_axis} vs {x_axis}")
        
        # Add annotations for top 5 stocks by market cap
        for i, row in df.nlargest(5, "market_cap").iterrows():
            plt.annotate(
                row["symbol"],
                (row["x"], row["y"]),
                textcoords="offset points",
                xytext=(0,10),
                ha='center'
            )
        
        plt.colorbar(scatter, label="Market Cap (in billions)")
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
            return f"Visualization saved to {save_path}"
        else:
            plt.show()
            return "Displaying visualization"
            
    except Exception as e:
        return f"Visualization error: {str(e)}"