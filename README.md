# Fintual Portfolio Management System

## Candidacy for Software Engineer [Fondos Mutuos] Position

- **Candidate:** Felipe Silva
- **Email:** felipe.silva@biomedica.udec.cl
- **Position:** Software Engineer [Fondos Mutuos]
- **Location:** América Latina
- **Application Date:** May 28, 2025

This project was created as part of the Fintual job application process, demonstrating my approach to building a professional portfolio management system that helps track and rebalance stock allocations.

## Project Overview

This project implements a portfolio management system that allows users to:
- Track multiple stocks with their price history
- Set target allocations for each stock
- Monitor current portfolio value and allocations
- Calculate rebalancing actions to maintain target allocations
- Visualize current vs target allocations

## Beyond Basic Requirements

While the original task asked for a simple Portfolio class with basic rebalancing functionality, I've extended the implementation with several professional features:

### Enhanced Stock Management
- **Price History**: Instead of just current prices, implemented a full price history system with date-based lookups
- **Data Validation**: Added input validation for prices, allocations, and positions
- **Error Handling**: Comprehensive error handling with descriptive messages

### Advanced Portfolio Features
- **Position Tracking**: Added support for tracking actual share positions
- **Value Calculation**: Implemented total portfolio value calculation
- **Allocation Monitoring**: Real-time monitoring of current allocations vs targets
- **Tolerance Settings**: Configurable tolerance levels for rebalancing to avoid unnecessary trades

### Professional Development Practices
- **Type Hints**: Full type annotation support for better code maintainability
- **Documentation**: Comprehensive docstrings and README
- **Testing**: High test coverage with pytest
- **Code Quality**: Integration with Black, Ruff, and other code quality tools
- **CI/CD**: GitHub Actions workflow for automated testing and quality checks

### Visualization
- **Interactive Charts**: Added matplotlib-based visualization of allocations
- **Comparison Views**: Side-by-side comparison of current vs target allocations

## Features

- **Stock Management**
  - Track stock prices over time
  - Get current and historical prices
  - Support for multiple stocks

- **Portfolio Management**
  - Set target allocations
  - Track current positions
  - Calculate portfolio value
  - Monitor current allocations

- **Rebalancing**
  - Calculate required trades to reach target allocations
  - Support for both buying and selling
  - Configurable tolerance for small adjustments

- **Visualization**
  - Compare current vs target allocations
  - Interactive pie charts
  - Clear visual feedback

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/felipe-silva-v/fintual-portfolio.git
   cd fintual-portfolio
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

## Usage

Here's a basic example of how to use the portfolio management system:

```python
from datetime import datetime
from portfolio import Portfolio, Stock

# Create stocks
aapl = Stock("AAPL", "Apple Inc.")
msft = Stock("MSFT", "Microsoft Corporation")

# Add price history
aapl.add_price(datetime(2024, 1, 1), 150.0)
aapl.add_price(datetime(2024, 1, 2), 152.0)
msft.add_price(datetime(2024, 1, 1), 300.0)
msft.add_price(datetime(2024, 1, 2), 298.0)

# Create portfolio
portfolio = Portfolio()
portfolio.add_stock(aapl)
portfolio.add_stock(msft)

# Set target allocations
portfolio.set_allocation("AAPL", 60.0)
portfolio.set_allocation("MSFT", 40.0)

# Set current positions
portfolio.set_position("AAPL", 10.0)
portfolio.set_position("MSFT", 5.0)

# Print current state
print("\nCurrent Portfolio State:")
print(f"Total Value: ${portfolio.get_current_value():,.2f}")
print("\nCurrent Allocations:")
for ticker, alloc in portfolio.get_current_allocation().items():
    print(f"{ticker}: {alloc:.1f}%")

# Calculate and print rebalancing actions
print("\nRebalancing Actions:")
actions = portfolio.rebalance()
for action in actions:
    print(
        f"{action.action} {action.shares:.2f} shares of {action.ticker} "
        f"(${action.value:,.2f})"
    )

# Show allocation comparison plot
portfolio.plot_allocation_comparison()
```

## Tolerance Settings

The portfolio management system uses two tolerance values to control rebalancing behavior:

### Allocation Tolerance (1%)
- **Purpose**: Validates that target allocations sum to 100%
- **Default Value**: 0.01 (1%)
- **Usage**: When setting target allocations, the system ensures that the sum of all allocations is within 1% of 100%
- **Example**: If you set allocations to 60% and 40%, the system will accept this as valid. If you set 60% and 41%, it will raise an error

### Share Tolerance (1%)
- **Purpose**: Determines when a position needs rebalancing
- **Default Value**: 0.01 (1%)
- **Usage**: When calculating rebalancing actions, the system only suggests trades if the current position differs from the target by more than 1%
- **Example**: If you have 100 shares and the target is 102 shares, no rebalancing action will be suggested

### Adjusting Tolerance Values

To modify these tolerance values, you can update the constants in `src/portfolio/portfolio.py`:

```python
# Constants
MAX_ALLOCATION = 100.0
ALLOCATION_TOLERANCE = 0.01  # Adjust this value to change allocation validation tolerance
SHARE_TOLERANCE = 0.01      # Adjust this value to change rebalancing sensitivity
```

Considerations when adjusting tolerances:
- Lower values (e.g., 0.005) will make the system more strict about allocations and trigger more rebalancing actions
- Higher values (e.g., 0.02) will make the system more lenient and reduce the frequency of rebalancing
- Values should be between 0 and 1 (representing percentages)
- Very small values (< 0.001) may lead to unnecessary rebalancing due to floating-point precision
- Very large values (> 0.05) may lead to significant deviations from target allocations

## Development

### Running Tests

```bash
pytest
```

### Code Quality

The project uses several tools to maintain code quality:

- **Black** for code formatting
- **Ruff** for linting
- **pytest** for testing
- **pytest-cov** for test coverage

Run all checks:
```bash
black .
ruff check .
pytest
```