import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend import load_data, get_metrics, get_monthly_churn

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Telecom Customer Churn Dashboard",
    layout="wide"
)

# -------------------------------
# Custom CSS Styling
# -------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f6f9;
    }
    .header {
        background-color: #0C2C55;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .header h1 {
        color: white;
        text-align: center;
        font-size: 40px;
    }
    .header p {
        color: #dcdde1;
        text-align: center;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# Header
# -------------------------------
st.markdown(
    """
    <div class="header">
        <h1>📊 Telecom Customer Churn Dashboard</h1>
        <p>Interactive Customer Churn Analysis</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# Load Data
# -------------------------------
df = load_data()

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔎 Filter Options")

states = st.sidebar.multiselect(
    "Select State",
    options=sorted(df["State"].unique()),
    default=sorted(df["State"].unique())
)

plans = st.sidebar.multiselect(
    "Select Subscription Plan",
    options=sorted(df["Subscription Plan"].unique()),
    default=sorted(df["Subscription Plan"].unique())
)

devices = st.sidebar.multiselect(
    "Select MTN Device",
    options=sorted(df["MTN Device"].unique()),
    default=sorted(df["MTN Device"].unique())
)

churn_status = st.sidebar.multiselect(
    "Select Churn Status",
    options=sorted(df["Customer Churn Status"].unique()),
    default=sorted(df["Customer Churn Status"].unique())
)

# -------------------------------
# Apply Filters
# -------------------------------
filtered_df = df[
    (df["State"].isin(states)) &
    (df["Subscription Plan"].isin(plans)) &
    (df["MTN Device"].isin(devices)) &
    (df["Customer Churn Status"].isin(churn_status))
]

# -------------------------------
# Metrics
# -------------------------------
metrics = get_metrics(filtered_df)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Customers", metrics["total_customers"])
col2.metric("Churned Customers", metrics["churned_customers"])
col3.metric("Churn Rate (%)", metrics["churn_rate"])
col4.metric("Avg Tenure (Months)", metrics["average_tenure"])
col5.metric("Total Revenue", metrics["total_revenue"])

# ======================================================
# 📊 CHURN BY SUBSCRIPTION PLAN (BAR CHART)
# ======================================================
st.subheader("📊 Churn by Subscription Plan")

churn_by_plan = (
    filtered_df[filtered_df["Customer Churn Status"] == "Yes"]
    .groupby("Subscription Plan")
    .size()
)

fig1, ax1 = plt.subplots()
churn_by_plan.plot(kind="bar", ax=ax1)
ax1.set_xlabel("Subscription Plan")
ax1.set_ylabel("Number of Churned Customers")
ax1.set_title("Churned Customers by Subscription Plan")
plt.xticks(rotation=45)

st.pyplot(fig1)

# ======================================================
# 🥧 CHURN DISTRIBUTION (PIE CHART)
# ======================================================
st.subheader("🥧 Churn Distribution")

churn_distribution = filtered_df["Customer Churn Status"].value_counts()

fig2, ax2 = plt.subplots()
ax2.pie(
    churn_distribution,
    labels=churn_distribution.index,
    autopct="%1.1f%%",
    startangle=90
)
ax2.set_title("Customer Churn Distribution")

st.pyplot(fig2)

# ======================================================
# 📉 Monthly Churn Trend
# ======================================================
st.subheader("📉 Monthly Customer Churn")

monthly_churn = get_monthly_churn(filtered_df)

fig3, ax3 = plt.subplots()
ax3.plot(monthly_churn.index, monthly_churn.values, marker="o")
ax3.set_xlabel("Month")
ax3.set_ylabel("Customers Leaving")
ax3.set_title("Customers Leaving Per Month")

st.pyplot(fig3)

# -------------------------------
# Dataset Preview
# -------------------------------
st.subheader("📋 Filtered Dataset Preview")
st.dataframe(filtered_df.head(20))
