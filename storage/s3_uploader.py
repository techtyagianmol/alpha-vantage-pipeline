import boto3

from config import OUTPUT_FILE, S3_BUCKET, S3_KEY
from utils.logger import setup_logger


logger = setup_logger()


def upload_to_s3():

    logger.info("Uploading CSV to S3")

    s3 = boto3.client("s3")

    s3.upload_file(
        OUTPUT_FILE,
        S3_BUCKET,
        S3_KEY
    )

    logger.info(
        f"CSV uploaded successfully to "
        f"s3://{S3_BUCKET}/{S3_KEY}"
    )
