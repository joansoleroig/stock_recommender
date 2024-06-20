import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path
from PIL import Image

# Add the data_generation folder to the system path to allow imports from there
from data_generation.recommendations import recommend_stocks as recommend_stocks_from_file, recommend_stocks_by_risk  # Importing the recommend_stocks functions

# Load user portfolio data
@st.cache_data
def load_data():
    data = pd.read_csv('./data_generation/user_portfolios.csv')
    data['user_id'] = data['user_id'].astype(str).str.strip()
    return data

# Load precomputed similarity matrices
@st.cache_data
def load_similarity_matrix(filename):
    matrix = pd.read_csv(filename, index_col=0)
    matrix.index = matrix.index.astype(str).str.strip()
    matrix.columns = matrix.columns.astype(str).str.strip()
    return matrix

# Load SP500 companies data
@st.cache_data
def load_sp500_companies():
    return pd.read_csv('data_generation/constituents.csv')

df = load_data()
sector_similarity_matrix = load_similarity_matrix('./data_generation/sector_similarity_matrix.csv')
risk_similarity_matrix = load_similarity_matrix('./data_generation/risk_similarity_matrix.csv')
sp500_companies = load_sp500_companies()

# Streamlit app
st.title("Stock Recommender System")
img = Image.open("finance.webp")
img_cropped = img.crop((150, 50, img.width, 190))
st.image(img_cropped, use_column_width=True)

# Sidebar for user selection
user_ids = df['user_id'].unique()
selected_user_id = st.selectbox("Select User ID", user_ids, index=0)  # Default selection is the first user

selected_user_data = df[df['user_id'] == selected_user_id]

tab1, tab2 = st.tabs(["User Portfolio", "Recommendations"])

with tab1:
    st.subheader(f"User Portfolio for User ID {selected_user_id}")

    # Display user's portfolio
    portfolio_df = selected_user_data[['stock', 'sector', 'weight']]
    st.table(portfolio_df)

    # Calculate and display sector diversification
    sector_data = portfolio_df.groupby('sector')['weight'].sum().reset_index()
    fig, ax = plt.subplots()
    ax.pie(sector_data['weight'], labels=sector_data['sector'], autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)

with tab2:
    subtab1, subtab2 = st.tabs(["Recommendations by Sector", "Recommendations by Risk"])

    with subtab1:
        st.subheader("Recommendations by Sector")

        # Recommend stocks based on the logic in recommendations.py
        recommendations, top_sector = recommend_stocks_from_file(selected_user_id)
        
        if top_sector is None:
            st.write(f"No data found for user ID {selected_user_id}")
        elif recommendations:
            st.write("Top 5 Stocks recommended based on **sector similarity and user similarity**:")

            # Prepare a DataFrame for displaying additional information
            recommendations_df = pd.DataFrame(recommendations, columns=['stock', 'score'])
            recommendations_df = recommendations_df.merge(sp500_companies, how='left', left_on='stock', right_on='Symbol')
            
            # Display only the top 5 recommendations
            top_recommendations = recommendations_df.head(5)

            for index, row in top_recommendations.iterrows():
                st.write(f"**{row['Security']} ({row['Symbol']})**")
                st.write(f"Sector: {row['GICS Sector']}, Sub-Industry: {row['GICS Sub-Industry']}")
                st.write(f"Headquarters: {row['Headquarters Location']}, Founded: {row['Founded']}")
                st.progress(row['score'] / 100)
                st.write(f"Recommendation Score: {row['score']:.2f}%")
                st.write("-----")
        else:
            st.write("No recommendations available for this user.")

    with subtab2:
        st.subheader("Recommendations by Risk")

        # Recommend stocks based on risk similarity
        recommendations = recommend_stocks_by_risk(selected_user_id)
        
        if recommendations:
            st.write("Top 5 Stocks recommended based on **risk similarity**:")

            # Prepare a DataFrame for displaying additional information
            recommendations_df = pd.DataFrame(recommendations, columns=['stock', 'score'])
            recommendations_df = recommendations_df.merge(sp500_companies, how='left', left_on='stock', right_on='Symbol')
            
            # Display only the top 5 recommendations
            top_recommendations = recommendations_df.head(5)

            for index, row in top_recommendations.iterrows():
                st.write(f"**{row['Security']} ({row['Symbol']})**")
                st.write(f"Sector: {row['GICS Sector']}, Sub-Industry: {row['GICS Sub-Industry']}")
                st.write(f"Headquarters: {row['Headquarters Location']}, Founded: {row['Founded']}")
                st.progress(row['score'] / 100)
                st.write(f"Recommendation Score: {row['score']:.2f}%")
                st.write("-----")
        else:
            st.write("No recommendations available for this user.")
