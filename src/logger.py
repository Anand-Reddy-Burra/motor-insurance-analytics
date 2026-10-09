
import logging
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "pipeline.log"


def get_logger(name="motor_insurance"):
    """Create and return a configured project logger."""

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Write logs to a file
        file_handler = logging.FileHandler(
            LOG_FILE, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        # Display logs in the terminal
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    logger = get_logger()

    logger.info("Logging system initialized successfully.")
    logger.warning("This is a sample warning message.")
    logger.error("This is a sample error message.")

    print(f"\nLog file location: {LOG_FILE}")
