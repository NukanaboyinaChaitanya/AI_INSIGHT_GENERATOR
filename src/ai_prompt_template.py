
def create_business_analysis_prompt(
    kpi_summary,
    category_analysis,
    subcategory_analysis
):

    if category_analysis.empty or subcategory_analysis.empty:
        raise ValueError("Business analysis data is empty.")

    # Calculate verified business findings using Python
    highest_sales = category_analysis["Total_Sales"].idxmax()

    highest_margin = category_analysis["Profit_Margin"].idxmax()

    lowest_margin = category_analysis["Profit_Margin"].idxmin()

    # Identify loss-making subcategories
    loss_making = subcategory_analysis[
        subcategory_analysis["Total_Profit"] < 0
    ]

    # Format loss-making subcategories
    if not loss_making.empty:
        loss_details = "\n".join(
            f"{name}: Profit ${row['Total_Profit']:,.2f}, "
            f"Margin {row['Profit_Margin']:.2f}%"
            for name, row in loss_making.iterrows()
        )
    else:
        loss_details = "No loss-making subcategories."

    # Convert analysis tables into readable text
    category_table = category_analysis.round(2).to_string()

    subcategory_table = subcategory_analysis.round(2).to_string()

    prompt = f"""
You are an experienced retail business analyst.

Analyze the following verified retail business results.

BUSINESS KPIs:
{kpi_summary}

VERIFIED CATEGORY FINDINGS:

Category with highest sales: {highest_sales}
Sales: ${category_analysis.loc[highest_sales, 'Total_Sales']:,.2f}

Category with highest profit margin: {highest_margin}
Margin: {category_analysis.loc[highest_margin, 'Profit_Margin']:.2f}%

Category with lowest profit margin: {lowest_margin}
Margin: {category_analysis.loc[lowest_margin, 'Profit_Margin']:.2f}%

LOSS-MAKING SUBCATEGORIES:
{loss_details}

COMPLETE CATEGORY ANALYSIS:
{category_table}

COMPLETE SUBCATEGORY ANALYSIS:
{subcategory_table}

IMPORTANT RULES:

1. Treat all supplied numerical values and verified findings as correct.
2. Technology has the highest sales, if confirmed by the supplied findings.
3. Never assign one category's sales or profit to another category.
4. Do not recalculate supplied metrics.
5. Do not invent facts or causes.
6. Negative aggregate profit does not mean every transaction is loss-making.
7. Do not describe average order value as stable without historical comparison.
8. Present recommendations as areas to investigate, not confirmed causes.
9. Distinguish observations from possible explanations.
10. Avoid repeating the same information.

Write a professional business report using exactly these sections:

1. Executive Summary
2. Key Business Findings
3. Areas of Concern
4. Three Practical Business Recommendations

Use simple professional English.
Keep the report approximately 150-200 words.
Complete all four sections.
"""

    return prompt
