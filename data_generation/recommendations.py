import pandas as pd
from collections import defaultdict

# Load data
user_portfolios = pd.read_csv('data_generation/user_portfolios.csv')
sector_similarity_matrix = pd.read_csv('data_generation/sector_similarity_matrix.csv', index_col=0)
sp500_companies = pd.read_csv('data_generation/constituents.csv')  # Contains columns 'Symbol' and 'GICS Sector'
constituents_with_changes = pd.read_csv('data_generation/constituents_with_changes.csv')
risk_similarity_matrix = pd.read_csv('data_generation/risk_similarity_matrix.csv', index_col=0)

# Ensure user_id is treated as a string across all dataframes
user_portfolios['user_id'] = user_portfolios['user_id'].astype(str).str.strip()
sector_similarity_matrix.index = sector_similarity_matrix.index.astype(str).str.strip()
sector_similarity_matrix.columns = sector_similarity_matrix.columns.astype(str).str.strip()
risk_similarity_matrix.columns = risk_similarity_matrix.columns.astype(str)
risk_similarity_matrix.index = risk_similarity_matrix.index.astype(str)

# Function to get top sector for a user
def get_top_sector(user_id):
    user_data = user_portfolios[user_portfolios['user_id'] == user_id]
    if user_data.empty:
        return None
    top_sector = user_data.groupby('sector')['weight'].sum().idxmax()
    return top_sector

# Function to recommend stocks based on top sector and similar users
def recommend_stocks(user_id):
    top_sector = get_top_sector(user_id)
    if top_sector is None:
        return None, f"No data found for user_id {user_id}"
    
    all_users = sector_similarity_matrix.index
    
    # Aggregate stocks in the top sector from all users
    all_users_data = user_portfolios[user_portfolios['user_id'].isin(all_users)]
    sector_stocks = all_users_data[all_users_data['sector'] == top_sector]
    
    # Calculate weighted similarity scores for each stock
    stock_similarity_scores = defaultdict(float)
    for other_user_id in all_users:
        if other_user_id != user_id:
            similarity_score = sector_similarity_matrix.loc[user_id, other_user_id]
            user_stocks = sector_stocks[sector_stocks['user_id'] == other_user_id]['stock']
            for stock in user_stocks:
                stock_similarity_scores[stock] += similarity_score
    
    # Filter out stocks already owned by the user
    user_stocks = set(user_portfolios[user_portfolios['user_id'] == user_id]['stock'])
    recommended_stocks = {stock: score for stock, score in stock_similarity_scores.items() if stock not in user_stocks}
    
    # Normalize the scores to percentages
    max_score = max(recommended_stocks.values(), default=0)
    if max_score > 0:
        recommended_stocks_percentage = {stock: (score / max_score) * 100 for stock, score in recommended_stocks.items()}
    else:
        recommended_stocks_percentage = recommended_stocks
    
    # Sort recommendations by weighted similarity score and return
    sorted_recommendations = sorted(recommended_stocks_percentage.items(), key=lambda x: x[1], reverse=True)
    return sorted_recommendations, top_sector

# Function to recommend stocks based on risk similarity
def recommend_stocks_by_risk(user_id):
    if user_id not in risk_similarity_matrix.index:
        raise ValueError(f"User ID {user_id} not found in the risk similarity matrix")

    stock_scores = defaultdict(float)

    # Get the list of stocks already owned by the user
    user_owned_stocks = set(user_portfolios[user_portfolios['user_id'] == user_id]['stock'])

    # Iterate through each stock in constituents_with_changes
    for stock in constituents_with_changes['Symbol']:
        if stock in user_owned_stocks:
            continue  # Skip stocks already owned by the user

        # Find users who have this stock in their portfolio
        for _, user_row in user_portfolios[user_portfolios['stock'] == stock].iterrows():
            other_user_id = user_row['user_id']
            weight = user_row['weight']
            
            if other_user_id in risk_similarity_matrix.columns:
                similarity = risk_similarity_matrix.at[user_id, other_user_id]
                if pd.isna(similarity):
                    similarity = 0
                stock_scores[stock] += weight * similarity

    # Normalize the scores to percentages
    if stock_scores:
        max_score = max(stock_scores.values())
        min_score = min(stock_scores.values())
        if max_score > min_score:
            normalized_scores = {stock: 100 * (score - min_score) / (max_score - min_score) for stock, score in stock_scores.items()}
        else:
            normalized_scores = {stock: 100 for stock, score in stock_scores.items()}
    else:
        normalized_scores = {}

    # Sort the recommendations by score in descending order
    sorted_recommendations = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)

    return sorted_recommendations
