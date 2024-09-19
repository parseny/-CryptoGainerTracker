import plotly.graph_objs as go
import yfinance as yf
import pandas as pd

def create_price_chart(coin_data):
    symbol = coin_data['symbol']
    name = coin_data['name']
    
    # Check if the coin is a stablecoin (you may need to expand this list)
    stablecoins = ['USDT', 'USDC', 'DAI', 'BUSD', 'UST', 'TUSD']
    
    if symbol not in stablecoins:
        ticker_symbol = f"{symbol}-USD"
    else:
        ticker_symbol = symbol

    try:
        # Fetch historical data using yfinance
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="1mo")

        if len(hist) > 0:
            # Create the candlestick chart
            fig = go.Figure(data=go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close']
            ))
        else:
            # Fallback to line chart if no candlestick data is available
            fig = go.Figure(data=go.Scatter(
                x=pd.date_range(end=pd.Timestamp.now(), periods=30),
                y=[coin_data['price']] * 30,
                mode='lines'
            ))

        fig.update_layout(
            title=f"{name} ({symbol}) Price Chart - Last 30 Days",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            height=500
        )
        return fig
    except Exception as e:
        # If yfinance fails, create a dummy chart with the current price
        fig = go.Figure(data=go.Scatter(
            x=pd.date_range(end=pd.Timestamp.now(), periods=30),
            y=[coin_data['price']] * 30,
            mode='lines'
        ))
        fig.update_layout(
            title=f"{name} ({symbol}) Price Chart - Last 30 Days (Data Unavailable)",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            height=500
        )
        return fig
