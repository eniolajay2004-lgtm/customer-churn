import pandas as pd

def load_data():
    # Adding encoding handling for CSVs and stripping column spaces
    df = pd.read_csv("mtn_customer_churn.csv")
    df.columns = df.columns.str.strip() 
    
    df["Date of Purchase"] = pd.to_datetime(df["Date of Purchase"], format="%b-%y", errors="coerce")
    df["Customer Churn Status"] = df["Customer Churn Status"].str.strip()
    return df

def get_metrics(df):
    total_customers = df["Customer ID"].nunique()
    churned_customers = df[df["Customer Churn Status"] == "Yes"].shape[0]
    churn_rate = round((churned_customers / total_customers) * 100, 2) if total_customers > 0 else 0
    total_revenue = round(df["Total Revenue"].sum(), 2)
    
    return {
        "total_customers": total_customers,
        "churned_customers": churned_customers,
        "churn_rate": churn_rate,
        "total_revenue": total_revenue
    }

def get_monthly_churn(df):
    churned = df[df["Customer Churn Status"] == "Yes"].copy()
    if churned.empty:
        return pd.Series()
    # Group by month name/period for better visualization
    monthly = churned.groupby(churned["Date of Purchase"].dt.strftime('%B')).size()
    # Sort months chronologically
    months_order = ["January", "February", "March", "April", "May", "June", 
                    "July", "August", "September", "October", "November", "December"]
    monthly = monthly.reindex(months_order).dropna()
    return monthly