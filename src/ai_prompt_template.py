
def create_business_analysis_prompt(
    kpi_summary,
    category_analysis,
    subcategory_analysis
):
    # Calculate verified findings using Python
    highest_sales = category_analysis["Total_Sales"].idxmax()

    highest_margin = category_analysis["Profit_Margin"].idxmax()

    lowest_margin = category_analysis["Profit_Margin"].idxmin()

    loss_making = subcategory_analysis[
        subcategory_analysis["Total_Profit"] < 0
    ].index.tolist()

    top_subcategories = (
        subcategory_analysis["Profit_Margin"]
        .nlargest(3)
        .index.tolist()
    )

    # Prepare verified findings for the AI
    verified_findings = f"""
VERIFIED BUSINESS FINDINGS:

Overall business profitability:
{"The business is profitable." if kpi_summary["Total Profit"] > 0 else "The business is operating at a loss."}

Category with highest sales: {highest_sales}

Category with highest profit margin: {highest_margin}

Category with lowest profit margin: {lowest_margin}

Loss-making subcategories: {", ".join(loss_making) if loss_making else "None"}

Top three subcategories by profit margin:
{", ".join(top_subcategories)}
"""

    prompt = f"""
You are an experienced retail business analyst.

Your task is to explain the following verified business findings
in simple, professional English.

{verified_findings}

STRICT INSTRUCTIONS:

1. Use only the verified findings supplied above.
2. Do not invent sales figures, profits, percentages or statistics.
3. Do not include any numerical values, currency amounts or percentages.
4. Do not recalculate any metrics.
5. Do not change the names or rankings of categories.
6. Do not assume why a product is profitable or loss-making.
7. Present possible causes as areas to investigate, not confirmed facts.
8. Avoid unsupported claims about customer behaviour or sales trends.

Write your report using these four sections:

1. Executive Summary
2. Key Business Findings
3. Areas of Concern
4. Three Practical Business Recommendations

Keep the report concise, professional and easy to understand.
"""

    return prompt
