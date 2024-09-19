import plotly.graph_objs as go

def create_price_chart(coin_data):
    # In a real-world scenario, we would fetch historical price data here
    # For this example, we'll create a dummy chart
    x = ['1d', '7d', '30d', '90d', '1y']
    y = [coin_data['price']] * 5  # Dummy data, replace with actual historical prices

    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines+markers'))
    fig.update_layout(
        title=f"{coin_data['name']} ({coin_data['symbol']}) Price Chart",
        xaxis_title="Time Period",
        yaxis_title="Price (USD)",
        height=500
    )
    return fig
