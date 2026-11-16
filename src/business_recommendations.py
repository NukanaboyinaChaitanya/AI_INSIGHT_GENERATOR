
def generate_business_recommendations(
    category_analysis,
    subcategory_analysis
):

    recommendations = []

    # 1. Identify low-profit categories

    lowest_category = category_analysis[
        "Profit_Margin"
    ].idxmin()

    lowest_category_margin = category_analysis.loc[
        lowest_category, "Profit_Margin"
    ]

    if lowest_category_margin < 10:

        recommendations.append(
            f"Review the pricing and discount strategy for "
            f"{lowest_category}. Its profit margin is only "
            f"{lowest_category_margin:.2f}%. "
            f"Investigate product costs and discount levels."
        )

    # 2. Identify loss-making subcategories

    loss_making = subcategory_analysis[
        subcategory_analysis["Total_Profit"] < 0
    ]

    for subcategory, row in loss_making.iterrows():

        recommendations.append(
            f"Investigate {subcategory}, which generated a loss of "
            f"${abs(row['Total_Profit']):,.2f}. "
            f"Review its pricing, costs and discount patterns."
        )

    # 3. Identify high-margin subcategory

    highest_subcategory = subcategory_analysis[
        "Profit_Margin"
    ].idxmax()

    highest_margin = subcategory_analysis.loc[
        highest_subcategory, "Profit_Margin"
    ]

    recommendations.append(
        f"Study the business strategy behind {highest_subcategory}, "
        f"which has the highest subcategory profit margin "
        f"of {highest_margin:.2f}%."
    )

    return recommendations
