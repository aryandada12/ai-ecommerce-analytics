from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io

from services.demand_forecasting import forecast_demand
from services.anomaly_detection import detect_anomalies
from services.recommendation import generate_recommendations


app = FastAPI(
    title="AI E-Commerce Analytics API"
)


@app.get("/")
def home():
    return {
        "message": "AI E-Commerce Analytics API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

   

    contents = await file.read()

    df = pd.read_csv(
        io.BytesIO(contents)
    )


    

    total_orders = len(df)

    total_revenue = df["net_revenue"].sum()

    total_profit = df["final_profit"].sum()

    total_quantity = df["quantity"].sum()

    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )


 

    profit_data = (
        df.groupby(
            ["product_id", "product_name"],
            as_index=False
        )
        .agg(
            orders=("order_id", "count"),
            units_sold=("quantity", "sum"),
            revenue=("net_revenue", "sum"),
            profit=("final_profit", "sum")
        )
    )


   

    forecast = forecast_demand(df)


   

    anomalies = detect_anomalies(df)


    

    recommendations = generate_recommendations(
        profit_data,
        forecast,
        anomalies
    )


   

    return {

        "status": "success",

        "business_metrics": {
            "total_orders": int(total_orders),
            "total_revenue": float(total_revenue),
            "total_profit": float(total_profit),
            "total_quantity": int(total_quantity),
            "average_order_value": float(
                average_order_value
            )
        },

        "profit_analysis":
            profit_data.to_dict(
                orient="records"
            ),

        "forecast":
            forecast.to_dict(
                orient="records"
            ),

        "anomalies":
            anomalies.to_dict(
                orient="records"
            ),

        "recommendations":
            recommendations
    }