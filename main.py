import streamlit as st
import pandas as pd
import plotly.express as px
from api_helpers import fetch_crypto_data, fetch_zapper_data
from data_processing import process_crypto_data, filter_crypto_data, get_top_gainers
from visualization import create_price_chart
from similarity_algorithm import find_similar_coins
from constants import COIN_TYPES

st.set_page_config(page_title="Crypto Tracker", layout="wide")

# Main application
def main():
    st.title("Cryptocurrency Tracking Application")

    # Fetch and process data
    crypto_data = fetch_crypto_data()
    df = process_crypto_data(crypto_data)

    # Sidebar filters
    st.sidebar.header("Filters")
    selected_types = st.sidebar.multiselect("Select Coin Types", COIN_TYPES, default=COIN_TYPES)
    min_price = st.sidebar.number_input("Minimum Price ($)", min_value=0.0, value=0.0)
    max_price = st.sidebar.number_input("Maximum Price ($)", min_value=0.0, value=1000000.0)
    min_market_cap = st.sidebar.number_input("Minimum Market Cap ($)", min_value=0, value=0)

    # Apply filters
    filtered_df = filter_crypto_data(df, selected_types, min_price, max_price, min_market_cap)

    # Display filtered cryptocurrency list
    st.header("Cryptocurrency List")
    st.dataframe(filtered_df[['name', 'symbol', 'price', 'market_cap', '24h_change', 'type']])

    # Top gainers section
    st.header("Top Gainers (24h)")
    top_gainers = get_top_gainers(df)
    st.dataframe(top_gainers[['name', 'symbol', 'price', 'market_cap', '24h_change']])

    # Similar coin recommendations
    st.header("Similar Coin Recommendations")
    selected_gainer = st.selectbox("Select a top gainer for recommendations", top_gainers['name'])
    if selected_gainer:
        selected_coin = df[df['name'] == selected_gainer].iloc[0]
        similar_coins = find_similar_coins(selected_coin)
        st.dataframe(similar_coins[['name', 'symbol', 'price', 'market_cap', '24h_change']])

    # Price chart for selected coin
    if selected_gainer:
        st.header(f"Price Chart: {selected_gainer}")
        chart = create_price_chart(selected_coin)
        st.plotly_chart(chart)

if __name__ == "__main__":
    main()
