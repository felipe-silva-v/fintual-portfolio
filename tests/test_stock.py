"""Tests for the Stock class."""

from datetime import datetime

import pytest

from portfolio import Stock

# Test constants
AAPL_PRICE_1 = 151.0
AAPL_PRICE_2 = 152.0


@pytest.fixture
def stock():
    """Create a sample stock for testing."""
    return Stock("AAPL", "Apple Inc.")


@pytest.fixture
def stock_with_prices():
    """Create a stock with price history for testing."""
    stock = Stock("AAPL", "Apple Inc.")
    stock.add_price(datetime(2024, 1, 1), AAPL_PRICE_1)
    stock.add_price(datetime(2024, 1, 2), AAPL_PRICE_2)
    return stock


def test_stock_initialization(stock):
    """Test stock initialization."""
    assert stock.ticker == "AAPL"
    assert stock.name == "Apple Inc."
    assert stock.price_history == {}


def test_add_price(stock):
    """Test adding price history."""
    date = datetime(2024, 1, 1)
    stock.add_price(date, AAPL_PRICE_1)
    assert len(stock.price_history) == 1
    assert stock.price_history[date].price == AAPL_PRICE_1


def test_current_price(stock_with_prices):
    """Test getting current price at different dates."""
    # Test latest price
    assert stock_with_prices.current_price() == AAPL_PRICE_2

    # Test specific date
    assert stock_with_prices.current_price(datetime(2024, 1, 2)) == AAPL_PRICE_2

    # Test date before any prices
    with pytest.raises(ValueError):
        stock_with_prices.current_price(datetime(2023, 12, 31))
