"""
Data cleaning and preprocessing routines.
Handles null values, deduplication, and date parsing.
"""

import pandas as pd
import numpy as np

def validate_and_clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans types, checks missing values, and adds date features."""
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
    
    return clean_df
