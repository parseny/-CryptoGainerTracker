import requests
import os

def fetch_crypto_data():
    # Replace with actual CoinMarketCap API endpoint and parameters
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.environ.get('COINMARKETCAP_API_KEY', 'YOUR_API_KEY_HERE'),
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    return data['data']

def fetch_zapper_data(contract_address):
    # Replace with actual Zapper API endpoint and parameters
    url = f"https://api.zapper.fi/v1/protocols/ethereum/tokens/{contract_address}/stats"
    parameters = {
        'api_key': os.environ.get('ZAPPER_API_KEY', 'YOUR_API_KEY_HERE'),
    }

    response = requests.get(url, params=parameters)
    data = response.json()
    return data
