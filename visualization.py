import plotly.graph_objs as go
import yfinance as yf

def create_price_chart(coin_data):
    # Fetch historical data using yfinance
    ticker = yf.Ticker(f"{coin_data['symbol']}-USD")
    hist = ticker.history(period="1mo")

    # Create the chart
    fig = go.Figure(data=go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close']
    ))

    fig.update_layout(
        title=f"{coin_data['name']} ({coin_data['symbol']}) Price Chart - Last 30 Days",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        height=500
    )
    return fig
