"""
Script to generate sales dataset for Small Business Profitability Analysis.
Generates realistic transactions with pricing, discounts, and return statuses.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Seed for consistent dataset generation
np.random.seed(42)
random.seed(42)

CATALOG = [
    # Electronics
    ("ELEC-001", "Wireless Optical Mouse", "Electronics", 280.0, 599.0),
    ("ELEC-002", "Bluetooth Over-Ear Headphones", "Electronics", 950.0, 1899.0),
    ("ELEC-003", "Braided USB-C Fast Cable", "Electronics", 85.0, 249.0),
    ("ELEC-004", "10,000mAh Power Bank", "Electronics", 620.0, 1199.0),
    ("ELEC-005", "Mechanical Gaming Keyboard", "Electronics", 1400.0, 2699.0),

    # Apparel
    ("APPR-001", "Classic Cotton Crew T-Shirt", "Apparel", 160.0, 499.0),
    ("APPR-002", "Slim Fit Denim Jeans", "Apparel", 450.0, 1299.0),
    ("APPR-003", "Vintage Denim Jacket", "Apparel", 800.0, 2199.0),
    ("APPR-004", "Fleece Winter Hoodie", "Apparel", 520.0, 1499.0),
    ("APPR-005", "Cushioned Sports Socks (3-Pack)", "Apparel", 75.0, 299.0),

    # Home & Kitchen
    ("HOME-001", "Stainless Steel Insulated Bottle", "Home & Kitchen", 220.0, 549.0),
    ("HOME-002", "Ceramic Coffee Mug (Set of 2)", "Home & Kitchen", 130.0, 399.0),
    ("HOME-003", "Non-Stick 24cm Frying Pan", "Home & Kitchen", 380.0, 899.0),
    ("HOME-004", "Adjustable LED Desk Lamp", "Home & Kitchen", 310.0, 749.0),
    ("HOME-005", "Airtight Glass Food Containers (3x)", "Home & Kitchen", 290.0, 699.0),

    # Stationery
    ("STAT-001", "Hardcover Ruled Journal", "Stationery", 90.0, 249.0),
    ("STAT-002", "Retractable Gel Pen Set (Pack of 5)", "Stationery", 45.0, 149.0),
    ("STAT-003", "Metal Mesh Desk Organizer", "Stationery", 140.0, 349.0),
    ("STAT-004", "Pastel Sticky Notes (4-Pack)", "Stationery", 35.0, 119.0),
    ("STAT-005", "Fluorescent Highlighter Set", "Stationery", 50.0, 159.0),

    # Personal Care
    ("CARE-001", "Gentle Hydrating Face Wash", "Personal Care", 110.0, 299.0),
    ("CARE-002", "Anti-Dandruff Herbal Shampoo", "Personal Care", 140.0, 379.0),
    ("CARE-003", "Nourishing Shea Butter Hand Cream", "Personal Care", 80.0, 249.0),
    ("CARE-004", "Sonic Electric Toothbrush", "Personal Care", 550.0, 1299.0),
    ("CARE-005", "Broad Spectrum Sunscreen SPF 50", "Personal Care", 180.0, 449.0),
]

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Cash"]
CUSTOMER_SEGMENTS = ["Regular", "New", "Premium"]

START_DATE = datetime(2025, 1, 1)
TOTAL_TRANSACTIONS = 1400

def generate_transactions():
    records = []
    
    for i in range(1, TOTAL_TRANSACTIONS + 1):
        txn_id = f"TXN-2025-{i:04d}"
        
        # Seasonal date weighting (festive shopping peak in Q4: Oct-Dec)
        month = random.choices(
            range(1, 13),
            weights=[0.07, 0.06, 0.08, 0.07, 0.08, 0.08, 0.08, 0.09, 0.09, 0.12, 0.14, 0.14]
        )[0]
        day = random.randint(1, 28 if month == 2 else 30)
        txn_date = datetime(2025, month, day)
        
        prod = random.choice(CATALOG)
        prod_id, prod_name, category, base_cost, base_price = prod
        
        # Small cost fluctuation (+/- 4%)
        cost = round(base_cost * random.uniform(0.96, 1.04), 2)
        # Retail pricing variation across customer batches
        price = round(base_price * random.uniform(0.99, 1.01), 2)
        
        # Quantity
        if category in ["Stationery", "Personal Care"]:
            units = random.choices([1, 2, 3, 4, 5, 6], weights=[0.35, 0.28, 0.18, 0.10, 0.06, 0.03])[0]
        else:
            units = random.choices([1, 2, 3, 4], weights=[0.60, 0.25, 0.10, 0.05])[0]
            
        # Category discounts
        if category == "Apparel":
            discount_pct = random.choices([0, 5, 10, 15, 20, 25, 30, 35, 40],
                                          weights=[0.15, 0.10, 0.15, 0.20, 0.15, 0.10, 0.08, 0.05, 0.02])[0]
        elif category == "Electronics":
            discount_pct = random.choices([0, 5, 10, 15, 20, 25],
                                          weights=[0.30, 0.25, 0.20, 0.15, 0.07, 0.03])[0]
        elif category == "Stationery":
            discount_pct = random.choices([0, 5, 10, 15],
                                          weights=[0.55, 0.25, 0.15, 0.05])[0]
        else:
            discount_pct = random.choices([0, 5, 10, 15, 20, 25],
                                          weights=[0.35, 0.25, 0.20, 0.10, 0.07, 0.03])[0]
        
        # Realistic return probability
        return_probs = {
            "Apparel": 0.085,
            "Electronics": 0.050,
            "Home & Kitchen": 0.035,
            "Personal Care": 0.025,
            "Stationery": 0.015
        }
        is_returned = "Yes" if random.random() < return_probs[category] else "No"
        
        payment = random.choices(PAYMENT_METHODS, weights=[0.55, 0.20, 0.15, 0.10])[0]
        customer = random.choices(CUSTOMER_SEGMENTS, weights=[0.50, 0.35, 0.15])[0]
        
        records.append({
            "Transaction_ID": txn_id,
            "Date": txn_date.strftime("%Y-%m-%d"),
            "Product_ID": prod_id,
            "Product_Name": prod_name,
            "Category": category,
            "Unit_Cost": cost,
            "Unit_Price": price,
            "Units_Sold": units,
            "Discount_Percent": discount_pct,
            "Payment_Method": payment,
            "Customer_Segment": customer,
            "Return_Status": is_returned
        })
        
    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    return df

if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, "small_business_sales.csv")
    
    print("Generating sales dataset...")
    df_sales = generate_transactions()
    df_sales.to_csv(output_file, index=False)
    
    print(f"Saved: {output_file} ({len(df_sales)} rows)")
