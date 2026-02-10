

# visualize_data.py

"""Create fitness tracker dashboard visualization."""

import sys
import logging
from typing import Optional, Dict

from haashi_pkg.plot_engine import PlotEngine
from haashi_pkg.utility import Logger
from setup_data import setup_data


def visualize_data(
    savepath: str = "data/plots/fitness_tracker_dashboard.png",
    logger: Optional[Logger] = None
) -> None:
    """
    Create fitness tracker dashboard with daily steps, calories, and sleep data.

    Creates a 2x2 grid with:
    - Line plot: Daily steps for all users
    - Bar chart: Total calories burned
    - Bar chart: Average sleep hours
    - Stats box: Weekly summary
    """
    if logger is None:
        logger = Logger(level=logging.INFO)

    logger.info("Starting fitness dashboard visualization...")

    # Get data
    logger.debug("Loading fitness data")
    result = setup_data(logger=logger)

    if result is None:
        logger.error("Data setup returned None - cannot visualize")
        sys.exit(1)

    weekly_steps_df, user_metrics_df = result

    # Initialize PlotEngine
    logger.debug("Initializing PlotEngine")
    pe = PlotEngine(logger=logger)

    # Create figure
    logger.debug("Creating 2x2 grid layout")
    fig, ((ax_steps, ax_calories), (ax_sleep, ax_stats)) = pe.create_figure(
        2, 2,
        figsize=(16, 10),
        gridspec_kw={"width_ratios": [2, 1], "height_ratios": [1, 1]}
    )

    # Set title
    pe.set_suptitle(fig, title="Fitness Tracker Dashboard", color="white")

    # Apply dark theme
    logger.debug("Applying theme")
    pe.set_background_color(
        fig,
        (ax_steps, ax_calories, ax_sleep),
        fig_color="#141e30",
        ax_color="#243b55",
        grid_color="#4ECDC4",
        grid_alpha=0.2,
        apply_to_all=True
    )

    # User names
    users = ['alex', 'bree', 'carlos']

    # ═══════════════════════════════════════════════════════════════════
    # PANEL 1: Daily Steps Line Plot
    # ═══════════════════════════════════════════════════════════════════

    logger.debug("Creating daily steps line plot")

    for color, user in zip(pe.colors_01[:3], users):
        pe.draw(
            ax_steps,
            x=weekly_steps_df.days,
            y=weekly_steps_df[user],
            plot_type="line",
            label=user.title(),
            color=color,
            linewidth=2.5,
            marker='o',
            markersize=6
        )

    pe.add_margins(ax_steps, ypad=0.25)
    pe.decorate(
        ax_steps,
        title="Daily Steps",
        xlabel="Days",
        ylabel="Steps",
        ylim="zero"
    )

    pe.add_reference_line(
        ax_steps,
        y=10000,
        label="Goal: 10K",
        color="cyan",
        linestyle="--"
    )

    pe.format_y_axis(ax_steps, currency="")
    pe.set_legend(ax_steps, loc="lower right")

    # ═══════════════════════════════════════════════════════════════════
    # PANEL 2: Total Calories Bar Chart
    # ═══════════════════════════════════════════════════════════════════

    logger.debug("Creating calories bar chart")

    pe.draw(
        ax_calories,
        x=user_metrics_df.users,
        y=user_metrics_df.calories,
        plot_type="bar",
        color=pe.colors_01[:3]
    )

    pe.add_margins(ax_calories, ypad=0.45)
    pe.decorate(
        ax_calories,
        title="Total Calories Burned",
        xlabel="Users",
        ylabel="Calories",
        ylim="zero"
    )

    pe.add_value_labels_on_bars(
        ax_calories,
        format_string="{:.0f}",
        color="white",
        fontsize=10
    )

    pe.format_y_axis(ax_calories, currency="")

    # ═══════════════════════════════════════════════════════════════════
    # PANEL 3: Average Sleep Hours Bar Chart
    # ═══════════════════════════════════════════════════════════════════

    logger.debug("Creating sleep hours bar chart")

    pe.draw(
        ax_sleep,
        x=user_metrics_df.users,
        y=user_metrics_df.average_sleep_hours,
        plot_type="bar",
        color=pe.colors_01[:3]
    )

    pe.add_margins(ax_sleep, ypad=0.45)
    pe.decorate(
        ax_sleep,
        title="Average Sleep Hours",
        xlabel="Users",
        ylabel="Hours",
        ylim="zero"
    )

    pe.add_reference_line(
        ax_sleep,
        y=7,
        label="Recommended: 7h",
        color="cyan",
        linestyle="--"
    )

    pe.add_value_labels_on_bars(
        ax_sleep,
        format_string="{:.1f}",
        color="white",
        fontsize=10
    )

    pe.set_legend(ax_sleep, loc="upper right", fontsize=10)

    # ═══════════════════════════════════════════════════════════════════
    # PANEL 4: Weekly Summary Stats
    # ═══════════════════════════════════════════════════════════════════

    logger.debug("Creating weekly summary box")

    # Calculate totals
    total_steps = sum(weekly_steps_df[user].sum() for user in users)
    avg_steps = total_steps / (len(users) * len(weekly_steps_df))

    stats: Dict[str, str] = {
        "Total Steps": f"{int(total_steps):,}",
        "Avg Steps/Day": f"{int(avg_steps):,}",
        "Total Calories": f"{int(user_metrics_df.calories.sum()):,}",
        "Avg Sleep": f"{user_metrics_df.average_sleep_hours.mean():.1f}h"
    }

    pe.create_stats_text_box(
        ax_stats,
        stats=stats,
        title="WEEKLY SUMMARY",
        fontsize=13,
        title_fontsize=15,
        box_color="#243b55",
        text_color="#4ECDC4"
    )

    # Add footer note
    fig.text(
        0.5, 0.02,
        "All visualized data above represents cumulative results over one week.",
        ha='center',
        fontsize=12,
        color='white',
        style='italic',
        weight='bold'
    )

    # Save
    logger.debug(f"Saving visualization to {savepath}")

    pe.save_or_show(
        fig,
        save_path=savepath,
        show=False,
        bottom=0.08,
        dpi=300
    )

    logger.info(f"Dashboard saved to {savepath}")


def main() -> None:
    """Run visualization as standalone script."""
    logger = Logger(level=logging.INFO)

    try:
        logger.info("Starting fitness tracker visualization...")
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
