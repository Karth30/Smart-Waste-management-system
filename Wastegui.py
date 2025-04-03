import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# Google Sheets URL (Replace with the correct one if needed)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1bYjM5O-qsO4kNUgJvQh6wz-q_fQyW1vYysjDPECVwpc/edit?gid=0#gid=0"

# Function to fetch data
def fetch_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = ['Timestamp', 'Distance', 'SmokeDetected', 'AlertStatus']
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Streamlit UI
st.title("Gas and Distance Monitoring Dashboard")

data = fetch_data()
if not data.empty:
    latest_data = data.iloc[-1]
    st.metric("Current Distance (cm)", f"{latest_data['Distance']:.2f}")
    st.metric("Gas Detection", latest_data['SmokeDetected'])
    st.metric("Alert Status", latest_data['AlertStatus'])

    # Filter Alerts
    alerts = data[data['AlertStatus'] != 'No Alert']
    st.subheader("Alerts")
    st.write(alerts[['Timestamp', 'Distance', 'SmokeDetected', 'AlertStatus']])

    # Gas Value Trend
    st.subheader("Gas Value Trend Over Time")
    fig, ax = plt.subplots()
    ax.plot(data['Timestamp'], data['Distance'], label='Distance')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Distance (cm)")
    ax.legend()
    st.pyplot(fig)

    # Alert Frequency Graph
    st.subheader("Alert Frequency")
    alert_counts = alerts.resample('H', on='Timestamp').count()
    fig, ax = plt.subplots()
    ax.bar(alert_counts.index, alert_counts['AlertStatus'])
    ax.set_xlabel("Time")
    ax.set_ylabel("Alert Count")
    st.pyplot(fig)

else:
    st.warning("No data available. Make sure the Google Sheet is accessible.")
