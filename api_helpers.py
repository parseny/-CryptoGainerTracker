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
        logging.error(f"Error fetching data from CoinMarketCap: {str(e)}")
        return []

def fetch_zapper_data(contract_address):
    # Implement Zapper API call here if needed
    pass

def is_valid_cryptocurrency(coin):
    # Implement cryptocurrency validation logic here if needed
    return True
