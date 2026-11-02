"""
Plotting functions using Matplotlib to generate project charts:
1. Category-wise Revenue vs Profit
2. Monthly Profitability and Revenue Trend
3. Discount Impact on Profit Margin
4. Top 5 vs Bottom 5 Products by Profit Margin
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

def plot_discount_impact(df: pd.DataFrame, save_path: str = None):
    valid_sales = df[df["Return_Status"] == "No"].copy()
    
    bracket_summary = valid_sales.groupby("Discount_Bracket", observed=False).agg({
        "Profit_Margin_Pct": "mean",
        "Net_Revenue": "sum",
        "Net_Profit": "sum"
    }).reset_index()
    
    bracket_summary["Realized_Margin"] = (bracket_summary["Net_Profit"] / bracket_summary["Net_Revenue"]) * 100
    
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    
    brackets = bracket_summary["Discount_Bracket"].astype(str)
    margins = bracket_summary["Realized_Margin"]
    colors = ["#2ca02c", "#70b028", "#d4ac0d", "#e67e22", "#d9534f"]
    
    bars = ax.bar(brackets, margins, color=colors, width=0.55, edgecolor="#444444")
    
    ax.set_title("Realized Profit Margin (%) by Discount Tier", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Discount Tier", fontsize=10, labelpad=8)
    ax.set_ylabel("Realized Profit Margin (%)", fontsize=10, labelpad=8)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.1f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha="center", va="bottom", fontsize=9.5, fontweight="bold")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        return save_path
    return fig

def plot_product_rankings(df: pd.DataFrame, save_path: str = None):
    valid_sales = df[df["Return_Status"] == "No"].copy()
    
    prod_summary = valid_sales.groupby(["Product_Name", "Category"]).agg({
        "Net_Revenue": "sum",
        "Net_Profit": "sum"
    }).reset_index()
    
    prod_summary["Margin_Pct"] = (prod_summary["Net_Profit"] / prod_summary["Net_Revenue"]) * 100
    prod_summary = prod_summary.sort_values("Margin_Pct", ascending=False)
    
    top_5 = prod_summary.head(5).copy()
    bottom_5 = prod_summary.tail(5).copy()
    combined = pd.concat([bottom_5, top_5]).reset_index(drop=True)
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    y_pos = np.arange(len(combined))
    colors = ["#e74c3c" if m < 35 else "#27ae60" for m in combined["Margin_Pct"]]
    
    bars = ax.barh(y_pos, combined["Margin_Pct"], color=colors, height=0.6, edgecolor="#444444")
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(combined["Product_Name"], fontsize=9)
    ax.set_xlabel("Profit Margin (%)", fontsize=10, labelpad=8)
    ax.set_title("Product Margin Comparison: Top 5 vs Bottom 5", fontsize=13, fontweight="bold", pad=12)
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    
    for bar, margin in zip(bars, combined["Margin_Pct"]):
        w = bar.get_width()
        ax.annotate(f"{margin:.1f}%",
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0),
                    textcoords="offset points",
                    ha="left", va="center", fontsize=8.5)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        return save_path
    return fig

def generate_all_charts():
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "small_business_sales.csv")
    from clean_data import validate_and_clean_data
    from metrics import enrich_sales_dataframe
    
    raw_df = pd.read_csv(data_path)
    clean_df = validate_and_clean_data(raw_df)
    enriched_df = enrich_sales_dataframe(clean_df)
    
    chart_dir = setup_chart_dir()
    plot_category_revenue_profit(enriched_df, os.path.join(chart_dir, "01_category_revenue_profit.png"))
    plot_monthly_trends(enriched_df, os.path.join(chart_dir, "02_monthly_profit_trend.png"))
    plot_discount_impact(enriched_df, os.path.join(chart_dir, "03_discount_vs_profit_margin.png"))
    plot_product_rankings(enriched_df, os.path.join(chart_dir, "04_top_bottom_products_margin.png"))
    print("Charts generated successfully.")

if __name__ == "__main__":
    generate_all_charts()
