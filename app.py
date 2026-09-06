from api.alpha_vantage import fetch_stock_data
from transform.csv_converter import transform_to_csv
from storage.s3_uploader import upload_to_s3
from utils.logger import setup_logger


logger = setup_logger()


def main():

    try:

        logger.info("Starting Alpha Vantage pipeline")

        # Step 1: Fetch data from API
        time_series = fetch_stock_data()

        # Step 2: Transform JSON → CSV
        transform_to_csv(time_series)

        # Step 3: Upload CSV → S3
        upload_to_s3()

        logger.info("Pipeline completed successfully")

    except Exception as e:

        logger.exception(
            f"Pipeline failed: {e}"
        )

        raise


if __name__ == "__main__":
    main()
