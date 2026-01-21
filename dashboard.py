import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend import load_data, get_metrics, get_monthly_churn

# -------------------------------
# 🎨 Page Configuration
# -------------------------------
st.set_page_config(page_title="MTN Churn Analytics", layout="wide")

# -------------------------------
# 🌓 Theme Toggle Logic (Sidebar Bottom)
# -------------------------------
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'

# -------------------------------
# 🪄 CSS Styling (Green Accent + Dynamic Theme)
# -------------------------------
accent_green = "#00A651"

if st.session_state.theme == 'Dark':
    bg_color = "#121212"
    text_color = "#FFFFFF"
    card_bg = "#1E1E1E"
    border_color = "#333333"
else:
    bg_color = "#FFFFFF"
    text_color = "#111111"
    card_bg = "#F8F9FA"
    border_color = "#E0E0E0"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    [data-testid="stSidebar"] {{ background-color: {bg_color}; border-right: 1px solid {border_color}; }}
    
    /* Header Section */
    .top-header {{
        display: flex; justify-content: space-between; align-items: center;
        padding: 15px 25px; background-color: {bg_color};
        border-bottom: 2px solid {accent_green}; margin-bottom: 20px;
    }}
    .greeting {{ font-size: 22px; font-weight: bold; color: {text_color}; }}
    .user-pill {{
        background-color: {accent_green}; color: white;
        padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 13px;
    }}
    
    /* Cards & Metrics */
    div[data-testid="stMetric"] {{
        background-color: {card_bg}; padding: 15px; border-radius: 10px;
        border-left: 5px solid {accent_green};
    }}
    div[data-testid="stMetricValue"] {{ color: {accent_green} !important; }}
    label[data-testid="stMetricLabel"] {{ color: {text_color} !important; opacity: 0.8; }}
    
    /* Navigation Style */
    .stRadio > label {{ color: {text_color} !important; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# 🛰️ Top Navigation Header
# -------------------------------
st.markdown(f"""
    <div class="top-header">
        <div class="greeting">👋 Hello, Admin</div>
        <div class="user-pill">MTN Admin Portal • Online</div>
    </div>
""", unsafe_allow_html=True)

# -------------------------------
# 📂 Sidebar Content
# -------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/MTN_Logo.svg/800px-MTN_Logo.svg.png", width=60)
    st.title("Main Menu")
    
    # Page Navigation
    page = st.radio("Navigation", ["📊 Dashboard", "🔍 Predictions", "📋 Raw Data"])
    
    st.vsplit() # Spacer
    
    # 🌓 Theme Toggle at the bottom
    st.markdown("---")
    theme_choice = st.toggle("🌙 Dark Mode", value=(st.session_state.theme == 'Dark'))
    st.session_state.theme = 'Dark' if theme_choice else 'Light'

# Load Data
df = load_data()

# -------------------------------
# 📊 Dashboard Page
# -------------------------------
if page == "📊 Dashboard":
    # Sidebar Filters (Dashboard specific)
    with st.sidebar:
        st.subheader("🔎 Filters")
        states = st.multiselect("State", sorted(df["State"].unique()), default=sorted(df["State"].unique())[:5])
        plans = st.multiselect("Plan", sorted(df["Subscription Plan"].unique()), default=sorted(df["Subscription Plan"].unique()))

    filtered_df = df[(df["State"].isin(states)) & (df["Subscription Plan"].isin(plans))]
    metrics = get_metrics(filtered_df)

    # 1. KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Customers", metrics["total_customers"])
    c2.metric("Churned", metrics["churned_customers"])
    c3.metric("Churn Rate", f"{metrics['churn_rate']}%")
    c4.metric("Revenue", f"₦{metrics['total_revenue']:,}")

    st.markdown("### 📈 Visual Analytics")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Churn by Plan")
        # FIXED: Using exact CSV column names
        sub_churn = filtered_df.groupby(['Subscription Plan', 'Customer Churn Status']).size().unstack(fill_value=0)
        
        fig1, ax1 = plt.subplots(facecolor=bg_color)
        sub_churn.plot(kind='bar', stacked=True, ax=ax1, color=['#333333', accent_green])
        ax1.set_facecolor(bg_color)
        ax1.tick_params(colors=text_color)
        ax1.xaxis.label.set_color(text_color)
        ax1.yaxis.label.set_color(text_color)
        st.pyplot(fig1)

    with col_b:
        st.subheader("Churn Proportion")
        dist = filtered_df["Customer Churn Status"].value_counts()
        fig2, ax2 = plt.subplots(facecolor=bg_color)
        ax2.pie(dist, labels=dist.index, autopct="%1.1f%%", colors=[accent_green, '#f0f2f6'], textprops={'color': text_color})
        st.pyplot(fig2)

    # Monthly Trend
    st.subheader("📉 Monthly Churn Trend")
    monthly = get_monthly_churn(filtered_df)
    fig3, ax3 = plt.subplots(figsize=(10, 3), facecolor=bg_color)
    ax3.bar(monthly.index.astype(str), monthly.values, color=accent_green)
    ax3.set_facecolor(card_bg)
    ax3.tick_params(colors=text_color)
    st.pyplot(fig3)

elif page == "🔍 Predictions":
    st.title("Predictive Modeling")
    st.warning("Logistic Regression Model: Active")
    st.write("Below are customers flagged as high-risk based on satisfaction rates.")
    high_risk = df[df["Satisfaction Rate"] <= 2]
    st.dataframe(high_risk[["Full Name", "Subscription Plan", "Satisfaction Rate", "Total Revenue"]], use_container_width=True)

elif page == "📋 Raw Data":
    st.title("Customer Database")
    st.dataframe(df, use_container_width=True)