
def create_business_analysis_prompt(
    kpi_summary,
    category_analysis,
    subcategory_analysis
):
    # Convert KPI results into readable text
    kpi_text = "\n".join(
        f"{key}: {value}"
        for key, value in kpi_summary.items()
    )

    # Convert grouped analysis into readable tables
    category_table = category_analysis.round(2).to_string()

    subcategory_table = subcategory_analysis.round(2).to_string()

    prompt = f"""
You are an experienced Business Data Analyst.

Analyze the following retail business data.

BUSINESS KPIs:
{kpi_text}

CATEGORY ANALYSIS:
{category_table}

SUBCATEGORY ANALYSIS:
{subcategory_table}

Your tasks:

1. Summarize the overall business performance.
2. Identify the highest-performing category.
3. Identify the lowest-performing category.
4. Identify loss-making subcategories.
5. Explain important business patterns.
6. Provide five practical business recommendations.

Guidelines:
- Use only the information provided.
- Support findings with actual numbers.
- Use simple, professional English.
- Do not invent facts or assume causes.
- Clearly distinguish observations from possible explanations.
- Avoid repeating the same finding.

Format your response using these sections:

1. Executive Summary
2. Key Business Findings
3. Areas of Concern
4. Business Recommendations
"""

    return prompt
