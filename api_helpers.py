import requests
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_crypto_data(timeout=30):
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
        response = requests.get(url, headers=headers, params=parameters, timeout=timeout)
        logging.info(f"Response status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        logging.info(f"Successfully fetched data for {len(data['data'])} cryptocurrencies")
        return data['data']
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from CoinMarketCap: {str(e)}")
        return []

def fetch_zapper_data(contract_address):
    logging.info(f"Fetching Zapper data for contract: {contract_address}")
    url = f"https://api.zapper.fi/v2/addresses/{contract_address}/balances"
    headers = {
        'Authorization': f"Basic {os.environ.get('ZAPPER_API_KEY', 'YOUR_API_KEY_HERE')}"
    }
    try:
        logging.info(f"Sending request to Zapper API for {contract_address}")
        response = requests.get(url, headers=headers)
        logging.info(f"Zapper API response status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        logging.info(f"Successfully fetched Zapper data for {contract_address}")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from Zapper for {contract_address}: {str(e)}")
        return None

def is_valid_cryptocurrency(coin):
    logging.info(f"Validating cryptocurrency: {coin.get('name', 'Unknown')}")
    if 'platform' in coin and coin['platform'] and 'token_address' in coin['platform']:
        contract_address = coin['platform']['token_address']
        zapper_data = fetch_zapper_data(contract_address)
        if zapper_data and 'tokens' in zapper_data:
            is_valid = any(token['address'].lower() == contract_address.lower() for token in zapper_data['tokens'])
            logging.info(f"Cryptocurrency {coin.get('name', 'Unknown')} validation result: {is_valid}")
            return is_valid
    logging.info(f"Cryptocurrency {coin.get('name', 'Unknown')} assumed valid (no contract address or Zapper data)")
    return True

def fetch_crypto_news():
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()['Data']
        return news_data[:5]  # Return the 5 most recent news items
    else:
        logging.error(f"Error fetching news: {response.status_code}")
        return []

def fetch_fear_greed_index():
    url = "https://api.alternative.me/fng/?limit=1"
    response = requests.get(url)
    if response.status_code == 200:
        fng_data = response.json()['data'][0]
        return {
            'value': fng_data['value'],
            'value_classification': fng_data['value_classification']
        }
    else:
        logging.error(f"Error fetching Fear & Greed index: {response.status_code}")
        return None
