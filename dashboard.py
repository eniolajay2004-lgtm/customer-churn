import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend import load_data, get_metrics, get_monthly_churn

st.set_page_config(page_title="Telecom Customer Churn Dashboard")

st.title("📊 Telecom Customer Churn Dashboard")

# Load data
df = load_data()

# Metrics
metrics = get_metrics(df)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Customers", metrics["total_customers"])
col2.metric("Churned Customers", metrics["churned_customers"])
col3.metric("Churn Rate (%)", metrics["churn_rate"])
col4.metric("Avg Tenure (Months)", metrics["average_tenure"])
col5.metric("Total Revenue", metrics["total_revenue"])

# Monthly churn chart
st.subheader("📉 Monthly Customer Churn")

monthly_churn = get_monthly_churn(df)

fig, ax = plt.subplots()
ax.plot(monthly_churn.index, monthly_churn.values, marker="o")
ax.set_xlabel("Month")
ax.set_ylabel("Customers Leaving")
ax.set_title("Customers Leaving Per Month")

st.pyplot(fig)

# Show data
st.subheader("📋 Dataset Preview")
st.dataframe(df.head(20))
