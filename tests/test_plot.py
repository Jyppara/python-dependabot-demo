"""Tests for datatoolsdemo.plot module.

The goal is to ensure that the plotting function behaves correctly
without actually opening a GUI window during tests.
"""

import pandas as pd
import pytest

from datatoolsdemo.plot import plot_column


def test_plot_column_raises_for_missing_column() -> None:
    """
    Verify that plot_column raises ValueError when the requested column
    does not exist in the dataframe.
    """

    df = pd.DataFrame({"a": [1, 2, 3]})

    with pytest.raises(ValueError):
        plot_column(df, "nonexistent")


def test_plot_column_calls_show(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Verify that plot_column completes successfully for a valid column.

    We monkeypatch matplotlib.pyplot.show to avoid actually opening
    a figure window and to ensure the function is called.
    """

    called = {"show": False}

    def fake_show() -> None:
        """Fake replacement for plt.show that only records the call."""
        called["show"] = True

    # Patch the show function inside the datatoolsdemo.plot module
    monkeypatch.setattr("datatoolsdemo.plot.plt.show", fake_show)

    df = pd.DataFrame({"a": [1, 2, 3]})
    plot_column(df, "a")

    assert called["show"] is True
