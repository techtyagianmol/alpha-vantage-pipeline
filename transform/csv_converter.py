import os

import pandas as pd

from config import OUTPUT_FILE
from utils.logger import setup_logger


logger = setup_logger()


def transform_to_csv(time_series):

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

    df = df.sort_values(
        by="date",
        ascending=False
    )

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    logger.info(
        f"CSV saved successfully: {OUTPUT_FILE}"
    )

    logger.info(
        f"Total records: {len(df)}"
    )

    logger.info(
        f"\nFirst 5 records:\n{df.head()}"
    )

    return df
