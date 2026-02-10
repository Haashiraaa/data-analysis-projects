

# visualize_data.py


"""Create retail sales visualization dashboard."""

import sys
import logging
from typing import Optional, Dict

import matplotlib.dates as mdates
from haashi_pkg.plot_engine import PlotEngine
from haashi_pkg.utility import Logger
from analyze_data import analyze_data


def visualize_data(
    plotpath: str = "data/plots/retail_sales_plots.png",
    logger: Optional[Logger] = None
) -> None:
    """Create comprehensive retail sales visualization dashboard."""
    if logger is None:
        logger = Logger(level=logging.INFO)

    logger.info("Starting visualization...")

    # Get analyzed data
    logger.debug("Loading analyzed data")
    result = analyze_data(logger=logger)

    if result is None:
        logger.error("Analysis returned None - cannot visualize")
        sys.exit(1)

    (
        sales_df,
        category_revenue,
        region_revenue,
        monthly_revenue,
        start_date,
        end_date,
    ) = result

    # Initialize PlotEngine
    logger.debug("Initializing PlotEngine")
    pe = PlotEngine(logger=logger)

    # Color scheme
    color_palette = pe.colors_03 + pe.colors_vibrant[:3]

    # Create figure layout
    logger.debug("Creating figure layout")
    fig, gs = pe.create_custom_grid(
        rows=2,
        cols=5,
        figsize=(40, 18),
        hspace=0.6
    )

    # Define subplots
    ax_monthly = fig.add_subplot(gs[0, :])      # Top row, full width
    ax_category = fig.add_subplot(gs[1, 0:2])   # Bottom left
    ax_region = fig.add_subplot(gs[1, 2:4])     # Bottom middle
    ax_stats = fig.add_subplot(gs[1, 4])        # Bottom right

    # Set background
    logger.debug("Applying theme")
    pe.set_background_color(
        fig,
        (ax_monthly, ax_category, ax_region, ax_stats),
        fig_color="#1a2332",
        ax_color="#2a3f54",
        grid_color="#4ECDC4",
        grid_alpha=0.15,
        apply_to_all=True
    )

    # Set title
    pe.set_suptitle(
        fig,
        title=f"Retail Sales Analysis {start_date}-{end_date}",
        color="#4ECDC4",
        fontsize=18
    )
    gs.update(top=0.88)

    # ═══════════════════════════════════════════════════════════════════
    # PANEL 1: Monthly Revenue Line Plot
    # ═══════════════════════════════════════════════════════════════════

    logger.debug("Creating monthly revenue plot")

    months = monthly_revenue.sale_month.dt.to_timestamp()

    pe.draw(
        ax_monthly,
        x=months,
        y=monthly_revenue.total_revenue,
        plot_type="line",
        color=color_palette[0],
        linewidth=2.5,
        marker='o',
        markersize=8
    )

    # Add percentage change labels
    y_range = ax_monthly.get_ylim()[1] - ax_monthly.get_ylim()[0]
    offset = y_range * 0.04

    for i in range(1, len(monthly_revenue)):
        x = months.iloc[i]
        y = monthly_revenue.total_revenue.iloc[i]
        pct = monthly_revenue.revenue_pct_change_pct.iloc[i]

        label_color = "#6BCB77" if pct > 0 else "#FF6B6B"

        ax_monthly.text(
            x, y + offset,
            f"{pct:+.1f}%",
            fontsize=8,
            fontweight="bold",
            color=label_color,
            ha="center",
            va="bottom"
        )

    pe.add_margins(ax_monthly, ypad=0.2)
    pe.decorate(
        ax_monthly,
        title="Monthly Revenue",
        xlabel="Months",
        ylabel="Revenue ($)",
        ylim="zero"
    )

    pe.force_xticks(ax_monthly, months, months)
    ax_monthly.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    pe.format_y_axis(ax_monthly, currency="$")

    # ═══════════════════════════════════════════════════════════════════
    # PANEL 2: Category Revenue Bar Chart
    # ═══════════════════════════════════════════════════════════════════

    logger.debug("Creating category revenue bar chart")

    pe.draw(
        ax_category,
        x=category_revenue.category,
        y=category_revenue.total_revenue,
        plot_type="bar",
        label=category_revenue.category,
        color=color_palette
    )

    pe.add_margins(ax_category, ypad=0.4)
    pe.decorate(
        ax_category,
        title="Total Revenue Per Category",
        xlabel="Category",
        ylabel="Revenue ($)"
    )

    pe.add_value_labels_on_bars(
        ax_category,
        format_string="${:,.0f}",
        fontsize=8,
        color="white"
    )

    pe.format_y_axis(ax_category, currency="$")
    pe.set_legend(
        ax_category,
        loc="upper right",
        fontsize=10,
        title="Categories"
    )

    # ═══════════════════════════════════════════════════════════════════
    # PANEL 3: Regional Revenue Bar Chart
    # ═══════════════════════════════════════════════════════════════════

    logger.debug("Creating regional revenue bar chart")

    pe.draw(
        ax_region,
        x=region_revenue.region,
        y=region_revenue.total_revenue,
        plot_type="bar",
        label=region_revenue.region,
        color=color_palette[:6]
    )

    pe.add_margins(ax_region, ypad=0.4)
    pe.decorate(
        ax_region,
        title="Total Revenue Per Region",
        xlabel="Region",
        ylabel="Revenue ($)"
    )

    pe.add_value_labels_on_bars(
        ax_region,
        format_string="${:,.0f}",
        fontsize=8,
        color="white"
    )

    pe.format_y_axis(ax_region, currency="$")
    pe.set_legend(
        ax_region,
        loc="upper right",
        fontsize=10,
        title="Regions"
    )

    # ═══════════════════════════════════════════════════════════════════
    # PANEL 4: Summary Statistics
    # ═══════════════════════════════════════════════════════════════════

    logger.debug("Creating summary statistics box")

    total_revenue = monthly_revenue.total_revenue

    stats: Dict[str, str] = {
        "Total Sales": f"{len(sales_df):,}",
        "Total Revenue": f"${total_revenue.sum():,.2f}",
        "Avg Per Month": f"${total_revenue.mean():,.2f}",
        "Highest Month": f"${total_revenue.max():,.2f}",
        "Lowest Month": f"${total_revenue.min():,.2f}"
    }

    pe.create_stats_text_box(
        ax_stats,
        stats=stats,
        title="SALES SUMMARY",
        fontsize=13,
        box_color="#2a3f54",
        text_color="#4ECDC4"
    )

    # Save
    logger.debug(f"Saving visualization to {plotpath}")
    pe.save_or_show(
        fig,
        dpi=96,
        save_path=plotpath,
        show=False,
        use_tight_layout=False
    )

    logger.info(f"Visualization saved to {plotpath}")


def main() -> None:
    """Run visualization as standalone script."""
    logger = Logger(level=logging.INFO)

    try:
        logger.info("Starting retail sales visualization...")
        visualize_data(logger=logger)
        logger.info("Visualization completed")

    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user")
        sys.exit(0)

    except Exception as e:
        logger.error(exception=e, save_to_json=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
