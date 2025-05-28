"""Example usage of the Fintual portfolio management system."""

from datetime import datetime

from portfolio import Portfolio, Stock


def main():
    """Run the example portfolio management scenario."""
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
    print("\nGenerating allocation comparison plot...")
    portfolio.plot_allocation_comparison()


if __name__ == "__main__":
    main()
