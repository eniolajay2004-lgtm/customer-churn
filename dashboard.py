import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend import load_data, get_metrics, get_monthly_churn

# -------------------------------
# 🎨 Page Configuration & Styling
# -------------------------------
st.set_page_config(page_title="MTN Churn Analytics", layout="wide")

# Custom CSS for Industry Standard Look (Green, White, Black)
st.markdown("""
    <style>
    :set_root {
        --main-green: #00A651;
        --dark-bg: #111111;
    }
    .stApp { background-color: #FFFFFF; }
    
    /* Top Navigation Bar */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        background-color: white;
        border-bottom: 2px solid #f0f2f6;
        margin-bottom: 25px;
    }
    .user-pill {
        background-color: #00A651;
        color: white;
        padding: 5px 15px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 14px;
    }
    .greeting { font-size: 24px; font-weight: bold; color: #111111; }
    
    /* Metric Cards */
    div[data-testid="stMetricValue"] { color: #00A651 !important; }
    
    /* Buttons and Sidebar */
    .stButton>button {
        background-color: #00A651;
        color: white;
        border-radius: 5px;
    }
    .css-17l2qt2 { background-color: #111111; } /* Sidebar color */
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# 🛰️ Top Navigation & User Pill
# -------------------------------
st.markdown("""
    <div class="top-header">
        <div class="greeting">👋 Hello, Admin</div>
        <div class="user-pill">MTN Network Operations • Online</div>
    </div>
""", unsafe_allow_html=True)

# -------------------------------
# 📂 Sidebar Navigation
# -------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/MTN_Logo.svg/800px-MTN_Logo.svg.png", width=80)
    st.title("Navigation")
    page = st.radio("Go to:", ["📊 Dashboard", "🔍 Predictive Analysis", "📋 Customer Data"])
    
    st.divider()
    st.header("🔎 Filters")
    df = load_data()
    
    # Dynamic Filters
    states = st.multiselect("State", sorted(df["State"].unique()), default=sorted(df["State"].unique())[:5])
    plans = st.multiselect("Subscription Plan", sorted(df["Subscription Plan"].unique()), default=sorted(df["Subscription Plan"].unique()))
    churn_status = st.multiselect("Churn Status", sorted(df["Customer Churn Status"].unique()), default=sorted(df["Customer Churn Status"].unique()))

# Apply Global Filters
filtered_df = df[
    (df["State"].isin(states)) &
    (df["Subscription Plan"].isin(plans)) &
    (df["Customer Churn Status"].isin(churn_status))
]

# -------------------------------
# 🚀 Page Routing Logic
# -------------------------------

if page == "📊 Dashboard":
    st.title("Customer Churn Dashboard")
    metrics = get_metrics(filtered_df)

    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Customers", metrics["total_customers"])
    m2.metric("Churned", metrics["churned_customers"])
    m3.metric("Churn Rate", f"{metrics['churn_rate']}%")
    m4.metric("Revenue Impact", f"₦{metrics['total_revenue']:,}")

    st.divider()

    # Charts Row 1
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📊 Churn by Subscription Plan")
        # FIXED: Using correct column names from your CSV
        sub_churn_data = filtered_df.groupby(['Subscription Plan', 'Customer Churn Status']).size().unstack(fill_value=0)
        
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sub_churn_data.plot(kind='bar', stacked=True, ax=ax1, color=['#111111', '#00A651'])
        ax1.set_title("Subscription Retention vs Churn")
        ax1.set_ylabel("Customer Count")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig1)

    with c2:
        st.subheader("🥧 Churn Distribution")
        churn_dist = filtered_df["Customer Churn Status"].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(churn_dist, labels=churn_dist.index, autopct="%1.1f%%", startangle=90, colors=['#f0f2f6', '#00A651'])
        st.pyplot(fig2)

    # Charts Row 2
    st.subheader("📉 Monthly Churn Trend")
    monthly_churn = get_monthly_churn(filtered_df)
    
    fig3, ax3 = plt.subplots(figsize=(12, 4))
    ax3.bar(monthly_churn.index.astype(str), monthly_churn.values, color="#00A651")
    ax3.set_ylabel("Customers Leaving")
    ax3.grid(axis='y', linestyle='--', alpha=0.3)
    st.pyplot(fig3)

elif page == "🔍 Predictive Analysis":
    st.title("Predictive Insights")
    st.info("This section uses the Logistic Regression model to identify high-risk customers.")
    
    # Example table of high-risk customers
    high_risk = filtered_df[filtered_df["Satisfaction Rate"] <= 2].head(10)
    st.subheader("⚠️ Top 10 High-Risk Customers (Low Satisfaction)")
    st.table(high_risk[["Full Name", "State", "Satisfaction Rate", "Total Revenue"]])

elif page == "📋 Customer Data":
    st.title("Customer Database")
    st.write(f"Showing {len(filtered_df)} records based on current filters.")
    st.dataframe(filtered_df, use_container_width=True)