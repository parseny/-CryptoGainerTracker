import pandas as pd
from constants import COIN_TYPES

def process_crypto_data(crypto_data):
    df = pd.DataFrame(crypto_data)
    df['price'] = df['quote'].apply(lambda x: x['USD']['price'])
    df['market_cap'] = df['quote'].apply(lambda x: x['USD']['market_cap'])
    df['24h_change'] = df['quote'].apply(lambda x: x['USD']['percent_change_24h'])
    
    # Categorize coins
    df['type'] = 'Other'
    df.loc[df['market_cap'] > 1e9, 'type'] = 'Major'
    df.loc[df['platform'].notna() & (df['platform'].apply(lambda x: x['symbol'] == 'SOL')), 'type'] = 'Solana Meme'

    return df[['id', 'name', 'symbol', 'price', 'market_cap', '24h_change', 'type']]

def filter_crypto_data(df, selected_types, min_price, max_price, min_market_cap):
    return df[
        (df['type'].isin(selected_types)) &
        (df['price'] >= min_price) &
        (df['price'] <= max_price) &
        (df['market_cap'] >= min_market_cap)
    ]

def get_top_gainers(df, limit=10):
    return df.nlargest(limit, '24h_change')
