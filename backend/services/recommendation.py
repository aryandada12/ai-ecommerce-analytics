def generate_recommendations(
    profit_data,
    forecast_data,
    anomalies
):

    recommendations = []

    

    loss_products = profit_data[
        profit_data["profit"] < 0
    ]

    for _, row in loss_products.head(5).iterrows():

        recommendations.append({
            "type": "Profit Risk",
            "product": row["product_name"],
            "recommendation":
                "Review pricing, discount level, marketing cost "
                "and product cost."
        })


   

    if not forecast_data.empty:

        high_demand = forecast_data.sort_values(
            "predicted_demand",
            ascending=False
        ).head(5)

        for _, row in high_demand.iterrows():

            recommendations.append({
                "type": "Inventory Opportunity",
                "product": row["product_id"],
                "recommendation":
                    "Consider maintaining sufficient inventory "
                    "to meet expected demand."
            })


  
    if len(anomalies) > 0:

        recommendations.append({
            "type": "Anomaly Alert",
            "product": "Multiple Orders",
            "recommendation":
                f"{len(anomalies)} unusual orders detected. "
                "Review these orders for abnormal discounts, "
                "quantities or profitability."
        })


    return recommendations