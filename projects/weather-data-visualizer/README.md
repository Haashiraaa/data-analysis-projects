# Weather Data Visualizer

**Historical weather pattern analysis and visualization**

A data visualization project that analyzes and displays historical temperature data from weather stations. Creates professional visualizations showing daily high/low temperatures with filled ranges for easy pattern identification.

---

## What This Does

Processes historical weather data (CSV format) and generates professional visualizations:
- Daily high and low temperature trends
- Temperature range visualization (filled area between highs and lows)
- Automatic date range detection and labeling
- Weather station identification

**Demonstrates professional weather data analysis and visualization capabilities.**

---

## The Visualization

Generates a single-panel professional chart with:

### Temperature Trend Chart
- **Dual-line plot** showing daily high and low temperatures
- **Filled area** between high/low for visual temperature range
- **Automatic labeling** with station name and date range
- **Clean, readable styling** with professional color scheme
- **Legend** distinguishing high vs. low temperatures

---

##  Quick Start

### Prerequisites

This project uses **[haashi_pkg](https://github.com/Haashiraaa/my-packages)**, a custom-built data engineering and visualization toolkit.

### Installation

```bash
# Clone the repository
git clone https://github.com/Haashiraaa/data-analysis-projects.git            cd projects && cd weather-data-visualizer

# Install haashi_pkg (custom package)
pip install git+https://github.com/Haashiraaa/my-packages.git

# Install other dependencies
pip install -r requirements.txt
```

### Usage

**Run the complete pipeline:**
```bash
cd pipeline
python main.py
```

This will:
1. Load weather data from `data/4150697.csv`
2. Clean and validate the data
3. Generate visualization
4. Save chart to `data/plots/weather_data.png`

**Run individual modules:**
```bash
# Just clean the data
python clean_data.py

# Just visualize (requires cleaned data structure)
python visualize_data.py
```

---

## Project Structure

```
weather-data-visualizer/
├── main.py              # Main pipeline orchestrator
├── clean_data.py        # Data cleaning and preprocessing
├── visualize_data.py    # Visualization generation
├── requirements.txt     # Python dependencies
├── data/
│   ├── 4150697.csv      # Raw weather data (station ID)
│   └── plots/
│       └── weather_data.png  # Output visualization
└── README.md
```

---

## Tech Stack

- **Python 3.x** - Core language
- **Pandas** - Data manipulation and cleaning
- **Matplotlib** - Data visualization
- **[haashi_pkg](https://github.com/Haashiraaa/my-packages)** - Custom data engineering toolkit (built from scratch)

---

##  What This Demonstrates

### Data Processing Skills
- CSV data loading and validation
- Column name normalization
- DateTime conversion and handling
- Missing data identification and removal
- Data sorting and preparation for visualization

### Data Analysis Skills
- Temperature trend analysis
- Date range extraction
- Station metadata handling
- Time-series data processing

### Data Visualization Skills
- Dual-line chart creation
- Filled area plots for ranges
- Professional color schemes
- Clear data labeling
- Legend and metadata display
- Publication-ready outputs

### Software Engineering Skills
- Modular code organization (cleaning separate from visualization)
- Reusable functions
- Error handling and user feedback
- Clean, maintainable code structure

---

## Use Cases

This visualization approach can be adapted for:
- Weather forecasting applications
- Climate change analysis
- Agricultural planning (temperature-based)
- Energy demand forecasting
- Historical weather comparisons
- Any time-series data with high/low ranges

**The pattern is universal: dual boundaries with filled ranges.**

---

## Key Features

**Data Cleaning:**
- Automatic column name standardization
- Missing value detection and removal
- DateTime conversion for proper temporal ordering
- Station name extraction

**Visualization:**
- High/low temperature dual-line plot
- Filled area showing temperature range
- Automatic title generation with station and date info
- Professional light-themed color scheme
- Clear axis labels and legends

**Technical Quality:**
- Custom PlotEngine for consistent styling
- Flexible date range handling
- Handles single or multiple weather stations
- Production-ready output quality

---

## Sample Insights

The visualization enables quick identification of:
- **Temperature Patterns:** Seasonal trends and variations
- **Daily Ranges:** Days with large temperature swings vs. stable days
- **Extremes:** Identification of unusually hot or cold periods
- **Trends:** Long-term warming or cooling patterns

---

## Future Enhancements

Potential additions:
- [ ] Multi-station comparison
- [ ] Precipitation data integration
- [ ] Moving average trend lines
- [ ] Anomaly detection (unusual temperatures)
- [ ] Interactive dashboard (Plotly)
- [ ] Monthly/seasonal aggregations
- [ ] Climate normal comparisons

---

## Data Source

Weather data is sourced from weather station records in CSV format. The station ID (e.g., `4150697`) identifies the specific weather station location. Data typically includes:
- Date
- Station name
- Maximum daily temperature (tmax)
- Minimum daily temperature (tmin)

---

## License

This project is available for portfolio and educational purposes.

---

**Built as part of a data visualization portfolio demonstrating weather data analysis and professional chart creation capabilities.**
