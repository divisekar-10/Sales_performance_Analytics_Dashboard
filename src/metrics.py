"""
KPI and Metric Calculations Module
Provides standardized business logic and mathematical formulas for computing
sales performance metrics, profitability margins, and growth indicators.
"""

from typing import Dict, Any
import pandas as pd
import numpy as np

def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes key performance indicators (KPIs) from the sales dataframe.
    
    Formulas:
    1. Total Sales = SUM(Sales)
    2. Total Profit = SUM(Profit)
    3. Profit Margin (%) = (Total Profit / Total Sales) * 100
    4. Total Orders = COUNT(DISTINCT Order ID)
    5. Total Quantity = SUM(Quantity)
    6. Average Order Value (AOV) = Total Sales / Total Orders
    7. Average Profit Per Order = Total Profit / Total Orders
    8. Unprofitable Orders Count = COUNT(Orders where Profit < 0)
    
    Returns:
        dict: Formatted KPI values and raw numerical metrics.
    """
    if df.empty:
        return {
            "total_sales": 0.0,
            "total_profit": 0.0,
            "profit_margin": 0.0,
            "total_orders": 0,
            "total_quantity": 0,
            "avg_order_value": 0.0,
            "avg_profit_per_order": 0.0,
            "unprofitable_orders": 0,
            "unprofitable_pct": 0.0,
            # Formatted strings
            "fmt_total_sales": "$0.00",
            "fmt_total_profit": "$0.00",
            "fmt_profit_margin": "0.0%",
            "fmt_total_orders": "0",
            "fmt_total_quantity": "0",
            "fmt_avg_order_value": "$0.00",
            "fmt_avg_profit_per_order": "$0.00",
        }

    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())
    total_orders = int(df["Order ID"].nunique())
    total_quantity = int(df["Quantity"].sum())

    # Overall weighted profit margin
    profit_margin = (total_profit / total_sales * 100.0) if total_sales > 0 else 0.0

    # Average Order Value (AOV)
    avg_order_value = (total_sales / total_orders) if total_orders > 0 else 0.0

    # Average Profit Per Order
    avg_profit_per_order = (total_profit / total_orders) if total_orders > 0 else 0.0

    # Unprofitable orders check
    unprofitable_mask = df["Profit"] < 0
    unprofitable_orders = int(unprofitable_mask.sum())
    unprofitable_pct = (unprofitable_orders / len(df) * 100.0) if len(df) > 0 else 0.0

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "profit_margin": profit_margin,
        "total_orders": total_orders,
        "total_quantity": total_quantity,
        "avg_order_value": avg_order_value,
        "avg_profit_per_order": avg_profit_per_order,
        "unprofitable_orders": unprofitable_orders,
        "unprofitable_pct": unprofitable_pct,
        # Academic & Executive display formatting
        "fmt_total_sales": f"${total_sales:,.2f}",
        "fmt_total_profit": f"${total_profit:,.2f}",
        "fmt_profit_margin": f"{profit_margin:.1f}%",
        "fmt_total_orders": f"{total_orders:,}",
        "fmt_total_quantity": f"{total_quantity:,}",
        "fmt_avg_order_value": f"${avg_order_value:,.2f}",
        "fmt_avg_profit_per_order": f"${avg_profit_per_order:,.2f}",
    }

def get_monthly_aggregation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates sales and profit by Year-Month for trend analysis.
    """
    if df.empty:
        return pd.DataFrame(columns=["YearMonth", "Sales", "Profit", "Orders", "Profit Margin", "MoM_Sales_Growth"])

    monthly = df.groupby("YearMonth").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum")
    ).reset_index()

    monthly["Profit Margin"] = np.where(
        monthly["Sales"] > 0,
        (monthly["Profit"] / monthly["Sales"] * 100.0).round(2),
        0.0
    )
    monthly["MoM_Sales_Growth"] = monthly["Sales"].pct_change() * 100.0
    monthly["MoM_Sales_Growth"] = monthly["MoM_Sales_Growth"].round(1)

    return monthly

def get_regional_aggregation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates performance by geographic Region.
    """
    if df.empty:
        return pd.DataFrame()

    regional = df.groupby("Region").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum")
    ).reset_index()

    regional["Profit Margin"] = (regional["Profit"] / regional["Sales"] * 100.0).round(2)
    regional["Avg_Order_Value"] = (regional["Sales"] / regional["Orders"]).round(2)
    return regional.sort_values(by="Sales", ascending=False).reset_index(drop=True)

def get_category_aggregation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates performance by Category.
    """
    if df.empty:
        return pd.DataFrame()

    cat_df = df.groupby("Category").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum")
    ).reset_index()

    cat_df["Profit Margin"] = (cat_df["Profit"] / cat_df["Sales"] * 100.0).round(2)
    cat_df["Sales_Share_Pct"] = (cat_df["Sales"] / cat_df["Sales"].sum() * 100.0).round(2)
    return cat_df.sort_values(by="Sales", ascending=False).reset_index(drop=True)

def get_top_performers(df: pd.DataFrame, entity_col="Product", top_n=10) -> pd.DataFrame:
    """
    Ranks top performing entities (Products or Salespersons).
    """
    if df.empty:
        return pd.DataFrame()

    ranked = df.groupby(entity_col).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum")
    ).reset_index()

    ranked["Profit Margin"] = (ranked["Profit"] / ranked["Sales"] * 100.0).round(2)
    ranked["Avg_Order_Value"] = (ranked["Sales"] / ranked["Orders"]).round(2)
    return ranked.sort_values(by="Sales", ascending=False).head(top_n).reset_index(drop=True)
