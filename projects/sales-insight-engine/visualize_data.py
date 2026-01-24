
# visualize_data.py

import sys
import matplotlib.dates as mdates
from haashi_pkg.plot_engine.plotengine import PlotEngine
from analyze_data import analyze_data

SAVEPATH: str = "_03_plot_images/revenue_by_category.png"


def visualize_data() -> None:

    pe = PlotEngine()

    SET_COLOR_1 = pe.colors_03 + pe.colors_vibrant[:3]

    fig, gs = pe.create_custom_grid(2, 5, figsize=(40, 18))
    ax1 = fig.add_subplot(gs[0, :])
    ax2 = fig.add_subplot(gs[1, 0:2])
    ax3 = fig.add_subplot(gs[1, 2:4])
    ax4 = fig.add_subplot(gs[1, 4])

    # ----------------
    # Background Color
    # ----------------
    pe.set_background_color(
        fig,
        (ax1, ax2, ax3, ax4),  # type: ignore
        fig_color="#1a2332",
        ax_color="#2a3f54",
        grid_color="#4ECDC4",
        grid_alpha=0.15,
        apply_to_all=True
    )

    (
        sales_df,
        category_revenue,
        region_revenue,
        monthly_revenue,
        start_date,
        end_date,
    ) = analyze_data()  # type: ignore

    pe.set_suptitle(
        f"Retail Sales Analysis {start_date}-{end_date} ", color="#4ECDC4"
    )
    gs.update(top=0.88, hspace=0.6)

    # ----------------------------
    # Line Plot -> Monthly Revenue
    # ----------------------------

    months = monthly_revenue.sale_month.dt.to_timestamp()

    pe.draw(
        ax1,
        months,
        monthly_revenue.total_revenue,
        color=SET_COLOR_1[0],
        linewidth=2.5,
        marker='o'
    )

    y_range = ax1.get_ylim()[1] - ax1.get_ylim()[0]
    offset = y_range * 0.04  # 3% of y-range

    for i in range(1, len(monthly_revenue)):
        x = months.iloc[i]
        y = monthly_revenue.total_revenue.iloc[i]
        pct = monthly_revenue.revenue_pct_change_pct.iloc[i]

        # Color based on increase/decrease
        label_color = "#6BCB77" if pct > 0 else "#FF6B6B"

        ax1.text(
            x, y + offset,
            f"{pct:+.1f}%",
            fontsize=8,
            fontweight="bold",
            color=label_color,
            ha="center",
            va="bottom"
        )

    pe.set_labels_and_title(
        ax1,
        title="Monthly Revenue",
        xlabel="Months",
        ylabel="Revenue ($)",
    )

    pe.add_margins(ax1, ypad=0.2)
    pe.force_xticks(ax1, months, months)  # type: ignore
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    pe.set_axis_limits(ax1, y_from_zero=True)
    pe.format_y_axis(ax1, currency="$")

    # ---------------------------------
    # Bar Chart — Category Revenue
    # ---------------------------------
    pe.draw(
        ax2,
        category_revenue.category,
        category_revenue.total_revenue,
        plot_type="bar",
        label=category_revenue.category,
        color=SET_COLOR_1
    )

    pe.set_labels_and_title(
        ax2, "Total Revenue Per Category", "Category", "Revenue ($)"
    )
    pe.add_margins(ax2, ypad=0.4)
    pe.add_value_labels_on_bars(
        ax2, format_string="${:,.2f}", fontsize=8, color="white"
    )
    pe.format_y_axis(ax2, currency="$")
    pe.set_legend(
        ax2,
        loc="upper right",
        fontsize=10,
        title="Categories",
        title_fontproperties={"weight": "bold", "size": 12}
    )

    # ---------------------------------
    # Bar Chart — Regional Revenue
    # ---------------------------------
    pe.draw(
        ax3,
        region_revenue.region,
        region_revenue.total_revenue,
        plot_type="bar",
        label=region_revenue.region,
        color=SET_COLOR_1[0:6]
    )

    pe.set_labels_and_title(
        ax3, "Total Revenue Per Region", "Region", "Revenue ($)"
    )
    pe.add_margins(ax3, ypad=0.4)
    pe.add_value_labels_on_bars(
        ax3, format_string="${:,.2f}", fontsize=8, color="white"
    )
    pe.format_y_axis(ax3, currency="$")
    pe.set_legend(
        ax3,
        loc="upper right",
        fontsize=10,
        title="Regions",
        title_fontproperties={"weight": "bold", "size": 12}
    )

    # -----------------
    # Stats Summary Box
    # -----------------

    tr = monthly_revenue.total_revenue

    stats = {
        "Total Sales": f"{len(sales_df)}",
        "Total Revenue": f"${tr.sum():,.2f}",
        "Avg Revenue Per Month": f"${tr.mean():,.2f}",
        "Highest Monthly Revenue": f"${tr.max():,.2f}",
        "Lowest Monthly Revenue": f"${tr.min():,.2f}"
    }

    pe.create_stats_text_box(
        ax4,
        stats,
        title="SALES SUMMARY",
        fontsize=13
    )

    # -----------------------
    # Set Text Colors
    # -----------------------
    pe.set_text_colors((ax1, ax2, ax3))  # type: ignore

    # -----------
    # Saving plot
    # -----------
    pe.save_or_show(
        fig,
        save_path=SAVEPATH,
        show=False,
        use_tight_layout=False
    )


if __name__ == "__main__":
    try:
        visualize_data()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
