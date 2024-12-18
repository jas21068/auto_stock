import yfinance as yf
import time
import openai
from datetime import datetime
import pytz

# OpenAI API Key setup
openai.api_key = "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"

# Function to fetch the current stock price
def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d", interval="1m")  # Fetches 1-minute interval data for the current day
    if data.empty:
        raise ValueError(f"No data found for ticker {ticker}")
    return data["Close"].iloc[-1]  # Get the latest closing price

# Function to ask ChatGPT for a stock recommendation
def get_stock_recommendation(previous_ticker=None, temperature=0.7):
    prompt = "Suggest a high-volatility USD stock that fluctuates hourly by 5 to 10% which is not mainstream. response with just ticker."
    if previous_ticker:
        prompt += f" Do not suggest the stock '{previous_ticker}'."
    response = openai.ChatCompletion.create(
        model="chatgpt-4o-latest",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response['choices'][0]['message']['content'].strip()

# Function to check if the time is within the first 4 hours of stock market opening (9:30 AM - 1:30 PM EST)
def is_market_open():
    eastern = pytz.timezone('US/Eastern')
    current_time = datetime.now(eastern)
    market_open_time = current_time.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close_time = current_time.replace(hour=17, minute=30, second=0, microsecond=0)
    return market_open_time <= current_time <= market_close_time

def main():
    investment_amount = float(input("Enter the initial investment amount ($): "))
    temperature = float(input("Enter risk levels (0.0-1.0, where higher is more risky): "))
    previous_ticker = None

    while True:
        # If within the market hours, apply sell conditions
        if is_market_open():
            try:
                # Ask AI for a stock recommendation
                ticker = get_stock_recommendation(previous_ticker, temperature).upper()
                print(f"Investing in: {ticker}")

                current_price = get_stock_price(ticker)
                shares = investment_amount / current_price  # Mock purchase of shares
                initial_benchmark = current_price  # Initial benchmark for profit calculation
                print(f"Bought {shares:.2f} shares of {ticker} at {current_price:.2f} per share.")

                while True:
                    # Get the latest price
                    new_price = get_stock_price(ticker)
                    total_value = shares * new_price
                    profit_loss_percentage = ((new_price - initial_benchmark) / initial_benchmark) * 100
                    total_profit_loss_percentage = ((total_value - investment_amount) / investment_amount) * 100

                    # Display the profit/loss status
                    print(f"Current Price: {new_price:.2f} | Total Value: {total_value:.2f} | "
                            f"Profit/Loss (Benchmark): {profit_loss_percentage:.2f}% | "
                            f"Total Profit/Loss: {total_profit_loss_percentage:.2f}%")


                    # Check for total loss exceeding $100
                    if investment_amount - total_value >= 100:
                        print("Total loss exceeded $100. Selling all shares.")
                        investment_amount = total_value  # Update the investment amount
                        break

                    # Check for total profit exceeding $300
                    if total_value - investment_amount >= 300:
                        print("Total profit exceeded $300. Selling all shares.")
                        investment_amount = total_value  # Update the investment amount
                        break

                    # Logic for selling and updating benchmark
                    if total_profit_loss_percentage <= -1:  # Total loss of 1%
                        print("Price dropped by 1% from the last benchmark. Selling all shares.")
                        investment_amount = total_value  # Update the investment amount
                        break
                    elif profit_loss_percentage <= -1:  # Loss of 1% on benchmark
                        print("Price dropped by 1% from the benchmark. Selling all shares.")
                        investment_amount = total_value  # Update the investment amount
                        break
                    elif profit_loss_percentage >= 2:  # Gain of 2% on benchmark
                        print("Price increased by 2%. Setting a new benchmark.")
                        initial_benchmark = new_price  # Update benchmark
                    elif total_profit_loss_percentage >= 7:  # Total gain of 7%
                        print("Total profit reached 7%. Selling all shares.")
                        investment_amount = total_value  # Update the investment amount
                        break

                    
                    # Wait for a short interval before checking again
                    time.sleep(1)  # Check every second

                # After selling, ask AI for a new stock recommendation
                previous_ticker = ticker

            except KeyboardInterrupt:
                print("\nExiting the program.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break
        else:
            print("Market is closed. Continuing to monitor the stock.")
            time.sleep(3)

if __name__ == "__main__":
    main()
