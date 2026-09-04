import os
import time
import logging

import requests
import pandas as pd
from dotenv import load_dotenv


# -----------------------------
# Configuration
# -----------------------------

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
API_URL = "https://www.alphavantage.co/query"

SYMBOL = "IBM"
OUTPUT_FILE = "data/stock_data.csv"


# -----------------------------
# Logging Configuration
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# -----------------------------
# Fetch data from API
# -----------------------------

def fetch_stock_data():
    if not API_KEY:
        raise ValueError("ALPHA_VANTAGE_API_KEY is not configured")

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": SYMBOL,
        "outputsize": "compact",
        "apikey": API_KEY
    }

    for attempt in range(1, 4):
        try:
            logger.info(
                "Requesting Alpha Vantage API - attempt %s",
                attempt
            )

            response = requests.get(
                API_URL,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            if "Error Message" in data:
                raise ValueError(data["Error Message"])

            if "Note" in data:
                raise RuntimeError(
                    f"Alpha Vantage API notice: {data['Note']}"
                )

            if "Time Series (Daily)" not in data:
                raise ValueError(
                    "Time Series (Daily) not found in API response"
                )

            logger.info("API data fetched successfully")

            return data["Time Series (Daily)"]

        except requests.exceptions.Timeout:
            logger.warning("Request timed out")

        except requests.exceptions.RequestException as error:
            logger.warning("Network/API error: %s", error)

        except (ValueError, RuntimeError):
            raise

        if attempt < 3:
            logger.info("Retrying in 5 seconds...")
            time.sleep(5)

    raise RuntimeError("API request failed after 3 attempts")


# -----------------------------
# Transform JSON → records
# -----------------------------

def transform_data(time_series):
    records = []

    for date, values in time_series.items():

        record = {
            "date": date,
            "open": values["1. open"],
            "high": values["2. high"],
            "low": values["3. low"],
            "close": values["4. close"],
            "volume": values["5. volume"]
        }

        records.append(record)

    logger.info("Transformed %s records", len(records))

    return records


# -----------------------------
# Save data as CSV
# -----------------------------

def save_to_csv(records):
    df = pd.DataFrame(records)

    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df["date"] = pd.to_datetime(df["date"])

    os.makedirs("data", exist_ok=True)

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    logger.info("CSV saved successfully: %s", OUTPUT_FILE)
    logger.info("Total records: %s", len(df))

    return df


# -----------------------------
# Main application
# -----------------------------

def main():
    logger.info("Starting Alpha Vantage pipeline")

    try:
        time_series = fetch_stock_data()

        records = transform_data(time_series)

        df = save_to_csv(records)

        print("\nFirst 5 records:")
        print(df.head())

        logger.info("Pipeline completed successfully")

    except Exception as error:
        logger.error("Pipeline failed: %s", error)
        raise


# -----------------------------
# Entry point
# -----------------------------

if __name__ == "__main__":
    main()