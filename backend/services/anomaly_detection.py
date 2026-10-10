import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df):

    features = [
        "quantity",
        "discount_pct",
        "net_revenue",
        "shipping_cost",
        "marketing_cost",
        "final_profit"
    ]

    data = df[features].copy()

    data = data.fillna(data.median())

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    df = df.copy()

    df["anomaly"] = model.fit_predict(data)

    anomalies = df[df["anomaly"] == -1].copy()

    return anomalies[
        [
            "order_id",
            "product_id",
            "product_name",
            "quantity",
            "net_revenue",
            "final_profit",
            "discount_pct"
        ]
    ]