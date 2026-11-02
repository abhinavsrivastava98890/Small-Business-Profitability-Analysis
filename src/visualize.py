"""
Plotting functions using Matplotlib to generate project charts:
1. Category-wise Revenue vs Profit
2. Monthly Profitability and Revenue Trend
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def setup_chart_dir():
    chart_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "charts")
    os.makedirs(chart_dir, exist_ok=True)
    return chart_dir

def plot_category_revenue_profit(df: pd.DataFrame, save_path: str = None):
    cat_summary = df[df["Return_Status"] == "No"].groupby("Category").agg({
        "Net_Revenue": "sum",
        "Net_Profit": "sum"
    }).sort_values(by="Net_Profit", ascending=False)
    
    cat_summary["Margin_Pct"] = (cat_summary["Net_Profit"] / cat_summary["Net_Revenue"]) * 100
    
    categories = cat_summary.index.tolist()
    revenue_vals = cat_summary["Net_Revenue"] / 1000.0
    profit_vals = cat_summary["Net_Profit"] / 1000.0
    
    x = np.arange(len(categories))
    width = 0.38
    
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    
    ax.bar(x - width/2, revenue_vals, width, label="Net Revenue (₹ in '000)", color="#2b5c8f")
    rects2 = ax.bar(x + width/2, profit_vals, width, label="Net Profit (₹ in '000)", color="#2ca02c")
    
    ax.set_title("Category-wise Net Revenue vs Net Profit", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Product Category", fontsize=10, labelpad=8)
    ax.set_ylabel("Amount (₹ in Thousands)", fontsize=10, labelpad=8)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9.5)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    
    for i, rect in enumerate(rects2):
        height = rect.get_height()
        margin = cat_summary["Margin_Pct"].iloc[i]
        ax.annotate(f"₹{height:.1f}k\n({margin:.1f}%)",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center", va="bottom", fontsize=8.5, color="#1e6b1e")
                    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        return save_path
    return fig

def plot_monthly_trends(df: pd.DataFrame, save_path: str = None):
    valid_sales = df[df["Return_Status"] == "No"].copy()
    monthly = valid_sales.groupby("Month").agg({
        "Net_Revenue": "sum",
        "Net_Profit": "sum",
        "Month_Name": "first"
    }).reset_index().sort_values("Month")
    
    monthly["Margin_Pct"] = (monthly["Net_Profit"] / monthly["Net_Revenue"]) * 100
    
    fig, ax1 = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax2 = ax1.twinx()
    
    months = monthly["Month_Name"]
    rev_k = monthly["Net_Revenue"] / 1000.0
    profit_k = monthly["Net_Profit"] / 1000.0
    
    line1 = ax1.plot(months, rev_k, color="#1f77b4", marker="o", linewidth=2.2, label="Net Revenue (₹'000)")
    line2 = ax1.plot(months, profit_k, color="#2ca02c", marker="s", linewidth=2.2, label="Net Profit (₹'000)")
    ax1.fill_between(months, profit_k, color="#2ca02c", alpha=0.1)
    
    line3 = ax2.plot(months, monthly["Margin_Pct"], color="#d62728", linestyle="--", marker="^", linewidth=1.8, label="Profit Margin %")
    
    ax1.set_title("Monthly Revenue, Profit & Margin Dynamics", fontsize=13, fontweight="bold", pad=12)
    ax1.set_xlabel("Month", fontsize=10, labelpad=8)
    ax1.set_ylabel("Revenue & Profit (₹ in Thousands)", fontsize=10, color="#1f77b4")
    ax2.set_ylabel("Profit Margin (%)", fontsize=10, color="#d62728")
    
    ax1.grid(True, linestyle=":", alpha=0.5)
    
    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper left")
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        return save_path
    return fig

def generate_macro_charts():
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "small_business_sales.csv")
    from clean_data import validate_and_clean_data
    from metrics import enrich_sales_dataframe
    
    raw_df = pd.read_csv(data_path)
    clean_df = validate_and_clean_data(raw_df)
    enriched_df = enrich_sales_dataframe(clean_df)
    
    chart_dir = setup_chart_dir()
    plot_category_revenue_profit(enriched_df, os.path.join(chart_dir, "01_category_revenue_profit.png"))
    plot_monthly_trends(enriched_df, os.path.join(chart_dir, "02_monthly_profit_trend.png"))
    print("Macro trend charts generated successfully.")

if __name__ == "__main__":
    generate_macro_charts()
