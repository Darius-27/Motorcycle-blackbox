
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Bike Blackbox Dashboard", layout="wide")
st.title("🏍 Bike Blackbox Smart Dashboard")

# -----------------------------
# Generate simulated sensor data
# -----------------------------
rows = 200
time = pd.date_range(start="2025-01-01", periods=rows, freq="100ms")

# Acceleration
acc_x = np.random.normal(0, 0.5, rows)
acc_y = np.random.normal(0, 0.5, rows)
acc_z = np.random.normal(1, 0.2, rows)

# Simulate crash event
acc_x[150] = 4.5
acc_y[150] = 3.2
acc_z[150] = 6.0

total_acc = np.sqrt(acc_x**2 + acc_y**2 + acc_z**2)
crash = total_acc > 3

# Speed simulation
speed = np.random.randint(30, 90, rows)

# Engine temperature simulation
engine_temp = np.random.randint(70, 110, rows)

# GPS simulation (Chennai region)
lat = 13.0827 + np.random.uniform(-0.01, 0.01, rows)
lon = 80.2707 + np.random.uniform(-0.01, 0.01, rows)

df = pd.DataFrame({
    "Timestamp": time,
    "Total Acceleration (g)": total_acc,
    "Crash": crash,
    "Speed (km/h)": speed,
    "Engine Temp (°C)": engine_temp,
    "Latitude": lat,
    "Longitude": lon
})

# -----------------------------
# Metrics Section
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Max Acceleration (g)", round(df["Total Acceleration (g)"].max(), 2))
col2.metric("Crash Events", int(df["Crash"].sum()))
col3.metric("Average Speed (km/h)", round(df["Speed (km/h)"].mean(), 2))
col4.metric("Max Engine Temp (°C)", df["Engine Temp (°C)"].max())

# -----------------------------
# Alerts
# -----------------------------

# Crash Alert
if df["Crash"].any():
    st.error("🚨 Crash Detected!")

# Over Speed Alert
if df["Speed (km/h)"].mean() > 60:
    st.error("🚨 Over Speeding Alert! Average Speed > 60 km/h")
else:
    st.success("✅ Speed Within Safe Limit")

# Engine Overheat
if df["Engine Temp (°C)"].max() > 105:
    st.error("🔥 Engine Overheating Detected!")

# -----------------------------
# Acceleration Chart
# -----------------------------
fig1 = px.line(df, x="Timestamp", y="Total Acceleration (g)",
               title="Acceleration Over Time")
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Speed Chart
# -----------------------------
fig2 = px.line(df, x="Timestamp", y="Speed (km/h)",
               title="Speed Over Time")
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Location Map (Latest Position)
# -----------------------------
st.subheader("📍 Current Bike Location")

latest_location = df[["Latitude", "Longitude"]].tail(1)
st.map(latest_location.rename(columns={"Latitude":"lat", "Longitude":"lon"}))

# -----------------------------
# Show Last 10 Records
# -----------------------------
st.subheader("Recent Sensor Data")
st.dataframe(df.tail(10))