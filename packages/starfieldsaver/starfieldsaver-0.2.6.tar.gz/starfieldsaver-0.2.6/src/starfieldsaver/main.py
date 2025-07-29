"""A utility to automatically quicksave in Starfield on a specified interval."""

from __future__ import annotations

from polykit.core import polykit_setup
from polykit.log import PolyLog

from starfieldsaver.quicksaver import StarfieldQuicksaver

polykit_setup()

logger = PolyLog.get_logger("starfieldsaver")


def main():
    """Main function to run the quicksave utility."""
    try:
        StarfieldQuicksaver().run()
    except Exception as e:
        logger.error("An error occurred while running the application: %s", str(e))


if __name__ == "__main__":
    main()
