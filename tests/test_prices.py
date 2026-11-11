
"""
test_prices.py

Automated tests for EnergiInsight's electricity price calculations.

These tests verify that the conversion from DKK/MWh to DKK/kWh
produces the expected results.
"""

import pytest

from scripts.fetch_prices import convert_price


@pytest.mark.parametrize(
    "price_dkk_mwh, expected_dkk_kwh",
    [
        (1000, 1.0),
        (500, 0.5),
        (0, 0.0),
        (-100, -0.1),
        (904.75, 0.90475),
    ],
)
def test_convert_price(price_dkk_mwh, expected_dkk_kwh):
    """
    Verify that electricity prices are converted correctly.

    Args:
        price_dkk_mwh (float): Original electricity price in DKK/MWh.
        expected_dkk_kwh (float): Expected converted price in DKK/kWh.
    """

    # Call the conversion function with the test input.
    result = convert_price(price_dkk_mwh)

    # Compare the result with the expected value.
    # pytest.approx handles small floating-point rounding differences.
    assert result == pytest.approx(expected_dkk_kwh)
