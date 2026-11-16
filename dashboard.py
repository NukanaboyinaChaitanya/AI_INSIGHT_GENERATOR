
import sys
from pathlib import Path

import streamlit as st
import plotly.express as px

# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
SRC_DIR = PROJECT_DIR / "src"
DATA_PATH = PROJECT_DIR / "data" / "sample_-_superstore.xls"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# --------------------------------------------------
# 2. IMPORT EXISTING PROJECT FUNCTIONS
# --------------------------------------------------

from data_processor import (
    load_excel_data,
    clean_data,
    calculate_kpis,
    calculate_category_analysis,
    calculate_subcategory_analysis
)

from business_insights import generate_business_insights
from business_recommendations import generate_business_recommendations


# --------------------------------------------------
# 3. STREAMLIT PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Business Insights Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Insights Dashboard")
st.write("Sales Performance and Business Analysis")


# --------------------------------------------------
# 4. LOAD AND PROCESS DATA
# --------------------------------------------------

@st.cache_data
def prepare_dashboard(file_path):

    orders = load_excel_data(file_path)
    orders_clean = clean_data(orders)

    kpis = calculate_kpis(orders_clean)

    category_analysis = calculate_category_analysis(orders_clean)
    subcategory_analysis = calculate_subcategory_analysis(orders_clean)

    insights = generate_business_insights(
        kpis,
        category_analysis,
        subcategory_analysis
    )

    recommendations = generate_business_recommendations(
        category_analysis,
        subcategory_analysis
    )

    monthly_sales = (
        orders_clean
        .set_index("Order Date")
        .resample("ME")["Sales"]
        .sum()
        .reset_index()
    )

    return (
        kpis,
        monthly_sales,
        category_analysis.reset_index(),
        subcategory_analysis.reset_index(),
        insights,
        recommendations
    )


# --------------------------------------------------
# 5. CHECK DATASET AND PREPARE DASHBOARD
# --------------------------------------------------

if not DATA_PATH.exists():
    st.error("Excel dataset not found. Please check the data folder.")
    st.stop()

try:
    with st.spinner("Loading business data..."):

        (
            kpis,
            monthly_sales,
            category_df,
            subcategory_df,
            insights,
            recommendations
        ) = prepare_dashboard(str(DATA_PATH))

except Exception as error:
    st.error("Unable to prepare the dashboard.")
    st.exception(error)
    st.stop()


# --------------------------------------------------
# 6. DISPLAY KPIs
# --------------------------------------------------

st.header("Business Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${kpis['Total Sales']:,.2f}")
col2.metric("Total Profit", f"${kpis['Total Profit']:,.2f}")
col3.metric("Total Orders", f"{kpis['Total Orders']:,}")
col4.metric("Profit Margin", f"{kpis['Profit Margin']:.2f}%")

col5, col6, col7 = st.columns(3)

col5.metric("Total Customers", f"{kpis['Total Customers']:,}")
col6.metric("Total Quantity", f"{kpis['Total Quantity']:,}")
col7.metric("Average Order Value", f"${kpis['Average Order Value']:,.2f}")


st.divider()


# --------------------------------------------------
# 7. MONTHLY SALES TREND
# --------------------------------------------------

st.header("Monthly Sales Trend")

fig1 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Performance"
)

st.plotly_chart(fig1, use_container_width=True)


# --------------------------------------------------
# 8. SALES BY CATEGORY
# --------------------------------------------------

st.header("Category Performance")

col1, col2 = st.columns(2)

with col1:

    fig2 = px.bar(
        category_df,
        x="Category",
        y="Total_Sales",
        title="Total Sales by Category"
    )

    st.plotly_chart(fig2, use_container_width=True)


# --------------------------------------------------
# 9. PROFIT BY SUBCATEGORY
# --------------------------------------------------

with col2:

    profit_df = subcategory_df.sort_values("Total_Profit")

    fig3 = px.bar(
        profit_df,
        x="Total_Profit",
        y="Sub-Category",
        orientation="h",
        title="Profit by Subcategory",
        color="Total_Profit",
        color_continuous_scale="RdYlGn"
    )

    st.plotly_chart(fig3, use_container_width=True)


st.divider()


# --------------------------------------------------
# 10. BUSINESS INSIGHTS
# --------------------------------------------------

st.header("🔍 Business Insights")

for number, insight in enumerate(insights, start=1):
    st.write(f"**{number}.** {insight}")


# --------------------------------------------------
# 11. BUSINESS RECOMMENDATIONS
# --------------------------------------------------

st.header("💡 Business Recommendations")

for number, recommendation in enumerate(recommendations, start=1):
    st.write(f"**{number}.** {recommendation}")


# --------------------------------------------------
# 12. DETAILED ANALYSIS TABLES
# --------------------------------------------------

with st.expander("View Category Analysis"):

    st.dataframe(category_df, use_container_width=True)

with st.expander("View Subcategory Analysis"):

    st.dataframe(subcategory_df, use_container_width=True)


st.success("Dashboard loaded successfully!")
