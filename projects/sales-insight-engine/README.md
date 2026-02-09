# Sales Insight Engine

**Transform raw retail sales data into actionable business insights.**

A complete data analysis pipeline that cleans messy sales data, performs statistical analysis, and generates professional visualizations for business decision-making.

---

## What This Does

Takes raw retail sales data (CSV) and produces:
- Cleaned, validated dataset (Parquet format)
- Statistical analysis and insights
- Professional multi-panel visualization dashboard

**Not just data cleaning. Not just charts. Complete business intelligence pipeline.**

---

## The Pipeline

```
Raw CSV Data → Data Cleaning → Statistical Analysis → Visualization → Insights
```

### 1. Data Cleaning (`clean_data.py`)
- Handles missing values
- Removes duplicates
- Validates data types
- Standardizes formats
- Exports to efficient Parquet format

### 2. Data Analysis (`analyze_data.py`)
- Calculates key business metrics
- Identifies trends and patterns
- Generates statistical summaries
- Extracts actionable insights

### 3. Data Visualization (`visualize_data.py`)
- Creates professional multi-panel dashboard
- Distribution analysis
- Trend visualization
- Category breakdowns
- Publication-ready charts

---

## Quick Start

### Prerequisites

This project uses **[haashi_pkg](https://github.com/Haashiraaa/my-packages)**, a custom-built data engineering and visualization toolkit.

**What is haashi_pkg?**
A reusable Python package providing:
- `DataEngine` - Data cleaning, validation, and transformation
- `PlotEngine` - Professional visualization toolkit
- `DataLoader/DataSaver` - Efficient data I/O operations
- `Utility` - Logging and debugging tools

### Installation

```bash
# Clone the repository
git clone https://github.com/Haashiraaa/data-analysis-projects.git
cd projects && cd sales-insight-engine

# Install haashi_pkg (custom package)
pip install git+https://github.com/Haashiraaa/my-packages.git

# Install other dependencies
pip install -r requirements.txt
```

**Note:** haashi_pkg is a custom package built as part of this portfolio. Check out the [full documentation](https://github.com/Haashiraaa/my-packages) to see the complete toolkit.

### Usage

**Run the complete pipeline:**
```bash
cd pipeline
python main.py
```

This will:
1. Load raw sales data from `data/retail_sales.csv`
2. Clean and validate the data
3. Perform statistical analysis
4. Generate visualization dashboard
5. Save results to `data/` directory

**Run individual components:**
```bash
# Just clean the data
python clean_data.py

# Just analyze (requires cleaned data)
python analyze_data.py

# Just visualize (requires cleaned data)
python visualize_data.py
```

---

## Project Structure

```
sales-insight-engine/
├── main.py                  # Main pipeline orchestrator
├── clean_data.py           # Data cleaning module
├── analyze_data.py         # Statistical analysis module
├── visualize_data.py       # Visualization module
├── report.md               # Professional analysis report with findings
├── requirements.txt        # Python dependencies
├── data/
│   ├── retail_sales.csv    # Raw input data
│   ├── cleaned_retail_sales.parquet  # Cleaned output
│   └── plots/
│       └── retail_sales_plots.png    # Visualization dashboard
└── README.md
```

---

## Tech Stack

- **Python 3.x** - Core language
- **Pandas** - Data manipulation and cleaning
- **NumPy** - Numerical computations
- **Matplotlib** - Data visualization
- **Seaborn** - Statistical visualizations
- **PyArrow** - Efficient Parquet file handling
- **[haashi_pkg](https://github.com/Haashiraaa/my-packages)** - Custom data engineering toolkit (built from scratch)

---

## Analysis Report

A comprehensive analysis report (`report.md`) is included with this project, featuring:
- **Executive insights** from the data analysis
- **Key findings** across categories, regions, and time periods
- **Detailed analysis** of revenue patterns and trends
- **Actionable recommendations** for business decisions
- **Technical documentation** of the data pipeline

The report demonstrates professional business intelligence delivery, combining technical analysis with strategic insights.

---

## What This Demonstrates

### Data Engineering Skills
- ETL pipeline design
- Data validation and cleaning
- Efficient data storage (Parquet format)
- Modular code architecture

### Data Analysis Skills
- Statistical analysis
- Trend identification
- Business metrics calculation
- Insight extraction

### Data Visualization Skills
- Multi-panel dashboard creation
- Professional chart styling
- Visual storytelling
- Publication-ready outputs

### Software Engineering Skills
- Modular design (separate concerns)
- Clean, maintainable code
- Reusable components
- Production-ready structure

---

## Use Cases

This pipeline structure can be adapted for:
- Retail sales analysis
- E-commerce metrics tracking
- Inventory management insights
- Customer behavior analysis
- Financial reporting
- Marketing performance analysis

**The approach is universal: Clean → Analyze → Visualize → Decide**

---

## Key Takeaways

**This isn't a tutorial project.**

This is a real data analysis workflow that solves actual business problems:
- Messy data gets cleaned properly
- Analysis produces actionable insights
- Visualizations communicate findings clearly
- Modular design allows easy adaptation
- **Built using custom reusable package** ([haashi_pkg](https://github.com/Haashiraaa/my-packages)) - demonstrating ability to create and maintain production tools

**From raw data to business decisions in one pipeline.**

---

## Future Enhancements

Potential additions:
- [ ] Automated anomaly detection
- [ ] Interactive dashboards (Plotly/Dash)
- [ ] Database integration (PostgreSQL)
- [ ] Automated reporting (PDF generation)
- [ ] Time series forecasting
- [ ] API endpoint for live data

---

## License

This project is available for portfolio and educational purposes.

---

**Built as part of a data analysis portfolio demonstrating end-to-end pipeline capabilities.**
