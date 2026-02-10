

# main.py

"""
Bank Statement Analysis Pipeline

Main entry point for the bank statement analysis workflow. Orchestrates
data generation, cleaning, analysis, and visualization.

The pipeline consists of:
1. Generate sample bank statement data (optional, for testing)
2. Clean and transform raw data
3. Visualize results in comprehensive dashboard

Usage:
    python main.py              # Run with INFO logging
    python main.py -d           # Run with DEBUG logging
    python main.py --debug      # Run with DEBUG logging
"""

import sys
import logging

from haashi_pkg.utility import Logger
from clean_data import clean_data
from sample_data_generator import generate_sample_bank_statement
from visualize_data import visualize_data


def parse_args() -> int:
    """
    Parse command line arguments for logging level.

    Returns:
        logging level (logging.INFO or logging.DEBUG)
    """
    if len(sys.argv) > 1:
        if "-d" in sys.argv or "--debug" in sys.argv:
            return logging.DEBUG
    return logging.INFO


def main() -> None:
    """
    Run the complete bank statement analysis pipeline.

    Steps:
        1. Generate sample bank statement data
        2. Clean and transform the data
        3. Create visualization dashboard

    All steps use the same logger instance for consistent logging.

    Raises:
        SystemExit: Exit code 0 on success, 1 on error
    """
    # Initialize logger based on command line args
    log_level = parse_args()
    logger = Logger(level=log_level)

    logger.info("=" * 60)
    logger.info("Bank Statement Analysis Pipeline")
    logger.info("=" * 60)

    try:
        # Step 1: Generate sample data
        logger.info("\n[Step 1/3] Generating sample bank statement data...")
        generate_sample_bank_statement(logger=logger)
        logger.info("✓ Sample data generation completed")

        # Step 2: Clean data
        logger.info("\n[Step 2/3] Cleaning bank statement data...")
        clean_data(logger=logger)
        logger.info("✓ Data cleaning completed")

        # Step 3: Visualize results
        logger.info("\n[Step 3/3] Creating visualization dashboard...")
        visualize_data(logger=logger)
        logger.info("✓ Visualization completed")

        # Success summary
        logger.info("\n" + "=" * 60)
        logger.info("Pipeline completed successfully!")
        logger.info("=" * 60)
        logger.info("Outputs:")
        logger.info(
            "  • Cleaned data: data/cleaned_bank_statement_2025.parquet")
        logger.info("  • Dashboard: data/plots/bank_statement_2025.png")

    except KeyboardInterrupt:
        logger.info("\n\nPipeline interrupted by user")
        logger.info("Exiting gracefully...")
        sys.exit(0)

    except Exception as e:
        logger.error("\n" + "=" * 60)
        logger.error("Pipeline failed with error:")
        logger.error("=" * 60)
        logger.error(exception=e, save_to_json=True)
        logger.error("\nError details saved to logs/errors.json")
        sys.exit(1)


if __name__ == "__main__":
    main()
