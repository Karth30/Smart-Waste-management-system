import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

SHEET_URL = "https://docs.google.com/spreadsheets/d/1bYjM5O-qsO4kNUgJvQh6wz-q_fQyW1vYysjDPECVwpc/gviz/tq?tqx=out:csv"

USERS = {"admin": "waste"}

# Function to fetch data
def fetch_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = ['Timestamp', 'Distance', 'GasValue', 'SmokeDetected', 'AlertStatus']
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# User Authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.experimental_rerun()

# Main App Logic
if not st.session_state.logged_in:
    st.sidebar.title("Authentication")
    login()
else:
    st.sidebar.write(f"Logged in as: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        logout()

    # Streamlit UI
    st.title("Gas and Distance Monitoring Dashboard")
    data = fetch_data()
    if not data.empty:
        latest_data = data.iloc[-1]
        st.metric("Current Distance (cm)", f"{latest_data['Distance']:.2f}")
        st.metric("Gas Sensor Value", latest_data['GasValue'])
        st.metric("Smoke Detection", latest_data['SmokeDetected'])
        st.metric("Alert Status", latest_data['AlertStatus'])

        # Filter Alerts
        alerts = data[data['AlertStatus'] != 'No Alert']
        st.subheader("Alerts")
        st.write(alerts[['Timestamp', 'Distance', 'GasValue', 'SmokeDetected', 'AlertStatus']])

        # Distance Trend Over Time
        st.subheader("Distance Trend Over Time")
        fig, ax = plt.subplots()
        ax.plot(data['Timestamp'], data['Distance'], label='Distance', color='blue')
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Distance (cm)")
        ax.legend()
        st.pyplot(fig)

        # Gas Sensor Trend Over Time
        st.subheader("Gas Sensor Trend Over Time")
        fig, ax = plt.subplots()
        ax.plot(data['Timestamp'], data['GasValue'], label='Gas Value', color='red')
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Gas Sensor Value")
        ax.legend()
        st.pyplot(fig)

    else:
        st.warning("No data available. Make sure the Google Sheet is accessible.")
    
    # Force manual refresh
    if st.button("Refresh Data"):
        st.rerun()
