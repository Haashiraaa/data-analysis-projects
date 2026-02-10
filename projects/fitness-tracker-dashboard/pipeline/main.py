

# main.py


"""Fitness Tracker Dashboard - Main entry point."""

import sys
import logging
from haashi_pkg.utility import Logger
from visualize_data import visualize_data


def parse_args() -> int:
    """Parse command line args for logging level."""
    if len(sys.argv) > 1:
        if "-d" in sys.argv or "--debug" in sys.argv:
            return logging.DEBUG
    return logging.INFO


def main() -> None:
    """Run the fitness tracker dashboard generator."""
    log_level = parse_args()
    logger = Logger(level=log_level)

    logger.info("=" * 60)
    logger.info("Fitness Tracker Dashboard Generator")
    logger.info("=" * 60)

    try:
        logger.info("\nCreating fitness tracker dashboard...")
        visualize_data(logger=logger)
        logger.info("✓ Dashboard created successfully")

        logger.info("\n" + "=" * 60)
        logger.info("Dashboard ready!")
        logger.info("=" * 60)
        logger.info("Output:")
        logger.info("  • Dashboard: data/plots/fitness_tracker_dashboard.png")

    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user")
        sys.exit(0)

    except Exception as e:
        logger.error("\n" + "=" * 60)
        logger.error("Dashboard generation failed:")
        logger.error("=" * 60)
        logger.error(exception=e, save_to_json=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
