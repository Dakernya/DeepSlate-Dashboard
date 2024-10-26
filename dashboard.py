
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Set up Streamlit UI
st.title("Healthcare Logistics Dashboard")
st.write("A predictive dashboard for real-time healthcare and logistics data.")

# API Details (replace with your details)
API_KEY = "YOUR_API_KEY"
API_ENDPOINT = "https://api.example.com/data"

# Fetch data function
@st.cache_data
def fetch_data():
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(API_ENDPOINT, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)
    else:
        st.error("Failed to fetch data.")
        return pd.DataFrame()

# Load the data
data = fetch_data()

# Check if data is loaded
if not data.empty:
    st.write("### Raw Data")
    st.write(data.head())

    # Convert dates and sort by time for time series
    data['date'] = pd.to_datetime(data['date_column'])  # replace 'date_column' with actual date column name
    data = data.sort_values('date')

    # Display a line chart for data visualization
    st.write("### Data Over Time")
    fig = px.line(data, x='date', y='value_column', title="Data Trend Over Time")  # replace 'value_column' with actual data column
    st.plotly_chart(fig)

    # Simple moving average forecast
    data['Moving_Avg'] = data['value_column'].rolling(window=7).mean()  # 7-day moving average

    # Display comparison chart
    st.write("### Comparison: Actual Data vs. Moving Average Forecast")
    fig, ax = plt.subplots()
    ax.plot(data['date'], data['value_column'], label="Actual Data")
    ax.plot(data['date'], data['Moving_Avg'], label="7-Day Moving Average", linestyle="--")
    ax.set_title("Data and Forecast Comparison")
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.legend()
    st.pyplot(fig)

    # Forecast future values (example extension)
    st.write("### Simple Forecast for Next 7 Days")
    last_value = data['Moving_Avg'].iloc[-1]
    forecast = [last_value] * 7  # Repeat last moving average value for simplicity
    future_dates = pd.date_range(data['date'].iloc[-1] + pd.Timedelta(days=1), periods=7)
    forecast_df = pd.DataFrame({"date": future_dates, "forecast": forecast})
    st.write(forecast_df)

    # Plot forecast
    fig2 = px.line(forecast_df, x='date', y='forecast', title="7-Day Forecast")
    st.plotly_chart(fig2)
else:
    st.write("No data available to display.")
