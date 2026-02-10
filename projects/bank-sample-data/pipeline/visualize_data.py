

# visualize_data.py

"""
Visualize Bank Statement Data

This module creates comprehensive visualizations of bank statement data including
monthly spending trends, categorical breakdowns, and summary statistics.

Functions:
    visualize_data: Create multi-panel dashboard visualization
"""

import sys
import logging
from typing import Optional

import matplotlib.dates as mdates
from haashi_pkg.plot_engine import PlotEngine
from haashi_pkg.utility import Logger
from analyze_data import aggregations


def visualize_data(
    save_path: str = "data/plots/bank_statement_2025.png",
    logger: Optional[Logger] = None
) -> None:
    """
    Create comprehensive bank statement visualization dashboard.

    Generates a multi-panel figure with:
    - Line plot: Monthly spending trends over time
    - Bar chart: Spending breakdown by category
    - Pie chart: Percentage share by category
    - Stats box: Summary statistics 

    Note:
        Calls aggregations() to get processed data. Ensure cleaned data
        exists at the default path before running.
    """
    # Initialize logger if not provided
    if logger is None:
        logger = Logger(level=logging.INFO)

    logger.info("Starting data visualization...")

    # Initialize PlotEngine
    logger.debug("Initializing PlotEngine")
    pe = PlotEngine(logger=logger)

    # Get aggregated data
    logger.debug("Loading aggregated data")
    result = aggregations(logger=logger)

    if result is None:
        logger.error("Aggregations returned None - cannot visualize")
        sys.exit(1)

    (
        monthly_spending,
        spend_by_category,
        avg_per_month,
        transaction_count,
        max_expense
    ) = result

    logger.info(f"Loaded data: {transaction_count} transactions across "
                f"{len(spend_by_category)} categories")

    # Define color scheme
    color_palette = pe.colors_vibrant[:3] + [pe.colors_vibrant[-1]]

    # Create figure with custom grid layout
    logger.debug("Creating figure layout (2 rows, 3 cols)")
    fig, gs = pe.create_custom_grid(
        rows=2,
        cols=3,
        figsize=(20, 10),
        height_ratios=[2, 1],
        hspace=0.6
    )

    # Define subplots
    ax_monthly = fig.add_subplot(gs[0, :])     # Top row, full width
    ax_category = fig.add_subplot(gs[1, 0])    # Bottom left
    ax_pie = fig.add_subplot(gs[1, 1])         # Bottom middle
    ax_stats = fig.add_subplot(gs[1, 2])       # Bottom right

    # Set figure title
    logger.debug("Setting figure title and background")
    pe.set_suptitle(
        fig,
        title="Bank Statement Analysis 2025",
        color="#4ECDC4",
        fontsize=18
    )
    gs.update(top=0.88)

    # Apply dark theme background
    pe.set_background_color(
        fig,
        (ax_monthly, ax_category, ax_pie, ax_stats),
        fig_color="#0f2027",
        ax_color="#1a3a4a",
        grid_color="#4ECDC4",
        grid_alpha=0.15,
        apply_to_all=True
    )

    # ═══════════════════════════════════════════════════════════════════
    # PANEL 1: Monthly Spending Line Plot
    # ═══════════════════════════════════════════════════════════════════

    logger.debug("Creating monthly spending line plot")

    # Convert period to timestamp for plotting
    months_timestamps = monthly_spending["months"].dt.to_timestamp()

    pe.draw(
        ax_monthly,
        x=months_timestamps,
        y=monthly_spending.total_spending,
        plot_type="line",
        color=pe.colors_vibrant[-2],
        linewidth=2.5,
        marker='o',
        markersize=8
    )

    # Customize grid
    ax_monthly.grid(
        True,
        alpha=0.15,
        color='#4ECDC4',
        linestyle='--',
        linewidth=0.8
    )

    # Add margins and labels
    pe.add_margins(ax_monthly, ypad=0.25)
    pe.decorate(
        ax_monthly,
        title="Monthly Expenditure Breakdown",
        xlabel="Months",
        ylabel="Amount Spent (₦)",
        ylim="zero",
        title_fontsize=14,
        label_fontsize=12
    )

    # Format x-axis dates
    pe.force_xticks(ax_monthly, months_timestamps, months_timestamps)
    ax_monthly.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

    # Format y-axis currency
    pe.format_y_axis(ax_monthly, currency="₦")

    # ═══════════════════════════════════════════════════════════════════
    # PANEL 2: Categorical Spending Bar Chart
    # ═══════════════════════════════════════════════════════════════════

    logger.debug("Creating categorical spending bar chart")

    pe.draw(
        ax_category,
        x=spend_by_category.category,
        y=spend_by_category.total_spending,
        plot_type="bar",
        label=spend_by_category.category,
        color=color_palette
    )

    pe.add_margins(ax_category, ypad=0.4)
    pe.decorate(
        ax_category,
        title="Categorical Expenditure",
        xlabel="Category",
        ylabel="Amount Spent (₦)",
        title_fontsize=14,
        label_fontsize=12
    )

    # Add value labels on bars
    pe.add_value_labels_on_bars(
        ax_category,
        format_string="₦{:,.0f}",
        fontsize=8,
        color="white"
    )

    # Format y-axis
    pe.format_y_axis(ax_category, currency="₦")

    # Add legend
    pe.set_legend(
        ax_category,
        loc="upper right",
        fontsize=10
    )

    # ═══════════════════════════════════════════════════════════════════
    # PANEL 3: Category Share Pie Chart
    # ═══════════════════════════════════════════════════════════════════

    logger.debug("Creating category share pie chart")

    # Calculate percentages
    spendings = spend_by_category.total_spending
    percentages = (spendings / spendings.sum()) * 100

    # Create custom legend labels with percentages
    legend_labels = [
        f"{category} — {pct:.1f}%"
        for category, pct in zip(spend_by_category.category, percentages)
    ]

    pe.draw(
        ax_pie,
        x=None,
        y=spendings,
        plot_type="pie",
        colors=color_palette,
        startangle=90,
    )

    # Set equal aspect ratio for circular pie
    ax_pie.set(aspect="equal")

    # Add custom legend
    ax_pie.legend(
        legend_labels,
        loc="upper right",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=11,
        frameon=True,
        fancybox=True
    )

    pe.decorate(
        ax_pie,
        title="Category Share (%)",
        title_fontsize=14
    )

    # ═══════════════════════════════════════════════════════════════════
    # PANEL 4: Summary Statistics Box
    # ═══════════════════════════════════════════════════════════════════

    logger.debug("Creating summary statistics box")

    stats = {
        "Total Spent": f"₦{spendings.sum():,.0f}",
        "Avg Per Month": f"₦{avg_per_month:,.0f}",
        "Total Transactions": f"{transaction_count}",
        "Biggest Expense": f"₦{max_expense:,.2f}",
    }

    pe.create_stats_text_box(
        ax_stats,
        stats=stats,
        title="SUMMARY",
        fontsize=13,
        title_fontsize=15,
        box_color="#1a3a4a",
        text_color="#4ECDC4",
        border_color="#4ECDC4"
    )

    # ═══════════════════════════════════════════════════════════════════
    # Save Figure
    # ═══════════════════════════════════════════════════════════════════

    logger.debug(f"Saving visualization to {save_path}")

    pe.save_or_show(
        fig,
        save_path=save_path,
        show=False,
        use_tight_layout=False,
        dpi=300
    )

    logger.info(f"Visualization saved to {save_path}")
    logger.info("Dashboard includes:")
    logger.info("  - Monthly spending trend (line plot)")
    logger.info("  - Category breakdown (bar chart)")
    logger.info("  - Category share (pie chart)")
    logger.info("  - Summary statistics")


def main() -> None:
    """Run visualization as standalone script."""
    logger = Logger(level=logging.INFO)

    try:
        logger.info("Starting bank statement visualization...")
        visualize_data(logger=logger)
        logger.info("Visualization completed successfully")

    except KeyboardInterrupt:
        logger.info("\n\nProcess interrupted by user")
        sys.exit(0)

    except Exception as e:
        logger.error(exception=e, save_to_json=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
