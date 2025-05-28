"""Portfolio class for managing a collection of stocks and their allocations."""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import matplotlib.pyplot as plt

from .stock import Stock

logger = logging.getLogger(__name__)

# Constants
MAX_ALLOCATION = 100.0
ALLOCATION_TOLERANCE = 0.01
SHARE_TOLERANCE = 0.01


@dataclass
class RebalanceAction:
    """Represents a rebalancing action for a stock."""

    ticker: str
    action: str  # "BUY" or "SELL"
    shares: float
    value: float


class Portfolio:
    """A portfolio of stocks with target allocations and positions.

    Attributes:
        stocks (dict[str, Stock]): Dictionary mapping tickers to Stock objects.
        allocations (dict[str, float]): Dictionary mapping tickers to target allocations.
        positions (dict[str, float]): Dictionary mapping tickers to number of shares.
    """

    def __init__(self):
        """Initialize an empty Portfolio instance."""
        self.stocks: dict[str, Stock] = {}
        self.allocations: dict[str, float] = {}
        self.positions: dict[str, float] = {}
        logger.info("Initialized new Portfolio")

    def add_stock(self, stock: Stock) -> None:
        """Add a stock to the portfolio.

        Args:
            stock: The Stock object to add.

        Raises:
            ValueError: If stock with same ticker already exists.
        """
        if stock.ticker in self.stocks:
            raise ValueError(f"Stock {stock.ticker} already exists in portfolio")

        self.stocks[stock.ticker] = stock
        self.positions[stock.ticker] = 0.0
        logger.info(f"Added stock {stock.ticker} to portfolio")

    def set_allocation(self, ticker: str, percentage: float) -> None:
        """Set the target allocation percentage for a stock.

        Args:
            ticker: The stock ticker symbol.
            percentage: Target allocation percentage (0-100).

        Raises:
            ValueError: If stock not found or percentage is invalid.
        """
        if ticker not in self.stocks:
            raise ValueError(f"Stock {ticker} not found in portfolio")

        if not 0 <= percentage <= MAX_ALLOCATION:
            raise ValueError("Allocation percentage must be between 0 and 100")

        self.allocations[ticker] = percentage
        logger.info(f"Set allocation for {ticker} to {percentage}%")

    def set_position(self, ticker: str, shares: float) -> None:
        """Set the number of shares for a stock.

        Args:
            ticker: The stock's ticker symbol.
            shares: The number of shares to hold.

        Raises:
            ValueError: If ticker doesn't exist or shares is negative.
        """
        if ticker not in self.stocks:
            raise ValueError(f"Stock {ticker} not found in portfolio")

        if shares < 0:
            raise ValueError("Number of shares cannot be negative")

        self.positions[ticker] = shares
        logger.info(f"Set position for {ticker} to {shares} shares")

    def get_current_value(self, date: Optional[datetime] = None) -> float:
        """Calculate the total current value of the portfolio.

        Args:
            date: The date to calculate value for. If None, uses latest prices.

        Returns:
            float: The total portfolio value.
        """
        total_value = 0.0
        for ticker, shares in self.positions.items():
            price = self.stocks[ticker].current_price(date)
            total_value += shares * price
        return total_value

    def get_current_allocation(
        self, date: Optional[datetime] = None
    ) -> dict[str, float]:
        """Calculate the current allocation percentages.

        Args:
            date: Optional date to calculate allocations at. Defaults to latest.

        Returns:
            dict[str, float]: Dictionary mapping tickers to current allocation percentages.
        """
        total_value = self.get_current_value(date)
        if total_value == 0:
            return {ticker: 0.0 for ticker in self.stocks}

        allocations = {}
        for ticker, stock in self.stocks.items():
            if ticker in self.positions:
                current_price = stock.current_price(date)
                shares = self.positions[ticker]
                value = shares * current_price
                allocations[ticker] = (value / total_value) * 100

        return allocations

    def rebalance(self, date: Optional[datetime] = None) -> list[RebalanceAction]:
        """Calculate rebalancing actions needed to reach target allocations.

        Args:
            date: Optional date to calculate rebalancing at. Defaults to latest.

        Returns:
            list[RebalanceAction]: List of actions needed to rebalance.

        Raises:
            ValueError: If no target allocations are set or they don't sum to 100%.
        """
        if not self.allocations:
            raise ValueError("No target allocations set")

        if abs(sum(self.allocations.values()) - MAX_ALLOCATION) > ALLOCATION_TOLERANCE:
            raise ValueError("Allocations must sum to 100%")

        current_value = self.get_current_value(date)
        actions = []

        for ticker, target_alloc in self.allocations.items():
            current_price = self.stocks[ticker].current_price(date)
            target_value = (target_alloc / MAX_ALLOCATION) * current_value
            current_shares = self.positions[ticker]
            target_shares = target_value / current_price

            if abs(target_shares - current_shares) > SHARE_TOLERANCE:
                shares_diff = target_shares - current_shares
                action = "BUY" if shares_diff > 0 else "SELL"
                actions.append(
                    RebalanceAction(
                        ticker=ticker,
                        action=action,
                        shares=abs(shares_diff),
                        value=abs(shares_diff) * current_price,
                    )
                )

        return actions

    def plot_allocation_comparison(self, date: Optional[datetime] = None) -> None:
        """Create a pie chart comparing current vs target allocations.

        Args:
            date: The date to plot allocations for. If None, uses latest prices.
        """
        current_alloc = self.get_current_allocation(date)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # Current allocation
        ax1.pie(current_alloc.values(), labels=current_alloc.keys(), autopct="%1.1f%%")
        ax1.set_title("Current Allocation")

        # Target allocation
        ax2.pie(
            self.allocations.values(), labels=self.allocations.keys(), autopct="%1.1f%%"
        )
        ax2.set_title("Target Allocation")

        plt.tight_layout()
        plt.show()
