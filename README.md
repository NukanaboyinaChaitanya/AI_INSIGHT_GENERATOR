# AI-Powered Automated Business Insight Generator

A Python-based retail analytics application that turns an Excel sales dataset into business KPIs, visual reports, rule-based findings, and AI-generated explanations in plain English.

The application uses **Pandas** for data processing, **Plotly** for charts, **Streamlit** for the dashboard, and a locally running **Qwen 3.5 4B** model through **Ollama** to write business narratives from the analysis results.

## What the project does

1. Loads retail order data from the provided Excel workbook.
2. Cleans the data before analysis.
3. Calculates key business metrics, including total sales, total profit, unique orders, unique customers, quantity sold, profit margin, and average order value.
4. Aggregates sales and profit by category and subcategory.
5. Displays business performance through a Streamlit dashboard and Plotly charts.
6. Generates rule-based findings and recommendations from the calculated results.
7. Sends a structured prompt containing the analysis to a local Qwen model and displays its plain-English business report.
8. Shows a before-and-after view: numerical analysis alongside the AI-generated explanation.

## Dashboard features

- **KPI metrics:** sales, profit, orders, customers, quantity, profit margin, and average order value.
- **Monthly sales trend:** monthly sales totals over time.
- **Sales by category:** comparison of Furniture, Office Supplies, and Technology.
- **Profit by subcategory:** identifies subcategories with positive and negative profit.
- **Business insights and recommendations:** generated from Python analysis rules.
- **AI Business Analyst:** produces an executive summary, key findings, areas of concern, and practical recommendations using Qwen.
- **Before-and-after comparison:** displays the numerical category and subcategory analysis next to the AI-generated narrative.

## Technology stack

- Python
- Pandas
- Streamlit
- Plotly
- Requests
- Ollama
- Qwen 3.5 4B
- Excel (`.xls`) input data

## Project structure

```text
AI_INSIGHT_GENERATOR/
├── data/
│   └── sample_-_superstore.xls
├── notebooks/
│   └── 01_data_understanding.ipynb
├── reports/
├── src/
│   ├── data_processor.py
│   ├── business_insights.py
│   ├── business_recommendations.py
│   ├── ai_prompt_template.py
│   ├── ai_generator.py
│   └── main.py
├── dashboard.py
├── README.md
└── .gitignore
```

The `venv/` virtual environment is created locally and should not be committed to GitHub.

## Getting started (Windows)

### 1. Clone the repository

```powershell
git clone https://github.com/NukanaboyinaChaitanya/AI_INSIGHT_GENERATOR.git
cd AI_INSIGHT_GENERATOR
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install Python dependencies

```powershell
pip install pandas xlrd streamlit plotly requests
```

### 4. Install and prepare Ollama

Install Ollama for Windows from [ollama.com/download](https://ollama.com/download).

Download the model used by this project:

```powershell
ollama pull qwen3.5:4b
```

Ollama must be running locally before you request an AI report. The application sends requests to Ollama's local chat endpoint at `http://localhost:11434/api/chat`.

You can check that the model is available with:

```powershell
ollama list
```

### 5. Run the Streamlit dashboard

From the project root, with the virtual environment activated and Ollama running:

```powershell
streamlit run dashboard.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser. Use **Generate AI Business Report** in the dashboard to create the narrative report.

## How the AI feature works

Python calculates the KPIs and grouped business results. The prompt-template module prepares those findings as context for Qwen. The local model then explains the supplied findings in natural language.

**Important:** Python/Pandas is the source of truth for numerical calculations. The language model is used to explain the results, not to calculate or verify financial metrics. AI-generated text can still contain mistakes, so review its statements against the tables and KPIs before using the report for decisions or presentations.

## Data notes

- The project uses the sample Superstore Excel workbook included in `data/`.
- The analysis is based on the workbook's `Orders` sheet.
- Cleaning and date-filtering rules are implemented in `src/data_processor.py`.
- This is a sample dataset for demonstrating an analytics workflow; it is not live company data.

## GitHub and credential safety

This project uses a local Ollama model and does not require an OpenAI API key for the dashboard's AI-report feature.

Do not commit any API keys, `.env` files, virtual environments, or Python cache folders. A suitable `.gitignore` includes:

```gitignore
.env
.env.*
!.env.example
venv/
.venv/
__pycache__/
*.py[cod]
.ipynb_checkpoints/
```

## Possible future improvements

- Add dashboard filters for date, region, and category.
- Add automated validation checks for AI-generated statements.
- Allow users to upload a different compatible sales workbook.
- Export the business report to PDF or CSV.

---

**Project:** AI-Powered Automated Business Insight Generator  
**Interface:** Streamlit  
**Local language model:** Qwen 3.5 4B via Ollama
