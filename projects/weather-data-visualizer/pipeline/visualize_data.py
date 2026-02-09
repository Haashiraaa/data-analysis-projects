

# visualize_data.py

import sys
import logging
from clean_data import clean_data
from haashi_pkg.plot_engine import PlotEngine
from haashi_pkg.utility import Logger

# pyright: basic

logger = Logger(level=logging.INFO)


def visualize_data(
    plotpath: str = "data/plots/weather_data.png",
    logger: Logger = logger,
) -> None:

    weather_data_df, station_name, start_str, end_str = clean_data()
    dates = weather_data_df["date"].dt.to_period("D")
    dates = dates.dt.to_timestamp()

    logger.debug("Visualizing data...")
    pe = PlotEngine(logger=logger)
    fig, ax = pe.create_figure(figsize=(14, 8))

    pe.set_background_color(
        fig, ax,
        fig_color="#e3f2fd",
        ax_color="#f5f9ff",
        grid_color="#90caf9",
        grid_alpha=0.3
    )
    pe.draw(
        ax,
        dates,
        weather_data_df.tmax,
        color=pe.colors_01[-2],
        alpha=0.5,
        label="High",
    )

    pe.draw(
        ax,
        dates,
        weather_data_df.tmin,
        color=pe.colors_01[0],
        alpha=0.5,
        label="Low"
    )

    ax.fill_between(
        dates,
        weather_data_df.tmax,
        weather_data_df.tmin,
        facecolor=pe.colors_01[0],
        alpha=0.1
    )

    pe.add_margins(ax, ypad=0.2)
    pe.decorate(
        ax,
        title=f"Daily Temperatures {start_str}-{end_str}\n{station_name}",
        xlabel="Date",
        ylabel="Temperature (°F)",
        title_color="black",
        label_color="black",
        tick_color="black",
        ylim="zero",
    )
    pe.set_legend(
        ax,
        loc="lower right",
        title="Temperature Category",
        title_fontproperties={"weight": "bold", "size": 12}
    )

    pe.save_or_show(
        fig, save_path=plotpath, show=False, use_tight_layout=True
    )
    logger.info(f"Plot saved to {plotpath}")


if __name__ == "__main__":
    try:
        visualize_data()
    except KeyboardInterrupt:
        logger.info("\nVisualization process interrupted.")
        sys.exit(0)
