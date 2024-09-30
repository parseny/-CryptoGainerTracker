import streamlit as st
import pandas as pd
import plotly.express as px
import logging
import os
from pathlib import Path
from api_helpers import fetch_crypto_data, fetch_zapper_data, fetch_crypto_news, fetch_fear_greed_index
from data_processing import process_crypto_data, filter_crypto_data, get_top_gainers, get_most_visited
from visualization import create_price_chart
from similarity_algorithm import find_similar_coins
from constants import COIN_TYPES

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

st.set_page_config(page_title="Crypto Tracker", layout="wide")

# Load custom CSS
css_file = Path(__file__).parent / "style.css"
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def coin_emoji(coin_type):
    if coin_type == 'Major':
        return '🪙'
    elif coin_type == 'Solana Meme':
        return '🌟'
    else:
        return '💎'

# Main application
def main():
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1

    items_per_page = 25

    logging.info("Starting main() function")
    try:
        st.title("Cryptocurrency Tracking Application")

        # Add a loading indicator
        with st.spinner("Loading cryptocurrency data..."):
            logging.info("Starting data fetch...")
            # Fetch and process data
            crypto_data = fetch_crypto_data(timeout=30)
            logging.info(f"Fetched {len(crypto_data)} cryptocurrencies")

            if not crypto_data:
                st.error("Failed to fetch cryptocurrency data. Please try again later.")
                return

            logging.info("Processing crypto data...")
            df = process_crypto_data(crypto_data)
            logging.info(f"Processed {len(df)} valid cryptocurrencies")

            if df.empty:
                st.warning("No valid cryptocurrencies found. Please check the data source and try again.")
                return

        # Sidebar filters
        st.sidebar.header("Filters")
        selected_types = st.sidebar.multiselect("Select Coin Types", COIN_TYPES, default=COIN_TYPES)
        min_price = st.sidebar.number_input("Minimum Price ($)", min_value=0.0, value=0.0)
        max_price = st.sidebar.number_input("Maximum Price ($)", min_value=0.0, value=1000000.0)
        min_market_cap = st.sidebar.number_input("Minimum Market Cap ($)", min_value=0, value=0)

        logging.info("Applying filters...")
        # Apply filters
        filtered_df = filter_crypto_data(df, selected_types, min_price, max_price, min_market_cap)
        logging.info(f"Filtered to {len(filtered_df)} cryptocurrencies")

        # 1. Display Top Gainers (24h) without pagination
        st.markdown('<div class="section-header">Top Gainers (24h)</div>', unsafe_allow_html=True)
        logging.info("Calculating top gainers...")
        top_gainers = get_top_gainers(df, limit=20)
        if not top_gainers.empty:
            st.markdown('<div class="crypto-table">', unsafe_allow_html=True)
            display_top_gainers = top_gainers.copy()
            display_top_gainers['Logo'] = display_top_gainers['type'].apply(coin_emoji)
            display_top_gainers['★'] = '☆'
            columns_order = ['★', 'Logo', 'name', 'symbol', 'price', 'market_cap', '24h_change', '7d_change', '24h_volume']
            display_top_gainers = display_top_gainers[columns_order]
            display_top_gainers['price'] = display_top_gainers['price'].apply(lambda x: f"${x:.2f}")
            display_top_gainers['market_cap'] = display_top_gainers['market_cap'].apply(lambda x: f"${x:,.0f}")
            display_top_gainers['24h_change'] = display_top_gainers['24h_change'].apply(lambda x: f"{x:.2f}%")
            display_top_gainers['7d_change'] = display_top_gainers['7d_change'].apply(lambda x: f"{x:.2f}%")
            display_top_gainers['24h_volume'] = display_top_gainers['24h_volume'].apply(lambda x: f"${x:,.0f}")
            st.table(display_top_gainers)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No top gainers found.")

        st.markdown('<div class="section-header">Similar Coin Recommendations</div>', unsafe_allow_html=True)
        selected_gainer = st.selectbox("Select a top gainer for recommendations", top_gainers['name'].tolist())
        if selected_gainer:
            selected_coin = df[df['name'] == selected_gainer].iloc[0]
            most_visited = get_most_visited(df)
            similar_coins = find_similar_coins(selected_coin, df, most_visited)
            if not similar_coins.empty:
                st.markdown('<div class="crypto-table">', unsafe_allow_html=True)
                display_similar_coins = similar_coins.copy()
                display_similar_coins['Logo'] = display_similar_coins['type'].apply(coin_emoji)
                display_similar_coins['★'] = '☆'
                columns_order = ['★', 'Logo', 'name', 'symbol', 'price', 'market_cap', '24h_change']
                display_similar_coins = display_similar_coins[columns_order]
                display_similar_coins['price'] = display_similar_coins['price'].apply(lambda x: f"${x:.2f}")
                display_similar_coins['market_cap'] = display_similar_coins['market_cap'].apply(lambda x: f"${x:,.0f}")
                display_similar_coins['24h_change'] = display_similar_coins['24h_change'].apply(lambda x: f"{x:.2f}%")
                st.table(display_similar_coins)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("No similar coins found.")
        else:
            st.warning("No top gainer selected for recommendations.")

        # 3. Display Most Visited Cryptocurrencies
        st.markdown('<div class="section-header">Most Visited</div>', unsafe_allow_html=True)
        most_visited = get_most_visited(df)
        if not most_visited.empty:
            st.markdown('<div class="crypto-table">', unsafe_allow_html=True)
            display_most_visited = most_visited.copy()
            display_most_visited['Logo'] = display_most_visited['type'].apply(coin_emoji)
            display_most_visited['★'] = '☆'
            columns_order = ['★', 'Logo', 'name', 'symbol', 'price', '24h_change']
            display_most_visited = display_most_visited[columns_order]
            display_most_visited['price'] = display_most_visited['price'].apply(lambda x: f"${x:.2f}")
            display_most_visited['24h_change'] = display_most_visited['24h_change'].apply(lambda x: f"{x:.2f}%")
            st.table(display_most_visited)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No data available for most visited cryptocurrencies.")

        # 4. All Cryptocurrencies (Paginated)
        st.markdown('<div class="section-header">All Cryptocurrencies</div>', unsafe_allow_html=True)

        # Pagination controls
        total_pages = len(filtered_df) // items_per_page + (1 if len(filtered_df) % items_per_page > 0 else 0)
        col1, col2, col3, col4, col5 = st.columns([1,1,2,1,1])
        with col1:
            if st.button('◀◀ First'):
                st.session_state.page_number = 1
        with col2:
            if st.button('◀ Previous'):
                st.session_state.page_number = max(1, st.session_state.page_number - 1)
        with col3:
            st.write(f'Page {st.session_state.page_number} of {total_pages}')
        with col4:
            if st.button('Next ▶'):
                st.session_state.page_number = min(total_pages, st.session_state.page_number + 1)
        with col5:
            if st.button('Last ▶▶'):
                st.session_state.page_number = total_pages

        # Display paginated cryptocurrency list
        start_idx = (st.session_state.page_number - 1) * items_per_page
        end_idx = start_idx + items_per_page
        paginated_df = filtered_df.iloc[start_idx:end_idx]

        if not paginated_df.empty:
            st.markdown('<div class="crypto-table">', unsafe_allow_html=True)
            display_df = paginated_df.copy()
            display_df['Logo'] = display_df['type'].apply(coin_emoji)
            display_df['★'] = '☆'
            columns_order = ['★', 'Logo', 'name', 'symbol', 'price', 'market_cap', '24h_change', '7d_change', '24h_volume']
            display_df = display_df[columns_order]
            display_df['price'] = display_df['price'].apply(lambda x: f"${x:.2f}")
            display_df['market_cap'] = display_df['market_cap'].apply(lambda x: f"${x:,.0f}")
            display_df['24h_change'] = display_df['24h_change'].apply(lambda x: f"{x:.2f}%")
            display_df['7d_change'] = display_df['7d_change'].apply(lambda x: f"{x:.2f}%")
            display_df['24h_volume'] = display_df['24h_volume'].apply(lambda x: f"${x:,.0f}")
            st.table(display_df)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No cryptocurrencies match the current filters or page number.")

        # Sidebar - Fear and Greed Index
        st.sidebar.markdown('<div class="section-header">Fear and Greed Index</div>', unsafe_allow_html=True)
        fear_greed_index = fetch_fear_greed_index()
        if fear_greed_index:
            st.sidebar.metric("Fear and Greed Index", fear_greed_index['value'], fear_greed_index['value_classification'])
        else:
            st.sidebar.warning("Unable to fetch Fear and Greed Index")

        # Sidebar - Latest Crypto News
        st.sidebar.markdown('<div class="section-header">Latest Crypto News</div>', unsafe_allow_html=True)
        news_items = fetch_crypto_news()
        if news_items:
            for item in news_items:
                st.sidebar.markdown(f"**{item['title']}**")
                st.sidebar.write(item['body'][:200] + "...")
                st.sidebar.markdown(f"[Read more]({item['url']})")
                st.sidebar.markdown("---")
        else:
            st.sidebar.warning("Unable to fetch latest crypto news")

    except Exception as e:
        logging.error(f"An error occurred in main(): {str(e)}")
        st.error("An unexpected error occurred. Please try again later.")

if __name__ == "__main__":
    logging.info(f"COINMARKETCAP_API_KEY is {'set' if os.environ.get('COINMARKETCAP_API_KEY') else 'not set'}")
    logging.info(f"ZAPPER_API_KEY is {'set' if os.environ.get('ZAPPER_API_KEY') else 'not set'}")
    main()
