# Project Report: Small Business Profitability Analysis

**Project ID:** DA-019  
**Domain:** Business Analytics  
**Course:** Data Analytics  

---

## 1. Project Overview
For small businesses, tracking sales revenue alone can be misleading. A company might see high sales numbers, but due to high product costs, heavy promotional discounts, and returned merchandise, the actual profit margin can be very low or even negative.

This project analyzes a retail sales dataset of **1,400 transactions** across 12 months in 2025 across 5 categories: **Electronics, Apparel, Home & Kitchen, Stationery, and Personal Care**. The goal is to calculate actual profits, evaluate category and product performance, analyze the effect of discounts, and provide actionable business recommendations.

---

## 2. Problem Statement & Objectives

### Problem Statement:
A small retail business knows its sales figures but lacks clarity on which products, product categories, or time periods generate the highest profit and better profit margins.

### Objectives:
1. Calculate Gross Revenue, Discounts, Net Revenue, COGS, Net Profit, and Profit Margin (%).
2. Compare profitability across different product categories.
3. Analyze the impact of customer discounts on profit margins.
4. Identify seasonal and monthly sales trends.
5. Rank products from highest to lowest margin to guide pricing and inventory decisions.

---

## 3. Assumptions and Mathematical Formulas

### Core Assumptions:
1. **Revenue is NOT Profit:** Total sales billing is reduced by cost of goods sold (COGS) to find net profit.
2. **Returns Handling:** If an order is marked as returned (`Return_Status == 'Yes'`), the Net Revenue is recorded as 0. Since the item is restocked into inventory, no COGS expense is assigned to that transaction.
3. **Discounts:** Discounts are applied directly to the selling price before calculating net revenue.

### Mathematical Formulas:
- **Gross Revenue:** $\text{Unit Price} \times \text{Units Sold}$
- **Discount Amount:** $\text{Gross Revenue} \times (\text{Discount Percent} / 100)$
- **Net Revenue:** $\text{Gross Revenue} - \text{Discount Amount}$ (0 if returned)
- **Total COGS:** $\text{Unit Cost} \times \text{Units Sold}$ (0 if returned)
- **Net Profit:** $\text{Net Revenue} - \text{Total COGS}$
- **Profit Margin (%):** $(\text{Net Profit} / \text{Net Revenue}) \times 100$

---

## 4. Key Findings

### 4.1 Summary Statistics
- **Total Transactions:** 1,400
- **Completed Sales:** 1,350
- **Returned Orders:** 50 (~3.6%)
- **Total Net Revenue:** ₹13,80,665.30
- **Total COGS:** ₹7,70,892.10
- **Total Net Profit:** ₹6,09,773.20
- **Overall Profit Margin:** **44.17%**

---

### 4.2 Category Performance (Chart 1)
- **Electronics:** Generated the highest net revenue (~₹4.8 Lakhs), but had a moderate profit margin (~35.2%) due to high procurement costs.
- **Stationery & Personal Care:** Delivered the highest profit margins (~56.4% and ~52.1% respectively). Although individual ticket sizes are lower, production costs are minimal.
- **Apparel:** Showed steady sales, but experienced the highest return rate (~8.5%) and frequent discounting.

---

### 4.3 Monthly Trends (Chart 2)
- Sales peaked in the fourth quarter (October to December), corresponding with the festive and holiday shopping season.
- Profit margins remained consistent across the year (between 43% and 46%), showing that base pricing is sustainable outside discount periods.

---

### 4.4 Impact of Discounts on Profit Margins (Chart 3)
- **0% Discount:** Average margin of **55.8%**.
- **1-10% Discount:** Average margin of **48.2%**.
- **11-20% Discount:** Average margin of **39.5%**.
- **21-30% Discount:** Average margin drops to **26.4%**.
- **Deep Discounts (>30%):** Profit margin drops sharply to **14.8%**.
- **Conclusion:** Offering discounts above 20% severely cuts into profitability without providing enough volume increase to compensate.

---

### 4.5 Product Margin Rankings (Chart 4)
- **Top 5 High-Margin Products:**
  1. Hardcover Ruled Journal (~64.2%)
  2. Retractable Gel Pen Set (~62.8%)
  3. Pastel Sticky Notes (~61.5%)
  4. Nourishing Shea Butter Hand Cream (~58.9%)
  5. Ceramic Coffee Mug (~57.4%)
- **Bottom 5 Low-Margin Products:**
  1. Mechanical Gaming Keyboard (~31.8%)
  2. Vintage Denim Jacket (~33.4%)
  3. Bluetooth Over-Ear Headphones (~35.1%)
  4. 10,000mAh Power Bank (~36.0%)
  5. Slim Fit Denim Jeans (~37.2%)

---

## 5. Business Recommendations

1. **Cap Discounts at 20%:** Discontinue standard promotional discounts exceeding 20% as they drop margins below 25%.
2. **Bundle Low-Margin with High-Margin Products:** Low-margin electronics attract customers; pairing them with high-margin stationery or accessories will improve overall basket margin.
3. **Supplier Price Renegotiation:** Since electronics have high purchase costs (up to 65% of price), renegotiating supplier bulk rates by even 5% will significantly improve net profit.
4. **Reduce Apparel Returns:** Better sizing descriptions and fit guidance can lower the return rate from 8.5% closer to the 3-4% seen in other categories.

---

## 6. Conclusion
The analysis demonstrates that revenue volume should not be the sole metric for business success. By evaluating cost structures, managing discount levels, and focusing on product mix, a small business can significantly improve its bottom line.
