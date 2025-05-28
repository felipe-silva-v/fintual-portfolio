"""Stock class for managing individual stock data and price information."""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class PricePoint:
    """Represents a price point for a stock at a specific date."""

    date: datetime
    price: float


class Stock:
    """A class representing a stock with price history.

    Attributes:
        ticker (str): The stock's ticker symbol.
        name (str): The company name.
        price_history (dict[datetime, PricePoint]): Dictionary mapping dates to price points.
    """

    def __init__(self, ticker: str, name: str):
        """Initialize a new Stock instance.

        Args:
            ticker: The stock's ticker symbol.
            name: The company name.
        """
        self.ticker = ticker.upper()
        self.name = name
        self.price_history: dict[datetime, PricePoint] = {}
        logger.info(f"Initialized Stock: {self.ticker} ({self.name})")

    def add_price(self, date: datetime, price: float) -> None:
        """Add a price point to the stock's history.

        Args:
            date: The date of the price point.
            price: The price at the given date.

        Raises:
            ValueError: If price is negative or zero.
        """
        if price <= 0:
            raise ValueError("Price must be positive")

        self.price_history[date] = PricePoint(date=date, price=price)
        logger.debug(f"Added price point for {self.ticker}: {date} - ${price:.2f}")

    def current_price(self, date: Optional[datetime] = None) -> float:
        """Get the stock's price at a specific date or the latest available price.

        Args:
            date: The date to get the price for. If None, returns the latest price.

        Returns:
            float: The price at the specified date or latest available price.

        Raises:
            ValueError: If no price data is available.
        """
        if not self.price_history:
            raise ValueError(f"No price data available for {self.ticker}")

        if date is None:
            latest_date = max(self.price_history.keys())
            return self.price_history[latest_date].price

        # Find the closest date that's not after the requested date
        valid_dates = [d for d in self.price_history.keys() if d <= date]
        if not valid_dates:
            raise ValueError(f"No price data available for {self.ticker} before {date}")

        closest_date = max(valid_dates)
        return self.price_history[closest_date].price
