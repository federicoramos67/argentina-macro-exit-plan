import argparse
import logging

from src.main import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Argentina Macro Exit Plan — Analysis Runner")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    main()
