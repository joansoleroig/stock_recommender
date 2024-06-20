import pandas as pd
import yfinance as yf

# Load the constituents data
def load_constituents(filename='constituents.csv'):
    return pd.read_csv(filename)

# Fetch the last month's percentage change for each stock
def fetch_last_month_change(stocks):
    stock_data = yf.download(stocks, period='1mo')['Adj Close']
    last_month_change = stock_data.pct_change().iloc[-1] * 100
    return last_month_change

# Main function to fetch data and save to a new CSV
def main():
    df = load_constituents()
    stocks = df['Symbol'].unique().tolist()

    # Fetch data in chunks to avoid memory issues
    chunk_size = 50
    last_month_changes = pd.Series(dtype=float)
    
    for i in range(0, len(stocks), chunk_size):
        chunk = stocks[i:i + chunk_size]
        try:
            chunk_changes = fetch_last_month_change(chunk)
            last_month_changes = pd.concat([last_month_changes, chunk_changes])
        except Exception as e:
            print(f"Failed to download data for {chunk}: {e}")
    
    # Merge the changes back to the original DataFrame
    df['last_month_move'] = df['Symbol'].map(last_month_changes)
    df.to_csv('constituents_with_changes.csv', index=False)

if __name__ == "__main__":
    main()
