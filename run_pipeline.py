
import sys

from src.data_loader import load_data
from src.validation import validate_data
from src.data_cleaner import clean_all_data
from src.insurance_analysis import analyze_insurance
from src.visualization import create_visualizations
from src.insights import generate_insights, save_insights
from src.logger import get_logger


def main():
    logger = get_logger()

    try:
        logger.info("Motor Insurance Analytics pipeline started.")

        # 1. Load raw data
        logger.info("Loading raw insurance datasets...")
        raw_data = load_data()

        # 2. Validate raw data
        logger.info("Validating datasets...")
        if not validate_data(raw_data):
            logger.error("Validation found data quality issues.")
            sys.exit(1)

        # 3. Clean data
        logger.info("Cleaning datasets...")
        clean_data = clean_all_data(raw_data)

        # 4. Analyze cleaned data
        logger.info("Analyzing insurance metrics...")
        metrics = analyze_insurance(clean_data)

        for metric, value in metrics.items():
            logger.info("%s: %s", metric, value)

        # 5. Generate business insights
        logger.info("Generating business insights...")
        insights = generate_insights(clean_data)
        save_insights(insights)

        # 6. Create visualizations
        logger.info("Creating charts...")
        create_visualizations()

        logger.info("Pipeline completed successfully.")

    except Exception:
        logger.exception("Pipeline failed.")
        raise


if __name__ == "__main__":
    main()
