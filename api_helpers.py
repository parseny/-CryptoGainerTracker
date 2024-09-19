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

    try:
        response = requests.get(url, params=parameters)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        # Check if the response contains typical cryptocurrency data
        if 'price' in data and 'market_cap' in data:
            return True  # It's likely a valid cryptocurrency
        else:
            return False  # It's likely an account or not a valid cryptocurrency
    except requests.exceptions.RequestException:
        return False  # If there's any error, assume it's not a valid cryptocurrency

def is_valid_cryptocurrency(coin):
    # Check if the coin has a contract address
    if 'platform' in coin and coin['platform'] and 'token_address' in coin['platform']:
        contract_address = coin['platform']['token_address']
        return fetch_zapper_data(contract_address)
    return True  # If there's no contract address, assume it's a valid cryptocurrency
