import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Telecom Customer Churn Dashboard",
    layout="centered"
)

# -------------------------------
# Title Section
# -------------------------------
st.title("📊 Telecom Customer Churn Dashboard")
st.write("Monthly Analysis of Customers Leaving the Telecom Company")

# -------------------------------
# Sample Monthly Churn Data
# -------------------------------
churn_data = {
    "Month": [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ],
    "Customers_Leaving": [
        40, 55, 50, 65,
        75, 60, 85, 80,
        70, 90, 105, 95
    ]
}

df = pd.DataFrame(churn_data)

# -------------------------------
# Metrics Section
# -------------------------------
total_customers = 5000
total_churned = df["Customers_Leaving"].sum()
churn_rate = round((total_churned / total_customers) * 100, 2)

st.subheader("📌 Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", total_customers)
col2.metric("Total Churned", total_churned)
col3.metric("Churn Rate (%)", churn_rate)

# -------------------------------
# Line Chart (Monthly Churn)
# -------------------------------
st.subheader("📉 Monthly Customer Churn Trend")

fig, ax = plt.subplots()
ax.plot(
    df["Month"],
    df["Customers_Leaving"],
    marker='o'
)
ax.set_xlabel("Month")
ax.set_ylabel("Number of Customers")
ax.set_title("Number of Customers Leaving Each Month")
plt.xticks(rotation=45)

st.pyplot(fig)

# -------------------------------
# Data Table
# -------------------------------
st.subheader("📋 Monthly Churn Data")
st.dataframe(df)


