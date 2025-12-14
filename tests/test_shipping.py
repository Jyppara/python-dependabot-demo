"""Test shipping functions boundary values with parametrized tests.

With parametrized test we can use the same testcase with various test inputs
based on the boundary-value analysis. This increases the code reusability and
makes it easier to design better code coverage.
"""

from typing import Any

import pytest

from datatoolsdemo import shipping_price_eur


# Listing valid weights and their expected results
@pytest.mark.parametrize(
    ("valid_weight_kg", "expected_eur"),
    [
        # Basic within-tier examples
        (0.1, 5),
        (2.0, 8),
        (7.5, 12),
        (15.0, 20),
        (25.0, 30),
        # Boundary values (upper bound inclusive)
        (1.0, 5),
        (5.0, 8),
        (10.0, 12),
        (20.0, 20),
        (30.0, 30),
        # Just over boundaries (moves to next tier)
        (1.000001, 8),
        (5.000001, 12),
        (10.000001, 20),
        (20.000001, 30),
    ],
)
def test_shipping_price_eur_boundaries(
    valid_weight_kg: float,
    expected_eur: int,
) -> None:
    """Test function with valid input values."""
    assert shipping_price_eur(valid_weight_kg) == expected_eur


# Listing invalid weights that result into a ValueError
@pytest.mark.parametrize(
    "invalid_weight_kg",
    [
        0.0,
        -0.1,
        30.000001,
        float("inf"),
        float("-inf"),
    ],
)
def test_shipping_price_eur_invalid_values(invalid_weight_kg: float) -> None:
    """Test function with invalid values."""
    with pytest.raises(ValueError):
        shipping_price_eur(invalid_weight_kg)


@pytest.mark.parametrize(
    "invalid_weight_kg",
    [
        "1.0",
        None,
        object(),
    ],
)
def test_shipping_price_eur_invalid_types(invalid_weight_kg: Any) -> None:
    """Test function with invalid types."""
    with pytest.raises(TypeError):
        shipping_price_eur(invalid_weight_kg)
