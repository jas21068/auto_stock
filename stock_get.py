import yfinance as yf
import time

# Function to fetch the current stock price
def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d", interval="1m")  # Fetches 1-minute interval data for the current day
    if data.empty:
        raise ValueError(f"No data found for ticker {ticker}")
    return data["Close"].iloc[-1]  # Get the latest closing price

def main():
    # Input ticker symbol from user
    ticker = input("Enter the stock ticker symbol (e.g., AAPL, TSLA, TD.TO): ").upper()
    initial_investment = float(input("Enter the investment amount ($): "))

    try:
        print(f"Fetching live data for {ticker}... Press Ctrl+C to stop.")

        # Initial setup
        current_price = get_stock_price(ticker)
        shares = initial_investment / current_price  # Mock purchase of shares
        initial_benchmark = current_price  # Initial benchmark for profit calculation
        total_benchmark = initial_investment  # Initial value for total profit calculation
        print(f"Bought {shares:.2f} shares at {current_price:.2f} per share.")

        while True:
            # Get the latest price
            new_price = get_stock_price(ticker)
            total_value = shares * new_price
            profit_loss_percentage = ((new_price - initial_benchmark) / initial_benchmark) * 100
            total_profit_loss_percentage = ((total_value - initial_investment) / initial_investment) * 100

            # Display the profit/loss status
            print(f"Current Price: {new_price:.2f} | Total Value: {total_value:.2f} | "
                  f"Profit/Loss (Benchmark): {profit_loss_percentage:.2f}% | "
                  f"Total Profit/Loss: {total_profit_loss_percentage:.2f}%")

            # Logic for selling and updating benchmark
            if total_profit_loss_percentage <= -1:  # Total loss of 1%
                print("Price dropped by 1% from the last benchmark. Selling all shares.")
                break
            elif profit_loss_percentage <= -1:  # Loss of 1% on benchmark
                print("Price dropped by 1% from the benchmark. Selling all shares.")
                break
            elif profit_loss_percentage >= 2:  # Gain of 2% on benchmark
                print("Price increased by 2%. Setting a new benchmark.")
                initial_benchmark = new_price  # Update benchmark
            elif total_profit_loss_percentage >= 7:  # Total gain of 7%
                print("Total profit reached 7%. Selling all shares.")
                break

            # Wait for a short interval before checking again
            time.sleep(1)  # Check every second

    except KeyboardInterrupt:
        print("\nExiting the program.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
