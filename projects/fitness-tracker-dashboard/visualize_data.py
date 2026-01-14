

# plot_data.py

from setup_data import setup_data
from haashi_pkg.plot_engine.plotengine import PlotEngine


pe = PlotEngine()


def main():
    ws_df, um_df = setup_data()

    # Create 2x2 grid
    fig, ((ax1, ax2), (ax3, ax4)) = pe.create_figure(
        2, 2, figsize=(16, 10),
        gridspec_kw={"width_ratios": [2, 1], "height_ratios": [1, 1]}
    )

    pe.set_suptitle("Fitness Tracker Dashboard", color="white")

    users: list[str] = ['alex', 'bree', 'carlos']

    # -------------------
    # Background Color
    # -------------------
    pe.set_background_color(
        fig,
        (ax1, ax2, ax3),
        fig_color="#141e30",
        ax_color="#243b55",
        grid_color="#4ECDC4",
        grid_alpha=0.2,
        apply_to_all=True
    )

    # -----------------------
    # Line Plot — Daily Steps
    # -----------------------
    for col, user in zip(pe.colors_01[0:3], users):
        pe.draw(
            ax1,
            ws_df.days,
            ws_df[user],
            label=user.title(),
            color=col,
            linewidth=2.5,
            marker='o'
        )

    pe.set_labels_and_title(ax1, "Daily Steps", "Days", "Steps")
    pe.add_margins(ax1, ypad=0.15)
    pe.set_axis_limits(ax1, y_from_zero=True)
    pe.add_reference_line(ax1, y=10000, label="Goal: 10K", color="cyan")
    pe.format_y_axis(ax1, currency="")
    pe.set_legend(ax1, loc="lower right")

    # ---------------------------------
    # Bar Chart — Total Calories Burned
    # ---------------------------------
    pe.draw(
        ax2,
        um_df.users,
        um_df.calories,
        plot_type="bar",
        color=pe.colors_01[0:3]
    )

    pe.set_labels_and_title(ax2, "Total Calories Burned", "Users", "Calories")
    pe.add_margins(ax2, ypad=0.45)
    pe.set_axis_limits(ax2, y_from_zero=True)
    pe.add_value_labels_on_bars(ax2, format_string="{:.0f}", color="white")
    pe.format_y_axis(ax2, currency="")

    # ---------------------------------
    # Bar Chart — Average Sleep Hours
    # ---------------------------------
    pe.draw(
        ax3,
        um_df.users,
        um_df.average_sleep_hours,
        plot_type="bar",
        color=pe.colors_01[0:3]
    )

    pe.set_labels_and_title(ax3, "Average Sleep Hours", "Users", "Hours")
    pe.set_axis_limits(ax3, ylim=(0, 10))
    pe.add_reference_line(ax3, y=7, label="Recommended: 7h", color="cyan")
    pe.add_value_labels_on_bars(ax3, format_string="{:.1f}", color="white")
    pe.set_legend(ax3, loc="upper right", fontsize=10)

    # ---------------------------------
    # Stats Summary Box
    # ---------------------------------
    total_steps = sum(ws_df[user].sum() for user in users)
    avg_steps = total_steps / (len(users) * len(ws_df))

    stats = {
        "Total Steps": total_steps,
        "Avg Steps/Day": int(avg_steps),
        "Total Calories": um_df.calories.sum(),
        "Avg Sleep": um_df.average_sleep_hours.mean()
    }

    pe.create_stats_text_box(
        ax4,
        stats,
        title="WEEKLY SUMMARY",
        fontsize=13,
        title_fontsize=15
    )

    # ---------------
    # Set Text Colors
    # ---------------

    pe.set_text_colors((ax1, ax2, ax3))

    # ---------------
    # Figure text
    # ---------------

    fig.text(
        0.5,
        0.02,
        "All visualized data above represents cumulative results over one week.",
        ha='center',
        fontsize=12,
        color='white',
        style='italic',
        weight='bold'
    )

    # -------------------
    # Saving plot
    # -------------------
    pe.save_or_show(
        fig,
        save_path="plot_images/fitness_tracker_dashboard.png",
        show=False,
        bottom=0.5
    )


if __name__ == "__main__":
    main()
