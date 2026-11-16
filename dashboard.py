
import sys
from pathlib import Path

import streamlit as st
import plotly.express as px


# ==================================================
# 1. PROJECT PATHS
# ==================================================

PROJECT_DIR = Path(__file__).resolve().parent

SRC_DIR = PROJECT_DIR / "src"

DATA_PATH = PROJECT_DIR / "data" / "sample_-_superstore.xls"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# ==================================================
# 2. IMPORT PROJECT MODULES
# ==================================================

from data_processor import (
    load_excel_data,
    clean_data,
    calculate_kpis,
    calculate_category_analysis,
    calculate_subcategory_analysis
)

from business_insights import generate_business_insights

from business_recommendations import generate_business_recommendations

from ai_prompt_template import create_business_analysis_prompt

from ai_generator import generate_ai_business_report


# ==================================================
# 3. STREAMLIT PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Business Insights Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Insights Dashboard")

st.caption(
    "Retail Sales Performance | Business Analytics | AI Storytelling"
)


# ==================================================
# 4. LOAD AND PROCESS DATA
# ==================================================

@st.cache_data
def prepare_dashboard(file_path):

    # Load Excel dataset
    orders = load_excel_data(file_path)

    # Clean data
    orders_clean = clean_data(orders)

    # Calculate KPIs
    kpis = calculate_kpis(orders_clean)

    # Category analysis
    category_analysis = calculate_category_analysis(
        orders_clean
    )

    # Subcategory analysis
    subcategory_analysis = calculate_subcategory_analysis(
        orders_clean
    )

    # Generate rule-based business insights
    insights = generate_business_insights(
        kpis,
        category_analysis,
        subcategory_analysis
    )

    # Generate rule-based recommendations
    recommendations = generate_business_recommendations(
        category_analysis,
        subcategory_analysis
    )

    # Monthly sales analysis
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
        category_analysis,
        subcategory_analysis,
        insights,
        recommendations
    )


# ==================================================
# 5. CHECK DATASET
# ==================================================

if not DATA_PATH.exists():

    st.error(
        f"Excel dataset not found: {DATA_PATH}"
    )

    st.stop()


# ==================================================
# 6. PREPARE DASHBOARD DATA
# ==================================================

try:

    with st.spinner("Preparing business dashboard..."):

        (
            kpis,
            monthly_sales,
            category_analysis,
            subcategory_analysis,
            insights,
            recommendations
        ) = prepare_dashboard(str(DATA_PATH))

except Exception as error:

    st.error("Unable to load business data.")

    st.exception(error)

    st.stop()


# Convert analysis DataFrames for displaying tables
category_df = category_analysis.reset_index()

subcategory_df = subcategory_analysis.reset_index()


# ==================================================
# 7. BUSINESS KPI METRICS
# ==================================================

st.header("📈 Business Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"${kpis['Total Sales']:,.2f}"
)

col2.metric(
    "Total Profit",
    f"${kpis['Total Profit']:,.2f}"
)

col3.metric(
    "Total Orders",
    f"{kpis['Total Orders']:,}"
)

col4.metric(
    "Profit Margin",
    f"{kpis['Profit Margin']:.2f}%"
)


col5, col6, col7 = st.columns(3)

col5.metric(
    "Total Customers",
    f"{kpis['Total Customers']:,}"
)

col6.metric(
    "Total Quantity",
    f"{kpis['Total Quantity']:,}"
)

col7.metric(
    "Average Order Value",
    f"${kpis['Average Order Value']:,.2f}"
)


st.divider()


# ==================================================
# 8. MONTHLY SALES TREND
# ==================================================

st.header("📅 Monthly Sales Trend")

fig1 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Performance"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# ==================================================
# 9. SALES BY CATEGORY
# ==================================================

st.header("📊 Category Performance")

col1, col2 = st.columns(2)

with col1:

    fig2 = px.bar(
        category_df,
        x="Category",
        y="Total_Sales",
        title="Total Sales by Category"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# ==================================================
# 10. PROFIT BY SUBCATEGORY
# ==================================================

with col2:

    profit_df = subcategory_df.sort_values(
        "Total_Profit"
    )

    fig3 = px.bar(
        profit_df,
        x="Total_Profit",
        y="Sub-Category",
        orientation="h",
        title="Profit by Subcategory",
        color="Total_Profit",
        color_continuous_scale="RdYlGn"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )


st.divider()


# ==================================================
# 11. BUSINESS INSIGHTS
# ==================================================

st.header("🔍 Business Insights")

for number, insight in enumerate(insights, start=1):

    st.write(f"**{number}.** {insight}")


# ==================================================
# 12. BUSINESS RECOMMENDATIONS
# ==================================================

st.header("💡 Business Recommendations")

for number, recommendation in enumerate(
    recommendations,
    start=1
):

    st.write(f"**{number}.** {recommendation}")


st.divider()


# ==================================================
# 13. DETAILED ANALYSIS TABLES
# ==================================================

st.header("📋 Detailed Business Analysis")

with st.expander("View Category Analysis"):

    st.dataframe(
        category_df,
        use_container_width=True,
        hide_index=True
    )


with st.expander("View Subcategory Analysis"):

    st.dataframe(
        subcategory_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ==================================================
# 14. AI BUSINESS ANALYST
# ==================================================

st.header("🤖 AI Business Analyst")

st.write(
    "Generate an AI-powered business report using "
    "your local Qwen model through Ollama."
)

# Initialize Streamlit session state
if "ai_report" not in st.session_state:

    st.session_state.ai_report = ""


# AI report generation button
if st.button(
    "Generate AI Business Report",
    type="primary",
    key="generate_ai_report"
):

    # Clear previous report before generating a new one
    st.session_state.ai_report = ""

    try:

        with st.spinner(
            "Qwen is analysing your business data..."
        ):

            # Create prompt using verified Python analysis
            prompt = create_business_analysis_prompt(
                kpis,
                category_analysis,
                subcategory_analysis
            )

            # Generate report using local Ollama model
            ai_report = generate_ai_business_report(
                prompt
            )

            st.session_state.ai_report = ai_report

    except Exception as error:

        st.error(
            f"Unable to generate AI report: {error}"
        )


# ==================================================
# 15. BEFORE AND AFTER COMPARISON
# ==================================================

if st.session_state.ai_report:

    st.divider()

    st.header(
        "📊 Before vs After: Data Storytelling"
    )

    st.write(
        "See how raw numerical analysis is transformed "
        "into understandable business explanations."
    )

    before, after = st.columns(2)

    # ----------------------------------------------
    # BEFORE: RAW NUMERICAL ANALYSIS
    # ----------------------------------------------

    with before:

        st.subheader("Before: Raw Numbers")

        st.caption(
            "Numerical results generated using Python GroupBy analysis."
        )

        st.markdown("**Category Analysis**")

        st.dataframe(
            category_df[
                [
                    "Category",
                    "Total_Sales",
                    "Total_Profit",
                    "Profit_Margin"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("**Subcategory Analysis**")

        st.dataframe(
            subcategory_df[
                [
                    "Sub-Category",
                    "Total_Sales",
                    "Total_Profit",
                    "Profit_Margin"
                ]
            ],
            use_container_width=True,
            hide_index=True,
            height=400
        )


    # ----------------------------------------------
    # AFTER: AI-GENERATED BUSINESS NARRATIVE
    # ----------------------------------------------

    with after:

        st.subheader("After: Business Narrative")

        st.caption(
            "Natural-language explanation generated using Qwen AI."
        )

        st.markdown(
            st.session_state.ai_report
        )


    st.success(
        "Raw business analysis transformed into an "
        "AI-generated business narrative successfully!"
    )

else:

    st.info(
        "Click 'Generate AI Business Report' above to "
        "see the Before and After comparison."
    )


# ==================================================
# 16. FOOTER
# ==================================================

st.divider()

st.caption(
    "Business Insights Dashboard | "
    "Python | Pandas | Plotly | Streamlit | Ollama"
)
