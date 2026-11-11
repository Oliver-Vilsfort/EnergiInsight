
"""
fetch_prices.py

Retrieves historical electricity spot prices from Energi Data Service,
converts the prices from DKK/MWh to DKK/kWh, and displays the results.

This script is an early prototype of EnergiInsight's data ingestion
and transformation functionality.
"""

import json

import requests


# Base endpoint for the electricity day-ahead price dataset.
API_URL = "https://api.energidataservice.dk/dataset/DayAheadPrices"


def fetch_prices(start_date, end_date):
    """
    Retrieve electricity prices for DK1 and DK2 within a date range.

    Args:
        start_date (str): Start date in YYYY-MM-DD format (inclusive).
        end_date (str): End date in YYYY-MM-DD format (exclusive).

    Returns:
        list[dict]: Electricity price records returned by the API.

    Raises:
        requests.HTTPError: If the API returns an unsuccessful status.
        requests.RequestException: If the request fails.
        ValueError: If the response contains no records.
    """

    # Define the query parameters for the API request.
    params = {
        "start": start_date,
        "end": end_date,
        "filter": json.dumps({"PriceArea": ["DK1", "DK2"]}),
        "limit": 500,
        "sort": "TimeUTC ASC"
    }

    # Send the HTTP request and check for errors.
    response = requests.get(API_URL, params=params, timeout=20)
    response.raise_for_status()

    # Parse the JSON response and extract the records.
    data = response.json()
    records = data["records"]

    # Stop execution if the API returned no electricity prices.
    if not records:
        raise ValueError("No electricity price records were returned.")

    return records


def convert_price(price_dkk_mwh):
    """
    Convert an electricity price from DKK/MWh to DKK/kWh.

    Args:
        price_dkk_mwh (float): Electricity price in DKK/MWh.

    Returns:
        float: Electricity price in DKK/kWh.
    """

    # One megawatt-hour equals 1000 kilowatt-hours.
    return price_dkk_mwh / 1000


def main():
    """
    Run the electricity price retrieval and conversion process.
    """

    # Define the date range to retrieve.
    start_date = "2026-11-01"
    end_date = "2026-11-02"

    # Retrieve the electricity price records.
    records = fetch_prices(start_date, end_date)

    print(f"Number of records: {len(records)}")

    # Convert and display the electricity prices.
    for record in records:
        price_dkk_kwh = convert_price(record["DayAheadPriceDKK"])

        print(
            f'{record["TimeDK"]} | '
            f'{record["PriceArea"]} | '
            f'{price_dkk_kwh:.3f} DKK/kWh'
        )


# Only execute main() when this file is run directly.
# This allows the functions to be imported into other Python files
# without automatically executing the entire script.
if __name__ == "__main__":
    main()
