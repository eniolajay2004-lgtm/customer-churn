import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

df = pd.read_csv("mtn_customer_churn.csv")

# Encode categorical columns
encoder = LabelEncoder()
df["Customer Churn Status"] = encoder.fit_transform(df["Customer Churn Status"])

categorical_cols = ["Gender", "Subscription Plan", "MTN Device"]

for col in categorical_cols:
    df[col] = encoder.fit_transform(df[col])

X = df[
    ["Age", "Customer Tenure in months", "Satisfaction Rate",
     "Number of Times Purchased", "Total Revenue"]
]
y = df["Customer Churn Status"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", round(accuracy * 100, 2), "%")
