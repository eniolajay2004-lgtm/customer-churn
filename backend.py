import pandas as pd

def load_data():
    df = pd.read_csv("mtn_customer_churn.csv")
    df.columns = df.columns.str.strip() # Remove hidden spaces
    df["Date of Purchase"] = pd.to_datetime(df["Date of Purchase"], format="%b-%y", errors="coerce")
    df["Customer Churn Status"] = df["Customer Churn Status"].str.strip()
    return df

def get_metrics(df):
    total = df["Customer ID"].nunique()
    churned = df[df["Customer Churn Status"] == "Yes"].shape[0]
    rate = round((churned / total) * 100, 2) if total > 0 else 0
    revenue = df["Total Revenue"].sum()
    return {
        "total_customers": total,
        "churned_customers": churned,
        "churn_rate": rate,
        "total_revenue": revenue
    }

def get_monthly_churn(df):
    churned = df[df["Customer Churn Status"] == "Yes"].copy()
    if churned.empty: return pd.Series()
    return churned.groupby(churned["Date of Purchase"].dt.month).size()