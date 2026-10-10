import pandas as pd
import joblib



model = joblib.load("models/demand_model.pkl")


def forecast_demand(df):

    
    df["order_date"] = pd.to_datetime(df["order_date"])

    
    daily = (
        df.groupby(
            ["order_date", "product_id"],
            as_index=False
        )["quantity"]
        .sum()
    )

    
    daily = daily.sort_values(
        ["product_id", "order_date"]
    )

   
    daily["lag_1"] = (
        daily.groupby("product_id")["quantity"]
        .shift(1)
    )

    
    daily["lag_7"] = (
        daily.groupby("product_id")["quantity"]
        .shift(7)
    )

    
    daily["rolling_7"] = (
        daily.groupby("product_id")["quantity"]
        .transform(
            lambda x: x.shift(1).rolling(7).mean()
        )
    )

    daily = daily.dropna()

    latest = (
        daily.sort_values("order_date")
        .groupby("product_id")
        .tail(1)
        .copy()
    )

   
    features = [
        "lag_1",
        "lag_7",
        "rolling_7"
    ]

    X_future = latest[features]

   
    predictions = model.predict(X_future)

    result = latest[
        ["product_id", "order_date"]
    ].copy()

    result["predicted_demand"] = predictions

    
    result["predicted_demand"] = (
        result["predicted_demand"].clip(lower=0)
    )

    return result