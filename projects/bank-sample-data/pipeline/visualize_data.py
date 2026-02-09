

# visualize_data.py

import matplotlib.dates as mdates

import sys
import logging
from haashi_pkg.plot_engine import PlotEngine
from haashi_pkg.utility import Logger
from analyze_data import aggregations

# pyright: basic

logger = Logger(level=logging.INFO)


def visualize_data(
    SAVE_PATH: str = "data/plots/bank_statement_2025.png",
    logger: Logger = logger
) -> None:

    logger.debug("Visualizing data...")
    pe = PlotEngine(logger=logger)

    SET_COLOR: list[str] = pe.colors_vibrant[:3] + [pe.colors_vibrant[-1]]

    fig, gs = pe.create_custom_grid(2, 3)
    ax1 = fig.add_subplot(gs[0, :])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1])
    ax4 = fig.add_subplot(gs[1, 2])

    pe.set_suptitle(
        fig, title="Bank Statement Analysis 2025", color="#4ECDC4"
    )
    gs.update(top=0.88, hspace=0.6)

    # ----------------
    # Background Color
    # ----------------
    pe.set_background_color(
        fig,
        (ax1, ax2, ax3, ax4),
        fig_color="#0f2027",
        ax_color="#1a3a4a",
        grid_color="#4ECDC4",
        grid_alpha=0.15,
        apply_to_all=True
    )

    (
        monthly_spending,
        spend_by_category,
        avg_per_month,
        transaction_count,
        max_expense
    ) = aggregations()

    # ----------------------------
    # Line Plot — Monthly Spending
    # ----------------------------

    months = monthly_spending["months"].dt.to_timestamp()  # type: ignore

    pe.draw(
        ax1,
        months,  # type: ignore
        monthly_spending.total_spending,
        color=pe.colors_vibrant[-2],
        linewidth=2.5,
        marker='o'
    )

    ax1.grid(
        True, alpha=0.15, color='#4ECDC4', linestyle='--', linewidth=0.8
    )

    pe.add_margins(ax1, ypad=0.25)
    pe.decorate(
        ax1,
        title="Monthly Expenditure Breakdown",
        xlabel="Months",
        ylabel="Amount Spent (₦)",
        ylim="zero",
    )

    pe.decorate
    pe.force_xticks(ax1, months, months)  # type: ignore
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    pe.format_y_axis(ax1, currency="₦")

    # ---------------------------------
    # Bar Chart — Categorical Spending
    # ---------------------------------
    pe.draw(
        ax2,
        spend_by_category.category,
        spend_by_category.total_spending,
        plot_type="bar",
        label=spend_by_category.category,
        color=SET_COLOR
    )

    pe.add_margins(ax2, ypad=0.4)
    pe.decorate(
        ax2,
        title="Categorical Expenditure",
        xlabel="Category",
        ylabel="Amount Spent (₦)"
    )

    pe.add_value_labels_on_bars(
        ax2, format_string="₦{:,.2f}", fontsize=8, color="white"
    )
    pe.format_y_axis(ax2, currency="₦")
    pe.set_legend(
        ax2,
        loc="upper right",
        fontsize=10,
        title="Categories",
        title_fontproperties={"weight": "bold", "size": 12}
    )

    # ---------------------------
    # Pie Chart — Category Share
    # ---------------------------

    spendings = spend_by_category.total_spending
    percentages = (spendings / spendings.sum()) * 100

    legend_labels = [
        f"{category} — {pct:.1f}%"
        for category, pct in zip(spend_by_category.category, percentages)
    ]

    pe.draw(
        ax3,
        None,
        spendings,
        plot_type="pie",
        colors=SET_COLOR,
        startangle=90,
    )

    ax3.set(aspect="equal")

    ax3.legend(
        legend_labels,
        loc="upper right",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=11,
        frameon=True,
        fancybox=True
    )

    pe.decorate(ax3, title="Category Share (%)")

    # -----------------
    # Stats Summary Box
    # -----------------

    stats = {
        "Total Spent": f"₦{spendings.sum():,}",
        "Avg Per Month": f"₦{avg_per_month:,}",
        "Total Debit Transactions": f"{transaction_count}",
        "Biggest Expense": f"₦{max_expense:,.2f}",
    }

    pe.create_stats_text_box(
        ax4,
        stats,
        title="SUMMARY",
        fontsize=13
    )

    # -----------
    # Saving plot
    # -----------

    pe.save_or_show(
        fig, save_path=SAVE_PATH, show=False, use_tight_layout=False
    )
    logger.info("Data visualized and saved to " + SAVE_PATH)


if __name__ == "__main__":
    try:
        visualize_data()
    except KeyboardInterrupt:
        logger.info("\n\nInterrupted by user")
        sys.exit(0)
