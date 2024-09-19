import pandas as pd

def find_similar_coins(selected_coin, df):
    # Filter coins with similar market cap and type
    similar_coins = df[
        (df['market_cap'] < selected_coin['market_cap'] * 1.5) &
        (df['market_cap'] > selected_coin['market_cap'] * 0.5) &
        (df['type'] == selected_coin['type']) &
        (df['name'] != selected_coin['name'])
    ]

    # Sort by market cap difference
    similar_coins['market_cap_diff'] = abs(similar_coins['market_cap'] - selected_coin['market_cap'])
    similar_coins = similar_coins.sort_values('market_cap_diff')

    # Return top 5 similar coins
    return similar_coins.head(5)[['name', 'symbol', 'price', 'market_cap', '24h_change']]
