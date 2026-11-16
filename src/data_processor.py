
import pandas as pd


def load_excel_data(file_path):
    """
    Load the Orders sheet from an Excel workbook.
    """

    try:
        orders = pd.read_excel(
            file_path,
            sheet_name="Orders"
        )

        print("Excel file loaded successfully!")
        print("Dataset shape:", orders.shape)

        return orders

    except Exception as e:
        raise ValueError(f"Error loading Excel file: {e}")


def clean_data(orders):
    """
    Perform basic data cleaning and validation.
    """

    df = orders.copy()

    # Standardize column names
    df.columns = df.columns.str.strip()

    # Convert date column
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    # Remove rows with invalid essential values
    required_columns = [
        "Order ID",
        "Order Date",
        "Customer ID",
        "Sales",
        "Profit",
        "Quantity",
        "Category",
        "Sub-Category"
    ]

    df = df.dropna(subset=required_columns)

    # Exclude future-dated records
    cutoff_date = pd.Timestamp("2026-11-16")

    df = df[df["Order Date"] <= cutoff_date].copy()

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    print("Data cleaning completed!")
    print("Cleaned dataset shape:", df.shape)

    return df


def calculate_kpis(df):
    """
    Calculate overall business KPIs.
    """

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order ID"].nunique()
    total_customers = df["Customer ID"].nunique()
    total_quantity = df["Quantity"].sum()

    profit_margin = (
        total_profit / total_sales * 100
        if total_sales != 0 else 0
    )

    average_order_value = (
        total_sales / total_orders
        if total_orders != 0 else 0
    )

    kpi_summary = {
        "Total Sales": round(float(total_sales), 2),
        "Total Profit": round(float(total_profit), 2),
        "Total Orders": int(total_orders),
        "Total Customers": int(total_customers),
        "Total Quantity": int(total_quantity),
        "Profit Margin": round(float(profit_margin), 2),
        "Average Order Value": round(
            float(average_order_value), 2
        )
    }

    return kpi_summary


def calculate_category_analysis(df):
    """
    Calculate category-level performance.
    """

    category_analysis = (
        df.groupby("Category")
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Orders=("Order ID", "nunique")
        )
    )

    category_analysis["Profit_Margin"] = (
        category_analysis["Total_Profit"]
        / category_analysis["Total_Sales"].replace(0, pd.NA)
    ) * 100

    return category_analysis


def calculate_subcategory_analysis(df):
    """
    Calculate subcategory-level performance.
    """

    subcategory_analysis = (
        df.groupby("Sub-Category")
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Orders=("Order ID", "nunique")
        )
    )

    subcategory_analysis["Profit_Margin"] = (
        subcategory_analysis["Total_Profit"]
        / subcategory_analysis["Total_Sales"].replace(0, pd.NA)
    ) * 100

    return subcategory_analysis
