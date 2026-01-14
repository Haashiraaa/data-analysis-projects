
# visualize_data.py

import matplotlib.dates as mdates
from clean_data import clean_data
from haashi_pkg.plot_engine.plotengine import PlotEngine

SAVE_PATH: str = "_02_plot_images/weather_data.png"

pe = PlotEngine()


def visualize_data() -> None:

    weather_data_df, station_name, start_str, end_str = clean_data()
    dates = weather_data_df["date"].dt.to_period("D")
    dates = dates.dt.to_timestamp()

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

    pe.set_labels_and_title(
        ax,
        f"Daily Temperatures {start_str}-{end_str}\n{station_name}",
        "Dates",
        "Temperature (°F)"
    )
    pe.set_legend(
        ax,
        loc="lower right",
        title="Temperature Category",
        title_fontproperties={"weight": "bold", "size": 12}
    )
    pe.add_margins(ax, ypad=0.2)
    pe.set_axis_limits(ax, y_from_zero=True)

    pe.save_or_show(
        fig, save_path=SAVE_PATH, show=False, use_tight_layout=True
    )


if __name__ == "__main__":
    visualize_data()
