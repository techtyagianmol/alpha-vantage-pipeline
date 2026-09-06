from unittest.mock import patch
from transform.csv_converter import transform_to_csv
from api.alpha_vantage import fetch_stock_data
from storage.s3_uploader import upload_to_s3

def test_api_returns_data():

    mock_response = {
        "Time Series (Daily)": {
            "2026-09-05": {
                "1. open": "100.00",
                "2. high": "105.00",
                "3. low": "99.00",
                "4. close": "103.00",
                "5. volume": "1000000"
            }
        }
    }

    with patch("api.alpha_vantage.requests.get") as mock_get:

        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status.return_value = None

        data = fetch_stock_data()

        assert data is not None
        assert len(data) == 1
        assert "2026-09-05" in data

        mock_get.assert_called_once()

def test_json_to_csv(tmp_path):

    mock_data = {
        "2026-09-05": {
            "1. open": "100.00",
            "2. high": "105.00",
            "3. low": "99.00",
            "4. close": "103.00",
            "5. volume": "1000000"
        }
    }

    output_file = tmp_path / "stock_data.csv"

    with patch("transform.csv_converter.OUTPUT_FILE", str(output_file)):

        df = transform_to_csv(mock_data)

    assert output_file.exists()
    assert len(df) == 1

    expected_columns = [
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    assert list(df.columns) == expected_columns

def test_s3_upload():

    with patch("storage.s3_uploader.boto3.client") as mock_boto3:

        mock_s3 = mock_boto3.return_value

        upload_to_s3()

        mock_s3.upload_file.assert_called_once()
