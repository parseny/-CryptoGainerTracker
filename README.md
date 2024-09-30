
# Cryptocurrency Tracking Application

## Introduction
This Streamlit-based web application provides real-time tracking and analysis of cryptocurrencies. It offers a comprehensive view of the crypto market, including top gainers, similar coin recommendations, and detailed information about various cryptocurrencies.

## Features
- **Top Gainers (24h)**: Displays the top 20 cryptocurrencies with the highest 24-hour price increase.
- **Similar Coin Recommendations**: Suggests similar coins based on the selected top gainer, including tokens from the most visited list.
- **Most Visited Cryptocurrencies**: Shows a list of the most frequently viewed cryptocurrencies.
- **All Cryptocurrencies**: Provides a paginated list of all tracked cryptocurrencies with detailed information.
- **Filtering Options**: Allows users to filter cryptocurrencies based on type, price range, and market cap.
- **Fear and Greed Index**: Displays the current market sentiment.
- **Latest Crypto News**: Shows recent news articles related to the cryptocurrency market.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/crypto-tracking-app.git
   cd crypto-tracking-app
   ```

2. Install [Poetry](https://python-poetry.org/) if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install the dependencies using Poetry:
   ```bash
   poetry install
   ```

4. Set up the necessary API keys as environment variables:
   - `COINMARKETCAP_API_KEY`
   - `ZAPPER_API_KEY`

## Usage

1. Run the application:
   ```bash
   poetry run streamlit run main.py --server.port 5000 --server.headless true
   ```

2. Open your web browser and navigate to `http://localhost:5000`.

3. Use the sidebar filters to customize your view of the cryptocurrency data.

4. Explore the different sections of the application to gain insights into the crypto market.

## Sections
- **Top Gainers**: View the cryptocurrencies with the highest 24-hour price increase.
- **Similar Coin Recommendations**: Get recommendations for coins similar to a selected top gainer.
- **Most Visited**: See the most frequently viewed cryptocurrencies.
- **All Cryptocurrencies**: Browse through a paginated list of all tracked cryptocurrencies.
- **Fear and Greed Index**: Check the current market sentiment.
- **Latest Crypto News**: Stay updated with recent cryptocurrency-related news articles.

## Note
This application uses real-time data from various APIs. Ensure you have a stable internet connection for the best experience.
