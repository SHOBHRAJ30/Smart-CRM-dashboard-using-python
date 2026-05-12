import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image


st.set_page_config(
    page_title="CRM Analytics Dashboard",
    page_icon="",
    layout="wide"
)


st.markdown(
    """
    <style>
    .main {
        background-color: #0E1117;
        color: white;
    }

    .stMetric {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }

    h1, h2, h3 {
        color: #00D4FF;
    }

    .css-1d391kg {
        background-color: #161B22;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.sidebar.title(" CRM Navigation")
menu = st.sidebar.radio(
    "Select Section",
    [
        "Dashboard",
        "Customer Analytics",
        "Sales Analytics",
        "Data Table",
        "About Project"
    ]
)


np.random.seed(42)

sample_data = pd.DataFrame({
    "Customer_ID": range(1001, 1051),
    "Customer_Name": [f"Customer {i}" for i in range(1, 51)],
    "City": np.random.choice([
        "Delhi", "Mumbai", "Bangalore", "Kolkata", "Assam"
    ], 50),
    "Sales": np.random.randint(1000, 15000, 50),
    "Orders": np.random.randint(1, 20, 50),
    "Satisfaction": np.random.randint(1, 6, 50),
    "Subscription": np.random.choice([
        "Basic", "Premium", "Enterprise"
    ], 50)
})


st.title(" Smart CRM Dashboard")
st.markdown("### Smart Customer Relationship Management & Business Insights")


if menu == "Dashboard":

    col1, col2, col3, col4 = st.columns(4)

    total_customers = sample_data.shape[0]
    total_sales = sample_data["Sales"].sum()
    avg_orders = round(sample_data["Orders"].mean(), 2)
    avg_satisfaction = round(sample_data["Satisfaction"].mean(), 2)

    col1.metric(" Total Customers", total_customers)
    col2.metric(" Total Sales", f"₹{total_sales:,}")
    col3.metric(" Avg Orders", avg_orders)
    col4.metric(" Avg Satisfaction", avg_satisfaction)

    st.markdown("---")

    
    city_sales = sample_data.groupby("City")["Sales"].sum().reset_index()

    fig_city = px.bar(
        city_sales,
        x="City",
        y="Sales",
        color="City",
        title=" Sales by City",
        text_auto=True
    )

    st.plotly_chart(fig_city, use_container_width=True)

    
    subscription_count = sample_data["Subscription"].value_counts().reset_index()
    subscription_count.columns = ["Subscription", "Count"]

    fig_pie = px.pie(
        subscription_count,
        values="Count",
        names="Subscription",
        title=" Subscription Distribution"
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    
    sales_trend = pd.DataFrame({
        "Month": [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ],
        "Revenue": np.random.randint(20000, 100000, 12)
    })

    fig_line = px.line(
        sales_trend,
        x="Month",
        y="Revenue",
        markers=True,
        title=" Monthly Revenue Trend"
    )

    st.plotly_chart(fig_line, use_container_width=True)


elif menu == "Customer Analytics":

    st.header(" Customer Analytics")

    col1, col2 = st.columns(2)

    
    with col1:
        fig_hist = px.histogram(
            sample_data,
            x="Satisfaction",
            color="Subscription",
            title=" Customer Satisfaction"
        )

        st.plotly_chart(fig_hist, use_container_width=True)

    
    with col2:
        fig_scatter = px.scatter(
            sample_data,
            x="Orders",
            y="Sales",
            color="Subscription",
            size="Sales",
            hover_name="Customer_Name",
            title=" Orders vs Sales"
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader(" Top 10 Customers")

    top_customers = sample_data.sort_values(
        by="Sales",
        ascending=False
    ).head(10)

    st.dataframe(top_customers, use_container_width=True)


elif menu == "Sales Analytics":

    st.header(" Sales Analytics")

    
    city_filter = st.selectbox(
        "Select City",
        sample_data["City"].unique()
    )

    filtered_data = sample_data[
        sample_data["City"] == city_filter
    ]

    st.write(f"Showing analytics for: {city_filter}")

    
    fig_area = px.area(
        filtered_data,
        x="Customer_ID",
        y="Sales",
        title=f" Sales Area Chart - {city_filter}"
    )

    st.plotly_chart(fig_area, use_container_width=True)

    
    fig_box = px.box(
        filtered_data,
        y="Sales",
        color="Subscription",
        title=" Sales Distribution"
    )

    st.plotly_chart(fig_box, use_container_width=True)

    
    donut = filtered_data["Subscription"].value_counts().reset_index()
    donut.columns = ["Subscription", "Count"]

    fig_donut = go.Figure(data=[go.Pie(
        labels=donut["Subscription"],
        values=donut["Count"],
        hole=.5
    )])

    fig_donut.update_layout(title_text=" Subscription Breakdown")

    st.plotly_chart(fig_donut, use_container_width=True)


elif menu == "Data Table":

    st.header(" CRM Data Table")

    search = st.text_input(" Search Customer")

    if search:
        filtered_table = sample_data[
            sample_data["Customer_Name"].str.contains(search, case=False)
        ]
        st.dataframe(filtered_table, use_container_width=True)
    else:
        st.dataframe(sample_data, use_container_width=True)

    csv = sample_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label=" Download Data",
        data=csv,
        file_name="crm_data.csv",
        mime="text/csv"
    )


elif menu == "About Project":

    st.header(" About This CRM Project")

    st.markdown(
        """
        ##  Features Included

        - Smart CRM Dashboard
        - Customer Analytics
        - Interactive Charts & Graphs
        - Sales Insights
        - Subscription Analytics
        - Downloadable Data Reports

        ##  Tech Stack

        - Python
        - Streamlit
        - Pandas
        - Plotly
        - NumPy
        - Matplotlib

        ##  Purpose

        This CRM dashboard helps businesses analyze:

        - Customer behavior
        - Sales growth
        - Revenue trends
        - Subscription performance
        - Customer satisfaction

        ##  Developed By

        Shobhraj Bhattacharjee
        """
    )


st.markdown("---")
st.caption("© 2026 CRM Analytics Dashboard | Developed using Streamlit")