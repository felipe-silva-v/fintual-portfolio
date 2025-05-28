"""Tests for the Portfolio class."""

from datetime import datetime

import pytest

from portfolio import Portfolio, Stock

# Test constants
AAPL_ALLOCATION = 60.0
MSFT_ALLOCATION = 40.0
AAPL_SHARES = 10.0
MSFT_SHARES = 5.0
AAPL_PRICE = 150.0
MSFT_PRICE = 300.0
TOTAL_VALUE = 3000.0
ALLOCATION_50 = 50.0
EXPECTED_ACTIONS = 2
AAPL_BUY_SHARES = 2.0


@pytest.fixture
def sample_portfolio():
    """Create a sample portfolio for testing."""
    portfolio = Portfolio()
    aapl = Stock("AAPL", "Apple Inc.")
    msft = Stock("MSFT", "Microsoft Corporation")

    # Add price history
    aapl.add_price(datetime(2024, 1, 1), AAPL_PRICE)
    msft.add_price(datetime(2024, 1, 1), MSFT_PRICE)

    portfolio.add_stock(aapl)
    portfolio.add_stock(msft)
    return portfolio


def test_portfolio_initialization():
    """Test portfolio initialization."""
    portfolio = Portfolio()
    assert len(portfolio.stocks) == 0
    assert len(portfolio.allocations) == 0
    assert len(portfolio.positions) == 0


def test_add_stock(sample_portfolio):
    """Test adding stocks to portfolio."""
    # Test adding new stock
    googl = Stock("GOOGL", "Alphabet Inc.")
    googl.add_price(datetime(2024, 1, 1), 100.0)
    sample_portfolio.add_stock(googl)

    assert "GOOGL" in sample_portfolio.stocks
    assert sample_portfolio.positions["GOOGL"] == 0.0

    # Test adding duplicate stock
    with pytest.raises(ValueError, match="Stock AAPL already exists in portfolio"):
        sample_portfolio.add_stock(Stock("AAPL", "Apple Inc."))


def test_set_allocation(sample_portfolio):
    """Test setting target allocations."""
    sample_portfolio.set_allocation("AAPL", AAPL_ALLOCATION)
    sample_portfolio.set_allocation("MSFT", MSFT_ALLOCATION)

    assert sample_portfolio.allocations["AAPL"] == AAPL_ALLOCATION
    assert sample_portfolio.allocations["MSFT"] == MSFT_ALLOCATION

    # Test invalid allocation
    with pytest.raises(ValueError):
        sample_portfolio.set_allocation("INVALID", 50.0)


def test_set_position(sample_portfolio):
    """Test setting positions."""
    sample_portfolio.set_position("AAPL", AAPL_SHARES)
    sample_portfolio.set_position("MSFT", MSFT_SHARES)

    assert sample_portfolio.positions["AAPL"] == AAPL_SHARES
    assert sample_portfolio.positions["MSFT"] == MSFT_SHARES

    # Test invalid position
    with pytest.raises(ValueError):
        sample_portfolio.set_position("INVALID", 10.0)


def test_get_current_value(sample_portfolio):
    """Test getting current portfolio value."""
    sample_portfolio.set_position("AAPL", AAPL_SHARES)
    sample_portfolio.set_position("MSFT", MSFT_SHARES)

    # Value = (10 * 150) + (5 * 300) = 3000
    assert sample_portfolio.get_current_value() == TOTAL_VALUE


def test_get_current_allocation(sample_portfolio):
    """Test getting current allocation percentages."""
    sample_portfolio.set_position("AAPL", AAPL_SHARES)
    sample_portfolio.set_position("MSFT", MSFT_SHARES)

    allocations = sample_portfolio.get_current_allocation()
    assert allocations["AAPL"] == ALLOCATION_50  # (10 * 150) / 3000 = 50%
    assert allocations["MSFT"] == ALLOCATION_50  # (5 * 300) / 3000 = 50%


def test_rebalance(sample_portfolio):
    """Test portfolio rebalancing."""
    sample_portfolio.set_position("AAPL", AAPL_SHARES)
    sample_portfolio.set_position("MSFT", MSFT_SHARES)
    sample_portfolio.set_allocation("AAPL", AAPL_ALLOCATION)
    sample_portfolio.set_allocation("MSFT", MSFT_ALLOCATION)

    actions = sample_portfolio.rebalance()

    # Verify actions
    assert len(actions) == EXPECTED_ACTIONS

    # AAPL should be bought (target: 60% of 3000 = 1800, current: 1500)
    aapl_action = next(a for a in actions if a.ticker == "AAPL")
    assert aapl_action.action == "BUY"
    assert aapl_action.shares == AAPL_BUY_SHARES  # (1800 - 1500) / 150 = 2

    # MSFT should be sold (target: 40% of 3000 = 1200, current: 1500)
    msft_action = next(a for a in actions if a.ticker == "MSFT")
    assert msft_action.action == "SELL"
    assert msft_action.shares == 1.0  # (1500 - 1200) / 300 = 1


def test_rebalance_validation(sample_portfolio):
    """Test rebalancing validation."""
    # Test without allocations
    with pytest.raises(ValueError, match="No target allocations set"):
        sample_portfolio.rebalance()

    # Test with invalid allocation sum
    sample_portfolio.set_allocation("AAPL", 60.0)
    sample_portfolio.set_allocation("MSFT", 50.0)

    with pytest.raises(ValueError, match="Allocations must sum to 100%"):
        sample_portfolio.rebalance()
