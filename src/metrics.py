"""
Financial calculation helper functions:
- Gross Revenue
- Discount Amount
- Net Revenue
- Total COGS (Cost of Goods Sold)
- Net Profit
- Profit Margin (%)
"""

import pandas as pd
import numpy as np

def calculate_gross_revenue(df: pd.DataFrame) -> pd.Series:
    """Gross Revenue = Unit Price * Units Sold"""
    return (df["Unit_Price"] * df["Units_Sold"]).round(2)

def calculate_discount_amount(df: pd.DataFrame) -> pd.Series:
    """Discount value given to customer"""
    gross_rev = df["Unit_Price"] * df["Units_Sold"]
    return (gross_rev * (df["Discount_Percent"] / 100.0)).round(2)

def calculate_net_revenue(df: pd.DataFrame) -> pd.Series:
    """Net Revenue = Gross Revenue - Discount Amount."""
    gross_rev = df["Unit_Price"] * df["Units_Sold"]
    discount_amt = gross_rev * (df["Discount_Percent"] / 100.0)
    net_rev = gross_rev - discount_amt
    return net_rev.round(2)

def calculate_total_cogs(df: pd.DataFrame) -> pd.Series:
    """Cost of Goods Sold (COGS) = Unit Cost * Units Sold."""
    return (df["Unit_Cost"] * df["Units_Sold"]).round(2)

def calculate_net_profit(df: pd.DataFrame) -> pd.Series:
    """Net Profit = Net Revenue - Total COGS"""
    return (df["Net_Revenue"] - df["Total_COGS"]).round(2)

def calculate_profit_margin_pct(df: pd.DataFrame) -> pd.Series:
    """Profit Margin (%) = (Net Profit / Net Revenue) * 100"""
    return ((df["Net_Profit"] / df["Net_Revenue"]) * 100.0).round(2)

def enrich_sales_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Adds all financial calculated columns to dataframe."""
    data = df.copy()
    data["Gross_Revenue"] = calculate_gross_revenue(data)
    data["Discount_Amount"] = calculate_discount_amount(data)
    data["Net_Revenue"] = calculate_net_revenue(data)
    data["Total_COGS"] = calculate_total_cogs(data)
    data["Net_Profit"] = calculate_net_profit(data)
    data["Profit_Margin_Pct"] = calculate_profit_margin_pct(data)
    return data
