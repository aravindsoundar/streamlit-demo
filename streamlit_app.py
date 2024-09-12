import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# Load database connection details from secrets
db_config = st.secrets["connections"]["postgresql"]

# Establish connection to the PostgreSQL database
def create_connection():
    try:
        conn = psycopg2.connect(
            dbname=db_config["database"],
            user=db_config["username"],
            password=db_config["password"],
            host=db_config["host"],
            port=db_config["port"]
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Query the stock data
def load_data():
    conn = create_connection()
    if conn is not None:
        query = "SELECT * FROM public.stockdata;"
        df = pd.read_sql(query, conn)
        conn.close()  # Ensure the connection is closed after the query
        return df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if connection failed

# Main application
st.title("Stock Data Analysis")

# Load data
data = load_data()

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
