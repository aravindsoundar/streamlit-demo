import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# Load database connection details from secrets
conn = st.connection("postgresql", type="sql")
query = 'SELECT * FROM public.stockdata;'
df = conn.query(query, ttl="10m")
# Main application
st.title("Stock Data Analysis")

# Load data
data = df
# Display data
if not data.empty:
    st.write("### Stock Data", data)

    # Basic statistics
    st.write("### Basic Statistics")
    st.write(data.describe())

    # Plotting
    st.write("### Closing Price Over Time")
    plt.figure(figsize=(10, 5))
    plt.plot(data['date'], data['close'], marker='o')
    plt.title('Closing Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.xticks(rotation=45)
    plt.grid()
    st.pyplot(plt)

    # Volume Analysis
    st.write("### Volume Over Time")
    plt.figure(figsize=(10, 5))
    plt.bar(data['date'], data['volume'], color='orange')
    plt.title('Volume Over Time')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.xticks(rotation=45)
    plt.grid()
    st.pyplot(plt)

else:
    st.write("No data available.")
