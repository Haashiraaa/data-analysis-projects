

# visualize_data.py


"""Create weather data visualization with temperature ranges."""

import sys
import logging
from typing import Optional

from haashi_pkg.plot_engine import PlotEngine
from haashi_pkg.utility import Logger
from clean_data import clean_data


def visualize_data(
    plotpath: str = "data/plots/weather_data.png",
    logger: Optional[Logger] = None
) -> None:
    """
    Create weather visualization showing daily temperature ranges.

    Displays high/low temperatures with shaded area between them.
    """
    if logger is None:
        logger = Logger(level=logging.INFO)

    logger.info("Starting weather data visualization...")

    # Get cleaned data
    logger.debug("Loading cleaned weather data")
    result = clean_data(logger=logger)

    if result is None:
        logger.error("Data cleaning returned None - cannot visualize")
        sys.exit(1)

    weather_df, station_name, start_str, end_str = result

    # Convert dates for plotting
    logger.debug("Preparing date data for plotting")
    dates = weather_df["date"].dt.to_period("D").dt.to_timestamp()

    # Initialize PlotEngine
    logger.debug("Initializing PlotEngine")
    pe = PlotEngine(logger=logger)

    # Create figure
    logger.debug("Creating figure")
    fig, ax = pe.create_figure(figsize=(14, 8))

    # Apply light theme
    logger.debug("Applying light theme")
    pe.set_background_color(
        fig, ax,
        fig_color="#e3f2fd",
        ax_color="#f5f9ff",
        grid_color="#90caf9",
        grid_alpha=0.3
    )

    # Plot high temperatures
    logger.debug("Plotting temperature data")
    pe.draw(
        ax,
        x=dates,
        y=weather_df.tmax,
        plot_type="line",
        color=pe.colors_01[-2],
        alpha=0.5,
        label="High",
        linewidth=2
    )

    # Plot low temperatures
    pe.draw(
        ax,
        x=dates,
        y=weather_df.tmin,
        plot_type="line",
        color=pe.colors_01[0],
        alpha=0.5,
        label="Low",
        linewidth=2
    )

    # Fill area between high and low
    ax.fill_between(
        dates,
        weather_df.tmax,
        weather_df.tmin,
        facecolor=pe.colors_01[0],
        alpha=0.1
    )

    # Decorate
    pe.add_margins(ax, ypad=0.2)
    pe.decorate(
        ax,
        title=f"Daily Temperatures {start_str}-{end_str}\n{station_name}",
        xlabel="Date",
        ylabel="Temperature (°F)",
        title_color="black",
        label_color="black",
        tick_color="black",
        ylim="zero"
    )

    # Add legend
    pe.set_legend(
        ax,
        loc="lower right",
        title="Temperature Category"
    )

    # Save
    logger.debug(f"Saving visualization to {plotpath}")
    pe.save_or_show(
        fig,
        save_path=plotpath,
        show=False,
        use_tight_layout=True,
        dpi=300
    )

    logger.info(f"Visualization saved to {plotpath}")


def main() -> None:
    """Run visualization as standalone script."""
    logger = Logger(level=logging.INFO)

    try:
        logger.info("Starting weather visualization...")
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

