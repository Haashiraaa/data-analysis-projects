# Retail Sales Data Analysis Report

**Date:** January 30, 2026  
**Analyzed by:** Haashiraaa

---

## Overview

I analyzed retail sales data from November 2023 to November 2025 to understand monthly revenue trends, category performance, and regional distribution patterns. The goal was to identify what's working, what's not, and where opportunities exist for growth and optimization.

---

## Key Findings

**Main Discovery 1:** Out of 500 raw sales records, 21 contained invalid values for price or quantity, requiring data cleaning before analysis.

**Main Discovery 2:** Product IDs in the dataset were not unique and could not serve as reliable identifiers for transactions.

**Main Discovery 3:** Category and region columns contained missing values that needed standardization, resulting in "Unknown" classifications for incomplete data.

---

## What The Data Shows

### Category Performance

Toys dominated category revenue at $199,581.50, with Furniture ($191,356.58) and Electronics ($187,084.33) following closely. Groceries, Clothing, Beauty, and Sports all performed solidly with revenues ranging between $150,000-$170,000. The only underperformer was an "Unknown" category that generated just $17,985.83, likely representing records with missing category data.

### Regional Performance

The top five regions showed strong and balanced performance with revenues between $200,000-$250,000. West led at $248,711.16, followed closely by East at $246,254.37, demonstrating stable profitability across most geographic markets. South, North, and Central regions all performed similarly in the $200,000-$235,000 range. The only outlier was an "Unknown" region at approximately $84,021.94, representing incomplete regional data.

### Trends Over Time

November 2023 started with low revenue ($7,586.96) but showed explosive growth of +303.7% in December 2023, followed by another strong climb of +82.2% in January 2024. The trend continued with fluctuations throughout 2024 & 2025, experiencing the steepest drop of -78.5% in June 2024. Two major revenue peaks occurred: April 2024 ($80,717.86) and August 2024 ($79,461.45). The latest data point (November 2025) shows revenue at $48,963.50.

---

## What This Means

- **Data quality matters:** 4.2% of records had invalid data, highlighting the importance of validation systems at data entry points to prevent bad data from entering the system.

- **Category diversification is strong:** Unlike many retail operations that rely heavily on one category, this business has balanced performance across 7 categories, reducing risk from market changes in any single product line.

- **Regional stability indicates scalability:** Five regions performing at similar levels suggests the business model works consistently across different markets, making expansion to new regions a viable growth strategy.

- **Seasonal patterns exist:** The dramatic swings (especially the June 2024 drop and subsequent recovery) suggest seasonal factors or campaign-driven sales that need to be understood and planned for.

- **Missing data cleanup needed:** The "Unknown" category and region represent lost revenue attribution that makes strategic planning harder - fixing data collection processes could improve decision-making.

---

## Recommendations

**Do This Now:**
- Investigate and fix the data collection process to eliminate the "Unknown" category and region entries in future data
- Analyze what caused the June 2024 revenue crash (-78.5%) to prevent similar drops
- Capitalize on the strong Toys category performance by ensuring adequate inventory during peak periods

**Consider For Later:**
- Study the April and August peaks to identify what drove those spikes - if they were marketing campaigns, replicate them
- Transfer operational best practices from West and East regions to boost Central and Unknown region performance
- Develop seasonal forecasting models based on the 2-year pattern to optimize inventory and staffing

**Watch Out For:**
- Sharp month-to-month volatility - implement early warning systems to detect downward trends before they become severe
- Over-reliance on any single category - continue monitoring to maintain balanced revenue distribution
- Data quality regression - regularly audit data entry processes to keep invalid records below 1%

---

## Visualizations

Dashboard saved at: `data/plots/retail_sales_plots.png`

**What's in the dashboard:**
- **Monthly Revenue Trend (Top Panel):** Line chart showing 24 months of revenue with growth percentages labeled, revealing seasonal patterns and major peaks/valleys
- **Total Revenue Per Category (Bottom Left):** Bar chart comparing all 8 product categories, with Toys, Furniture, and Electronics leading
- **Total Revenue Per Region (Bottom Center):** Bar chart showing geographic distribution across 6 regions, with West and East performing strongest
- **Sales Summary (Bottom Right):** Key statistics including total sales (479), total revenue ($1,239,971.43), average monthly revenue ($49,598.86), highest monthly revenue ($80,717.86), and lowest monthly revenue ($7,586.96)

---

## Technical Details

**Data processed:** 479 records (after cleaning from 500 raw records)  
**Time period:** November 2023 - November 2025 (24 months)  
**Tools used:** Python, Pandas, Matplotlib, Seaborn, Custom haashi_pkg toolkit  

**Files:**
- Raw data: `data/retail_sales.csv`
- Cleaned data: `data/cleaned_retail_sales.parquet`
- Visualizations: `data/plots/retail_sales_plots.png`

**Data Pipeline:**
1. Extracted 500 records from CSV source
2. Inspected data structure and identified quality issues (missing values, invalid records)
3. Handled missing values in category and region columns (filled with "Unknown")
4. Performed data type conversions:
   - Converted sale_date to datetime format for temporal analysis
   - Cast category and region to categorical dtype for memory efficiency
5. Identified and removed 21 invalid records with negative or zero values in price/quantity columns
6. Calculated derived metrics:
   - Created revenue column (price × quantity)
   - Generated sale_month feature for monthly aggregation
7. Sorted data by sale_date for chronological analysis
8. Validated final data quality and exported to optimized Parquet format
---

**End of Report**
