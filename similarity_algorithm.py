import pandas as pd

def find_similar_coins(selected_coin, df, most_visited_coins):
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

    # Add most visited coins to the similar coins list
    most_visited_similar = most_visited_coins[most_visited_coins['name'] != selected_coin['name']]
    similar_coins = pd.concat([similar_coins, most_visited_similar]).drop_duplicates(subset=['name'])

    # Return top 5 similar coins
    return similar_coins.head(5)[['name', 'symbol', 'price', 'market_cap', '24h_change']]
