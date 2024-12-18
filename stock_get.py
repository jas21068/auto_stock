import yfinance as yf
import time

# Function to fetch the current stock price
def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d", interval="1m")  # Fetches 1-minute interval data for the current day
    return data["Close"].iloc[-1]  # Get the latest closing price

def main():
    # Input ticker symbol from user
    ticker = input("Enter the stock ticker symbol (e.g., AAPL, TSLA, TD.TO): ").upper()
    
    try:
        print(f"Fetching live data for {ticker}... Press Ctrl+C to stop.")
        current_price = get_stock_price(ticker)
        print(f"Initial price: {current_price:.2f}")

        while True:
            # Get the latest price
            new_price = get_stock_price(ticker)

            # Check if the price has changed
            if new_price != current_price:
                print(f"Price updated: {new_price:.2f}")
                current_price = new_price

            # Wait for a short interval before checking again
            time.sleep(2)  # Check every 2 seconds

    except KeyboardInterrupt:
        print("\nExiting the program.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
