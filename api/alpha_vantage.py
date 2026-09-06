import time

import requests

from config import API_KEY, API_URL, SYMBOL
from utils.logger import setup_logger


logger = setup_logger()


def fetch_stock_data():

    if not API_KEY:
        raise RuntimeError(
            "ALPHA_VANTAGE_API_KEY is not configured"
        )

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": SYMBOL,
        "outputsize": "compact",
        "apikey": API_KEY
    }

    max_retries = 3

    for attempt in range(1, max_retries + 1):

        try:

            logger.info(
                f"Requesting Alpha Vantage API - attempt {attempt}"
            )

            response = requests.get(
                API_URL,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            if "Error Message" in data:
                raise RuntimeError(
                    data["Error Message"]
                )

            if "Note" in data:
                raise RuntimeError(
                    data["Note"]
                )

            time_series = data.get(
                "Time Series (Daily)"
            )

            if not time_series:
                raise RuntimeError(
                    "No time-series data found in API response"
                )

            logger.info(
                "API data fetched successfully"
            )

            return time_series

        except requests.exceptions.Timeout:

            logger.error(
                f"API timeout - attempt {attempt}"
            )

        except requests.exceptions.RequestException as e:

            logger.error(
                f"API request failed - attempt {attempt}: {e}"
            )

        except RuntimeError as e:

            logger.error(
                f"API data error - attempt {attempt}: {e}"
            )

        if attempt < max_retries:

            wait_time = 2 ** (attempt - 1)

            logger.info(
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)

    raise RuntimeError(
        "API request failed after all retry attempts"
    )
