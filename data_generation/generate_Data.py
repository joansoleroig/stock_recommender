import pandas as pd
import numpy as np
import yfinance as yf
from faker import Faker

# Initialize Faker for generating random names
fake = Faker()

# Function to get 10 random stocks from the S&P 500 and assign sectors
def get_random_stocks(sp500_df, num_stocks=10):
    selected_stocks = sp500_df.sample(n=num_stocks, random_state=np.random.randint(1000))
    stock_sector = dict(zip(selected_stocks['Symbol'], selected_stocks['GICS Sector']))
    return stock_sector

# Function to generate portfolio percentages
def generate_portfolio():
    weights = np.random.dirichlet(np.ones(10), size=1)[0] * 100
    return weights

# Generate data for 500 users
def generate_user_data(sp500_df, num_users=500):
    users = []
    for user_id in range(num_users):
        name = fake.name()
        stock_sector = get_random_stocks(sp500_df)
        portfolio = generate_portfolio()
        user_data = {
            'user_id': user_id,
            'name': name,
            'stocks': list(stock_sector.keys()),
            'sectors': list(stock_sector.values()),
            'portfolio': portfolio
        }
        users.append(user_data)
    return users

# Save user data to CSV
def save_to_csv(users, filename='user_portfolios.csv'):
    data = []
    for user in users:
        for stock, sector, weight in zip(user['stocks'], user['sectors'], user['portfolio']):
            data.append([user['user_id'], user['name'], stock, sector, weight])
    df = pd.DataFrame(data, columns=['user_id', 'name', 'stock', 'sector', 'weight'])
    df.to_csv(filename, index=False)

# Main function
if __name__ == "__main__":
    # Load S&P 500 constituents from CSV
    sp500_df = pd.read_csv('constituents.csv')
    users = generate_user_data(sp500_df)
    save_to_csv(users)
