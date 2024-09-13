import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Title of the app
st.title("Stock Data Visualization")

# Connect to PostgreSQL database
@st.cache_resource
def get_data():
    conn = st.connection("postgresql", type="sql")
    df = conn.query('SELECT * FROM stockdata;')
    return df

# Load data
df = get_data()

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Sidebar for stock selection with a "like" filter
stock_names = df['name'].unique()
search_term = st.sidebar.text_input("Search for a Stock", "")
filtered_stocks = [name for name in stock_names if search_term.lower() in name.lower()]

if filtered_stocks:
    selected_stock = st.sidebar.selectbox("Select a Stock", filtered_stocks)
    
    # Filter data for the selected stock
    filtered_data = df[df['name'] == selected_stock]

    # Create line chart for open, high, low, close prices
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['open'], mode='lines', name='Open'))
    fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['high'], mode='lines', name='High'))
    fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['low'], mode='lines', name='Low'))
    fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['close'], mode='lines', name='Close'))

    # Update layout for the line chart
    fig.update_layout(title=f'Stock Prices for {selected_stock}', xaxis_title='Date', yaxis_title='Price', xaxis_rangeslider_visible=True)

    # Display line chart
    st.plotly_chart(fig)

    # Create bar chart for volume
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=filtered_data['date'], y=filtered_data['volume'], name='Volume'))
    fig2.update_layout(title=f'Trading Volume for {selected_stock}', xaxis_title='Date', yaxis_title='Volume')

    # Display bar chart
    st.plotly_chart(fig2)

    # Optional: Show a summary of the selected stock
    st.subheader(f"Summary for {selected_stock}")
    st.write(filtered_data.describe())
else:
    st.sidebar.warning("No stocks found. Please refine your search.")
