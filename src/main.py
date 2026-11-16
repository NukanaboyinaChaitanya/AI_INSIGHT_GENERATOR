
from data_processor import (
    load_excel_data,
    clean_data,
    calculate_kpis,
    calculate_category_analysis,
    calculate_subcategory_analysis
)

from business_insights import generate_business_insights

from business_recommendations import generate_business_recommendations


def run_business_analysis(file_path):

    # 1. Load dataset
    orders = load_excel_data(file_path)

    # 2. Clean dataset
    orders_clean = clean_data(orders)

    # 3. Calculate KPIs
    kpi_summary = calculate_kpis(orders_clean)

    # 4. Category analysis
    category_analysis = calculate_category_analysis(orders_clean)

    # 5. Subcategory analysis
    subcategory_analysis = calculate_subcategory_analysis(orders_clean)

    # 6. Generate insights
    insights = generate_business_insights(
        kpi_summary,
        category_analysis,
        subcategory_analysis
    )

    # 7. Generate recommendations
    recommendations = generate_business_recommendations(
        category_analysis,
        subcategory_analysis
    )

    # 8. Display results
    print("\n========== BUSINESS KPIs ==========\n")

    for key, value in kpi_summary.items():
        print(f"{key}: {value}")

    print("\n========== BUSINESS INSIGHTS ==========\n")

    for i, insight in enumerate(insights, start=1):
        print(f"{i}. {insight}")

    print("\n========== BUSINESS RECOMMENDATIONS ==========\n")

    for i, recommendation in enumerate(recommendations, start=1):
        print(f"{i}. {recommendation}")

    return {
        "kpis": kpi_summary,
        "insights": insights,
        "recommendations": recommendations,
        "category_analysis": category_analysis,
        "subcategory_analysis": subcategory_analysis
    }
