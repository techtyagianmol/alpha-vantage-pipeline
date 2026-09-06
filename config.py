import os

from dotenv import load_dotenv


load_dotenv()


# Alpha Vantage
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
API_URL = "https://www.alphavantage.co/query"
SYMBOL = "IBM"


# AWS S3
S3_BUCKET = "alpha-vantage-stock-data-2026-abc"
S3_KEY = "stock_data.csv"


# Local output
OUTPUT_FILE = "data/stock_data.csv"
