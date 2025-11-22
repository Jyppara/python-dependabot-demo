"""Tests for datatoolsdemo.clean module."""

import pandas as pd

from datatoolsdemo import normalize_dataframe


def test_normalize_dataframe_scales_numeric_columns_between_0_and_1() -> None:
    """Verify that numeric columns are scaled to the [0, 1] range."""
    df = pd.DataFrame(
        {
            "a": [0, 5, 10],
            "b": [10, 20, 30],
        }
    )

    normalized = normalize_dataframe(df)

    # All numeric values should be between 0 and 1
    assert (normalized["a"] >= 0).all()
    assert (normalized["a"] <= 1).all()
    assert (normalized["b"] >= 0).all()
    assert (normalized["b"] <= 1).all()

    # Check specific points to ensure the scaling is correct
    assert normalized["a"].iloc[0] == 0.0
    assert normalized["a"].iloc[-1] == 1.0
    assert normalized["b"].iloc[0] == 0.0
    assert normalized["b"].iloc[-1] == 1.0


def test_normalize_dataframe_preserves_non_numeric_columns() -> None:
    """
    Verify that non-numeric columns are preserved unchanged.
    """

    df = pd.DataFrame(
        {
            "value": [1, 2, 3],
            "label": ["x", "y", "z"],
        }
    )

    normalized = normalize_dataframe(df)

    # Non-numeric column should remain equal to original
    assert (normalized["label"] == df["label"]).all()

    # Numeric column still normalized
    assert normalized["value"].iloc[0] == 0.0
    assert normalized["value"].iloc[-1] == 1.0
