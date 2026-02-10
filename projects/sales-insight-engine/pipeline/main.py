

# main.py


"""Retail Sales Analysis Pipeline - Main entry point."""

import sys
import logging
from haashi_pkg.utility import Logger
from clean_data import clean_data
from visualize_data import visualize_data


def parse_args() -> int:
    """Parse command line args for logging level."""
    if len(sys.argv) > 1:
        if "-d" in sys.argv or "--debug" in sys.argv:
            return logging.DEBUG
    return logging.INFO


def main() -> None:
    """Run the retail sales analysis pipeline."""
    log_level = parse_args()
    logger = Logger(level=log_level)

    logger.info("=" * 60)
    logger.info("Retail Sales Analysis Pipeline")
    logger.info("=" * 60)

    try:
        # Step 1: Clean data
        logger.info("\n[Step 1/2] Cleaning retail sales data...")
        clean_data(logger=logger)
        logger.info("✓ Data cleaning completed")

        # Step 2: Visualize
        logger.info("\n[Step 2/2] Creating visualization dashboard...")
        visualize_data(logger=logger)
        logger.info("✓ Visualization completed")

        # Success
        logger.info("\n" + "=" * 60)
        logger.info("Pipeline completed successfully!")
        logger.info("=" * 60)
        logger.info("Outputs:")
        logger.info("  • Cleaned data: data/cleaned_retail_sales.parquet")
        logger.info("  • Dashboard: data/plots/retail_sales_plots.png")

    except KeyboardInterrupt:
        logger.info("\nPipeline interrupted by user")
        sys.exit(0)

    except Exception as e:
        logger.error("\n" + "=" * 60)
        logger.error("Pipeline failed:")
        logger.error("=" * 60)
        logger.error(exception=e, save_to_json=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
