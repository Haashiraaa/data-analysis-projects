# Fitness Tracker Dashboard

**Visual analytics for personal fitness metrics tracking**

A data visualization project demonstrating professional dashboard creation for fitness and health monitoring. Tracks daily steps, calories burned, and sleep patterns across multiple users.

---

## What This Does

Creates a comprehensive 4-panel fitness analytics dashboard that visualizes:
- Daily step counts over a week (multi-user comparison)
- Total calories burned per user
- Average sleep hours with health recommendations
- Weekly summary statistics

**Demonstrates professional data visualization for health/fitness applications.**

---

## The Dashboard

Generates a professional visualization dashboard with:

### Panel 1: Daily Steps Trend
- Multi-line chart tracking steps for 3 users across the week
- Reference line showing 10K daily step goal
- Color-coded by user for easy comparison

### Panel 2: Total Calories Burned
- Bar chart comparing calorie expenditure across users
- Value labels for precise metrics
- Professional styling and formatting

### Panel 3: Average Sleep Hours
- Bar chart showing sleep patterns
- Reference line indicating recommended 7-hour target
- Identifies users meeting/missing sleep goals

### Panel 4: Weekly Summary Stats
- Total steps (all users combined)
- Average steps per day
- Total calories burned
- Average sleep hours

---

## Quick Start

### Prerequisites

This project uses **[haashi_pkg](https://github.com/Haashiraaa/my-packages)**, a custom-built data engineering and visualization toolkit.

### Installation

```bash
# Clone the repository
git clone https://github.com/Haashiraaa/data-analysis-projects.git            cd projects && cd fitness-tracker-dashboard

# Install haashi_pkg (custom package)
pip install git+https://github.com/Haashiraaa/my-packages.git

# Install other dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Generate the dashboard
python main.py
```

Dashboard will be saved to: `data/plots/fitness_tracker_dashboard.png`

**Individual modules:**
```bash
# Just run visualization
python visualize_data.py
```

---

## Project Structure

```
fitness-tracker-dashboard/
├── main.py              # Main execution script
├── setup_data.py        # Synthetic fitness data generation
├── visualize_data.py    # Dashboard visualization logic
├── requirements.txt     # Python dependencies
├── data/
│   └── plots/
│       └── fitness_tracker_dashboard.png  # Output dashboard
└── README.md
```

---

## Tech Stack

- **Python 3.x** - Core language
- **Pandas** - Data manipulation and analysis
- **Matplotlib** - Data visualization
- **[haashi_pkg](https://github.com/Haashiraaa/my-packages)** - Custom visualization toolkit (built from scratch)

---

## What This Demonstrates

### Data Visualization Skills
- Multi-panel dashboard layout design
- Line charts for temporal trends
- Bar charts for comparative analysis
- Reference lines for goal tracking
- Professional color schemes and styling

### Data Analysis Skills
- Multi-user fitness metric tracking
- Statistical aggregations (totals, averages)
- Health goal comparison (vs. recommended targets)
- Weekly trend analysis

### Software Engineering Skills
- Modular code organization (data setup, visualization separate)
- Reusable visualization components
- Clean, maintainable code structure
- Custom package integration

---

## Use Cases

This dashboard structure can be adapted for:
- Personal fitness tracking applications
- Health monitoring systems
- Corporate wellness programs
- Sports performance analytics
- Habit tracking dashboards
- Any multi-metric, multi-user comparison visualization

**The visualization approach is universal and scalable.**

---

## Key Features

**Professional Visualization:**
- Dark theme optimized for digital displays
- Color-coded user differentiation
- Reference lines for health goals
- Value labels for precise metrics
- Grid system for easy reading

**Health Insights:**
- Daily step goal tracking (10K steps)
- Sleep recommendation comparison (7 hours)
- Multi-user performance comparison
- Weekly aggregate statistics

**Technical Quality:**
- Custom PlotEngine for consistent styling
- Flexible layout using GridSpec
- Publication-ready output quality
- Scalable to additional users/metrics

---

## Sample Insights

Based on the dashboard visualization:
- **Step Goals:** Tracks who's hitting the 10K daily step target
- **Calorie Burn:** Compares total weekly calorie expenditure
- **Sleep Quality:** Identifies users meeting recommended sleep hours
- **Trends:** Shows day-by-day activity patterns for behavior insights

---

## Future Enhancements

Potential additions:
- [ ] Live data integration (fitness tracker APIs)
- [ ] Historical trend analysis (multi-week comparison)
- [ ] Heart rate and workout intensity metrics
- [ ] Interactive dashboard (Plotly/Dash)
- [ ] Automated weekly report generation
- [ ] Goal achievement notifications

---

## License

This project is available for portfolio and educational purposes.

---

**Built as part of a data visualization portfolio demonstrating professional dashboard creation capabilities.**
