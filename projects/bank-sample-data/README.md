# Bank Statement Analysis

**Personal finance tracking and expenditure visualization**

A comprehensive financial data analysis project that processes bank statement data to provide insights into spending patterns. Includes synthetic data generation for privacy, automated categorization, and professional multi-panel dashboard visualization.

---

## What This Does

Analyzes bank statement transactions (Excel format) and generates detailed spending insights:
-  Monthly expenditure tracking and trends
-  Categorical spending breakdown
-  Spending distribution visualization (pie chart)
-  Summary statistics with key financial metrics
-  Privacy-focused: includes synthetic data generator for demonstrations

**Demonstrates professional financial data analysis and personal finance tracking capabilities.**

---

##  The Dashboard

Generates a comprehensive 4-panel financial analytics dashboard:

### Panel 1: Monthly Expenditure Line Chart
- Tracks total spending month-over-month
- Identifies spending trends and patterns
- Currency-formatted axis (Nigerian Naira ₦)

### Panel 2: Categorical Spending Bar Chart
- Compares spending across different categories
- Categories: Transfers, Purchases, Phone & Data, Electricity
- Value labels showing exact amounts spent

### Panel 3: Category Share Pie Chart
- Visual percentage breakdown of spending by category
- Color-coded for easy identification
- Legend with percentage details

### Panel 4: Summary Statistics Box
- Total amount spent
- Average spending per month
- Total number of debit transactions
- Biggest single expense

---

## Quick Start

### Prerequisites

This project uses **[haashi_pkg](https://github.com/Haashiraaa/my-packages)**, a custom-built data engineering and visualization toolkit.

### Installation

```bash
# Clone the repository

git clone https://github.com/Haashiraaa/data-analysis-projects.git
cd projects && cd bank-sample-data

# Install haashi_pkg (custom package)
pip install git+https://github.com/Haashiraaa/my-packages.git

# Install other dependencies
pip install -r requirements.txt
```

### Usage

**Run the complete pipeline (with synthetic data generation):**
```bash
cd pipeline
python main.py
```

This will:
1. Generate synthetic bank statement data (`sample_bank_statement_2025.xlsx`)
2. Clean and categorize transactions
3. Analyze spending patterns
4. Generate visualization dashboard
5. Save results to `data/plots/bank_statement_2025.png`

**Run individual modules:**
```bash
# Generate sample data only
python sample_data_generator.py

# Clean existing data
python clean_data.py

# Analyze cleaned data
python analyze_data.py

# Visualize analyzed data
python visualize_data.py
```


---

## Project Structure

```
bank-sample-data/
├── main.py                     # Main pipeline orchestrator
├── sample_data_generator.py   # Synthetic data generation
├── clean_data.py               # Data cleaning and categorization
├── analyze_data.py             # Statistical analysis
├── visualize_data.py           # Dashboard visualization
├── requirements.txt            # Python dependencies
├── data/
│   ├── sample_bank_statement_2025.xlsx     # Generated synthetic data
│   ├── bank_statement_2025.xlsx            # Real data (user-provided)
│   ├── cleaned_bank_statement_2025.parquet # Processed data
│   └── plots/
│       └── bank_statement_2025.png         # Output dashboard
└── README.md
```

---

## Tech Stack

- **Python 3.x** - Core language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Synthetic data generation
- **Matplotlib** - Data visualization
- **openpyxl** - Excel file handling
- **PyArrow** - Efficient Parquet storage
- **[haashi_pkg](https://github.com/Haashiraaa/my-packages)** - Custom data engineering toolkit (built from scratch)

---

## What This Demonstrates

### Data Engineering Skills
- Excel data loading with configurable row skipping
- Column name normalization
- Data type conversions (datetime, categorical, numeric)
- Missing data handling
- Efficient storage (Parquet format with compression)

### Data Cleaning & Privacy
- Transaction description masking/categorization
- Personal information filtering
- Pattern-based data cleaning
- Savings/investment transaction filtering
- Generic category creation

### Data Analysis Skills
- Monthly spending aggregation
- Categorical spending analysis
- Statistical metrics calculation (median, max, totals)
- Temporal trend analysis
- Financial pattern identification

### Data Visualization Skills
- Multi-panel dashboard layout
- Line charts for temporal trends
- Bar charts for categorical comparison
- Pie charts for distribution visualization
- Summary statistics boxes
- Professional dark-themed styling
- Currency-formatted axes

### Software Engineering Skills
- Modular code architecture
- Synthetic data generation for testing
- Configurable data sources (real vs. synthetic)
- Privacy-focused design
- Clean, maintainable code structure

---

## Use Cases

This analysis framework can be adapted for:
- Personal budgeting and expense tracking
- Financial planning applications
- Corporate expense analysis
- Subscription tracking
- Budget vs. actual comparisons
- Financial health monitoring
- Spending habit identification

**The pattern is universal for any transaction-based financial data.**

---

## Key Features

**Privacy & Security:**
- Synthetic data generator for safe demonstrations
- Transaction description masking
- Personal information filtering
- No sensitive data in repository

**Data Processing:**
- Automated categorization using regex patterns
- Configurable masking rules
- Debit transaction filtering
- Monthly aggregation

**Analysis Capabilities:**
- Month-over-month spending trends
- Category-based spending breakdown
- Statistical summaries
- Expense pattern identification

**Visualization:**
- 4-panel professional dashboard
- Multiple chart types (line, bar, pie)
- Currency formatting (₦)
- Dark theme optimized for readability
- Color-coded categories

---

## Transaction Categories

The system automatically categorizes transactions:
- **Transfers** - Peer-to-peer transfers
- **Phone & Data** - Mobile airtime, data, USSD charges
- **Electricity bill** - Utility payments
- **Purchases** - Card/merchant transactions

Categories can be customized by modifying `MASKING_RULES` in `clean_data.py`.

---

## Privacy Features

**Synthetic Data Generator:**
- Creates realistic but fake bank statements
- Safe for portfolio demonstrations
- Reproducible with seed value
- Customizable transaction count

**Data Masking:**
- Generic descriptions replace specific details
- Personal account numbers filtered out
- Savings/investment transactions removed
- Only spending patterns analyzed

---

## Future Enhancements

Potential additions:
- [ ] Budget goal tracking and alerts
- [ ] Income vs. expense comparison
- [ ] Year-over-year spending comparison
- [ ] Anomaly detection (unusual expenses)
- [ ] Predictive spending forecasts
- [ ] Category drill-down reports
- [ ] Interactive dashboard (Plotly/Dash)
- [ ] PDF report generation

---

## Data Format

Expected Excel bank statement format:
```
| Trans. Date | Value Date | Description | Debit(₦) | Credit(₦) | Balance After(₦) | Channel | Transaction Reference |
```

The cleaner handles:
- Header rows (configurable skip)
- Date format conversion
- Currency symbols
- Missing values
- Special characters

---

## License

This project is available for portfolio and educational purposes.

---

**Built as part of a data analysis portfolio demonstrating financial data processing, privacy-conscious design, and professional dashboard creation capabilities.**
