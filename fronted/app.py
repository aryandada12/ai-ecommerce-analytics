import streamlit as st
import requests
import pandas as pd




st.set_page_config(
    page_title="AI E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)



st.title("AI E-Commerce Analytics")

st.write(
    "AI-powered D2C business analytics, "
    "demand forecasting and recommendations."
)




uploaded_file = st.file_uploader(
    "Upload your orders CSV",
    type=["csv"]
)


if uploaded_file is not None:

    st.success("CSV uploaded successfully!")

    if st.button("Analyze"):

        with st.spinner("Analyzing your business data..."):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "text/csv"
                )
            }

            try:

                response = requests.post(
                    "https://ai-ecommerce-analytics.onrender.com/analyze",
                    files=files
                )



                if response.status_code == 200:

                    result = response.json()

                    st.success("Analysis completed!")


                   

                    st.header("Business Overview")

                    metrics = result["business_metrics"]

                    col1, col2, col3, col4, col5 = st.columns(5)

                    with col1:
                        st.metric(
                            "Orders",
                            f"{metrics['total_orders']:,}"
                        )

                    with col2:
                        st.metric(
                            "Revenue",
                            f"₹{metrics['total_revenue']:,.0f}"
                        )

                    with col3:
                        st.metric(
                            "Profit",
                            f"₹{metrics['total_profit']:,.0f}"
                        )

                    with col4:
                        st.metric(
                            "Units Sold",
                            f"{metrics['total_quantity']:,}"
                        )

                    with col5:
                        st.metric(
                            "Avg Order Value",
                            f"₹{metrics['average_order_value']:,.0f}"
                        )



                    st.divider()

                    st.header("Product Profit Analysis")

                    profit_df = pd.DataFrame(
                        result["profit_analysis"]
                    )

                    if not profit_df.empty:

                        st.dataframe(
                            profit_df,
                            use_container_width=True
                        )

                        st.subheader(
                            "Top Products by Profit"
                        )

                        top_products = (
                            profit_df
                            .sort_values(
                                "profit",
                                ascending=False
                            )
                            .head(10)
                        )

                        chart_data = (
                            top_products
                            .set_index("product_name")["profit"]
                        )

                        st.bar_chart(chart_data)



                    st.divider()

                    st.header("Demand Forecast")

                    forecast_df = pd.DataFrame(
                        result["forecast"]
                    )

                    if not forecast_df.empty:

                        forecast_df[
                            "predicted_demand"
                        ] = forecast_df[
                            "predicted_demand"
                        ].round(2)

                        st.dataframe(
                            forecast_df,
                            use_container_width=True
                        )

                        st.subheader(
                            "🔥 Predicted Demand by Product"
                        )

                        demand_chart = (
                            forecast_df
                            .sort_values(
                                "predicted_demand",
                                ascending=False
                            )
                            .head(10)
                            .set_index("product_id")
                            ["predicted_demand"]
                        )

                        st.bar_chart(
                            demand_chart
                        )


                  

                    st.divider()

                    st.header("Anomaly Detection")

                    anomalies_df = pd.DataFrame(
                        result["anomalies"]
                    )

                    if not anomalies_df.empty:

                        st.warning(
                            f"{len(anomalies_df)} unusual "
                            "orders detected."
                        )

                        st.dataframe(
                            anomalies_df,
                            use_container_width=True
                        )

                    else:

                        st.success(
                            "No unusual orders detected."
                        )



                    st.divider()

                    st.header("Business Recommendations")

                    recommendations = result[
                        "recommendations"
                    ]

                    if recommendations:

                        for rec in recommendations:

                            rec_type = rec.get(
                                "type",
                                "Recommendation"
                            )

                            product = rec.get(
                                "product",
                                "Business"
                            )

                            recommendation = rec.get(
                                "recommendation",
                                ""
                            )

                            st.info(
                                f"**{rec_type}** — "
                                f"{product}\n\n"
                                f"{recommendation}"
                            )

                    else:

                        st.success(
                            "No immediate recommendations."
                        )



                else:

                    st.error(
                        f"API Error: {response.status_code}"
                    )

                    st.write(
                        response.text
                    )


         

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Could not connect to FastAPI."
                )

                st.info(
                    "Make sure FastAPI is running on "
                    "http://127.0.0.1:8000"
                )