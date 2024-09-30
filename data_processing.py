import pandas as pd
from constants import COIN_TYPES
from api_helpers import is_valid_cryptocurrency

def process_crypto_data(crypto_data):
    # Filter out invalid cryptocurrencies
    valid_crypto_data = [coin for coin in crypto_data if is_valid_cryptocurrency(coin)]
    
    df = pd.DataFrame(valid_crypto_data)
    df['price'] = df['quote'].apply(lambda x: x['USD']['price'])
    df['market_cap'] = df['quote'].apply(lambda x: x['USD']['market_cap'])
    df['24h_change'] = df['quote'].apply(lambda x: x['USD']['percent_change_24h'])
    df['24h_volume'] = df['quote'].apply(lambda x: x['USD']['volume_24h'])
    df['7d_change'] = df['quote'].apply(lambda x: x['USD']['percent_change_7d'])
    
    # Categorize coins
    df['type'] = 'Other'
    df.loc[df['market_cap'] > 1e9, 'type'] = 'Major'
    df.loc[df['platform'].notna() & (df['platform'].apply(lambda x: x is not None and x.get('symbol') == 'SOL')), 'type'] = 'Solana Meme'

    return df[['id', 'name', 'symbol', 'price', 'market_cap', '24h_change', '24h_volume', '7d_change', 'type']]

def filter_crypto_data(df, selected_types, min_price, max_price, min_market_cap):
    return df[
        (df['type'].isin(selected_types)) &
        (df['price'] >= min_price) &
        (df['price'] <= max_price) &
        (df['market_cap'] >= min_market_cap)
    ]

def get_top_gainers(df, limit=20):  # Changed from 10 to 20
    return df.nlargest(limit, '24h_change')

def get_most_visited(df, limit=5):
    return df.sample(n=limit)  # Randomly select 5 cryptocurrencies as a placeholder
