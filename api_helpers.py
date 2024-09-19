import requests
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_crypto_data():
    logging.info("Starting fetch_crypto_data function")
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

    logging.info(f"COINMARKETCAP_API_KEY is {'set' if os.environ.get('COINMARKETCAP_API_KEY') else 'not set'}")
    logging.info("Sending request to CoinMarketCap API")
    try:
        response = requests.get(url, headers=headers, params=parameters)
        logging.info(f"Response status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        logging.info(f"Successfully fetched data for {len(data['data'])} cryptocurrencies")
        return data['data']
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {str(e)}")
        return []

def fetch_zapper_data(contract_address):
    logging.info(f"Starting fetch_zapper_data function for {contract_address}")
    url = f"https://api.zapper.fi/v1/protocols/ethereum/tokens/{contract_address}/stats"
    parameters = {
        'api_key': os.environ.get('ZAPPER_API_KEY', 'YOUR_API_KEY_HERE'),
    }

    logging.info(f"ZAPPER_API_KEY is {'set' if os.environ.get('ZAPPER_API_KEY') else 'not set'}")
    try:
        response = requests.get(url, params=parameters)
        logging.info(f"Zapper API response status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        if 'price' in data and 'market_cap' in data:
            logging.info(f"Valid cryptocurrency data found for {contract_address}")
            return True
        else:
            logging.info(f"Invalid cryptocurrency data for {contract_address}")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching Zapper data: {str(e)}")
        return False

def is_valid_cryptocurrency(coin):
    logging.info(f"Checking validity of {coin.get('name', 'Unknown')}")
    if 'platform' in coin and coin['platform'] and 'token_address' in coin['platform']:
        contract_address = coin['platform']['token_address']
        return fetch_zapper_data(contract_address)
    logging.info(f"{coin.get('name', 'Unknown')} has no contract address, assuming valid")
    return True
