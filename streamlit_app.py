import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Connect to PostgreSQL database
conn = st.connection("postgresql", type="sql")

# Retrieve data from stockdata table
df = conn.query('SELECT * FROM stockdata;')

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Create line chart for open, high, low, close prices
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['date'], y=df['open'], mode='lines', name='Open'))
fig.add_trace(go.Scatter(x=df['date'], y=df['high'], mode='lines', name='High'))
fig.add_trace(go.Scatter(x=df['date'], y=df['low'], mode='lines', name='Low'))
fig.add_trace(go.Scatter(x=df['date'], y=df['close'], mode='lines', name='Close'))
fig.update_layout(title='Stock Prices', xaxis_title='Date', yaxis_title='Price')

# Display line chart
st.plotly_chart(fig)

# Create bar chart for volume
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=df['date'], y=df['volume']))
fig2.update_layout(title='Trading Volume', xaxis_title='Date', yaxis_title='Volume')

# Display bar chart
st.plotly_chart(fig2)
