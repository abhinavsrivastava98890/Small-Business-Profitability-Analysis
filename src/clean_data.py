"""
Data cleaning and preprocessing routines.
Handles null values, date parsing, and discount grouping.
"""

import pandas as pd
import numpy as np

def validate_and_clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans types, checks missing values, and adds date/discount features."""
    clean_df = df.copy()
    
    clean_df = clean_df.drop_duplicates(subset=["Transaction_ID"])
    clean_df["Return_Status"] = clean_df["Return_Status"].fillna("No").astype(str).str.strip().str.capitalize()
    clean_df["Discount_Percent"] = clean_df["Discount_Percent"].fillna(0.0).clip(lower=0.0, upper=100.0)
    clean_df["Units_Sold"] = clean_df["Units_Sold"].fillna(1).astype(int).clip(lower=1)
    clean_df["Unit_Price"] = clean_df["Unit_Price"].fillna(0.0).astype(float)
    clean_df["Unit_Cost"] = clean_df["Unit_Cost"].fillna(0.0).astype(float)
    
    # Date formatting
    clean_df["Date"] = pd.to_datetime(clean_df["Date"])
    clean_df["Year"] = clean_df["Date"].dt.year
    clean_df["Month"] = clean_df["Date"].dt.month
    clean_df["Month_Name"] = clean_df["Date"].dt.strftime("%b")
    clean_df["Year_Month"] = clean_df["Date"].dt.strftime("%Y-%m")
    clean_df["Quarter"] = "Q" + clean_df["Date"].dt.quarter.astype(str)
    
    # Discount tiers
    bins = [-1, 0, 10, 20, 30, 100]
    labels = ["No Discount (0%)", "Low (1-10%)", "Moderate (11-20%)", "High (21-30%)", "Deep (>30%)"]
    clean_df["Discount_Bracket"] = pd.cut(clean_df["Discount_Percent"], bins=bins, labels=labels)
    
    return clean_df

def assign_discount_tier(discount_pct: float) -> str:
    """Categorizes raw discount percent into human-readable tier label."""
    if discount_pct <= 0:
        return "No Discount (0%)"
    elif discount_pct <= 10:
        return "Low (1-10%)"
    elif discount_pct <= 20:
        return "Moderate (11-20%)"
    elif discount_pct <= 30:
        return "High (21-30%)"
    return "Deep (>30%)"
