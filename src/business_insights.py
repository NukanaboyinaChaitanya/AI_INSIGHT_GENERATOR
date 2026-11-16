
def generate_business_insights(
    kpi_summary,
    category_analysis,
    subcategory_analysis
):

    insights = []

    # 1. Sales performance
    insights.append(
        f"The business generated total sales of "
        f"${kpi_summary['Total Sales']:,.2f}."
    )

    # 2. Profit performance
    insights.append(
        f"The total profit generated was "
        f"${kpi_summary['Total Profit']:,.2f}."
    )

    # 3. Profit margin analysis
    margin = kpi_summary["Profit Margin"]

    insights.append(
        f"The overall profit margin is {margin}%."
    )

    if margin < 0:
        insights.append(
            "Warning: The business is operating at an overall loss."
        )

    elif margin < 10:
        insights.append(
            "The profit margin is below 10%. "
            "Profitability needs attention."
        )

    else:
        insights.append(
            "The business has a profit margin above 10%."
        )

    # 4. Customer performance
    insights.append(
        f"The business served "
        f"{kpi_summary['Total Customers']} unique customers."
    )

    # 5. Order performance
    insights.append(
        f"A total of {kpi_summary['Total Orders']} unique orders "
        f"were placed."
    )

    # 6. Category profitability analysis

    lowest_margin_category = category_analysis[
        "Profit_Margin"
    ].idxmin()

    lowest_margin = category_analysis.loc[
        lowest_margin_category, "Profit_Margin"
    ]

    insights.append(
        f"{lowest_margin_category} has the lowest "
        f"profit margin at {lowest_margin:.2f}%."
    )

    highest_margin_category = category_analysis[
        "Profit_Margin"
    ].idxmax()

    highest_margin = category_analysis.loc[
        highest_margin_category, "Profit_Margin"
    ]

    insights.append(
        f"{highest_margin_category} has the highest "
        f"profit margin at {highest_margin:.2f}%."
    )

    # 7. Subcategory profitability analysis

    lowest_subcategory = subcategory_analysis[
        "Profit_Margin"
    ].idxmin()

    lowest_subcategory_margin = subcategory_analysis.loc[
        lowest_subcategory, "Profit_Margin"
    ]

    insights.append(
        f"{lowest_subcategory} has the lowest profit margin "
        f"at {lowest_subcategory_margin:.2f}%."
    )

    highest_subcategory = subcategory_analysis[
        "Profit_Margin"
    ].idxmax()

    highest_subcategory_margin = subcategory_analysis.loc[
        highest_subcategory, "Profit_Margin"
    ]

    insights.append(
        f"{highest_subcategory} has the highest profit margin "
        f"at {highest_subcategory_margin:.2f}%."
    )

    # 8. Identify loss-making subcategories

    loss_making = subcategory_analysis[
        subcategory_analysis["Total_Profit"] < 0
    ]

    if not loss_making.empty:

        loss_names = ", ".join(
            str(name) for name in loss_making.index.tolist()
        )

        insights.append(
            f"The following subcategories are generating losses: "
            f"{loss_names}."
        )

    else:
        insights.append(
            "No loss-making subcategories were identified."
        )

    return insights
