import pandas as pd

def load_data():
    df = pd.read_csv("mtn_customer_churn.csv")
    df["Date of Purchase"] = pd.to_datetime(df["Date of Purchase"], errors="coerce")
    df["Customer Churn Status"] = df["Customer Churn Status"].str.strip()
    return df

def get_metrics(df):
    total_customers = df["Customer ID"].nunique()
    churned_customers = df[df["Customer Churn Status"] == "Yes"].shape[0]
    churn_rate = round((churned_customers / total_customers) * 100, 2)
    average_tenure = round(df["Customer Tenure in months"].mean(), 2)
    total_revenue = round(df["Total Revenue"].sum(), 2)

    return {
        "total_customers": total_customers,
        "churned_customers": churned_customers,
        "churn_rate": churn_rate,
        "average_tenure": average_tenure,
        "total_revenue": total_revenue
    }

def get_monthly_churn(df):
    churned = df[df["Customer Churn Status"] == "Yes"]
    monthly = churned.groupby(churned["Date of Purchase"].dt.month).size()
    return monthly
