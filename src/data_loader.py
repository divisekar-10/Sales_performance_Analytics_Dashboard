"""
Data Loading, Cleaning, and Preprocessing Module
Handles CSV ingestion, data validation, type conversion, missing value management,
and feature engineering for the Sales Performance Analytics Dashboard.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sales_data.csv")

def ensure_dataset_exists(filepath=DATA_PATH):
    """
    Ensures that the sales dataset exists; generates it if missing.
    """
    if not os.path.exists(filepath):
        from data.generate_dataset import generate_sales_data
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        generate_sales_data(output_path=filepath)
    return filepath

def load_sales_data(filepath=DATA_PATH) -> pd.DataFrame:
    """
    Loads raw sales dataset from CSV, performs preprocessing, data validation,
    type casting, and feature engineering.
    
    Returns:
        pd.DataFrame: Cleaned and feature-enriched sales dataframe.
    """
    resolved_path = ensure_dataset_exists(filepath)
    df = pd.read_csv(resolved_path)

    # 1. Strip whitespace from string columns
    str_cols = ["Order ID", "Product", "Category", "Region", "Salesperson", "Customer"]
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # 2. Date parsing and validation
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    # Drop records with invalid dates if any
    df = df.dropna(subset=["Order Date"]).copy()

    # 3. Numeric type casting and validation
    numeric_cols = ["Quantity", "Unit Price", "Sales", "Cost", "Profit", "Profit Margin"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fill any null values with median / reasonable defaults
    if df["Quantity"].isnull().any():
        df["Quantity"] = df["Quantity"].fillna(1).astype(int)
    else:
        df["Quantity"] = df["Quantity"].astype(int)

    if df["Sales"].isnull().any():
        df["Sales"] = (df["Quantity"] * df["Unit Price"]).round(2)

    if df["Cost"].isnull().any():
        df["Cost"] = (df["Sales"] - df["Profit"]).round(2)

    if df["Profit"].isnull().any():
        df["Profit"] = (df["Sales"] - df["Cost"]).round(2)

    if df["Profit Margin"].isnull().any():
        df["Profit Margin"] = np.where(df["Sales"] > 0, ((df["Profit"] / df["Sales"]) * 100).round(2), 0.0)

    # 4. Feature Engineering
    # Temporal attributes
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.strftime("%b")
    df["Month_Num"] = df["Order Date"].dt.month
    df["YearMonth"] = df["Order Date"].dt.strftime("%Y-%m")
    df["Quarter"] = df["Order Date"].dt.to_period("Q").astype(str)
    df["DayOfWeek"] = df["Order Date"].dt.day_name()
    df["IsWeekend"] = df["Order Date"].dt.dayofweek.isin([5, 6]).astype(int)

    # Profitability flag
    df["IsProfitable"] = df["Profit"] >= 0

    # Order Size Categorization
    bins = [0, 500, 2000, 5000, np.inf]
    labels = ["Small (<$500)", "Medium ($500-$2K)", "Large ($2K-$5K)", "Enterprise (>$5K)"]
    df["OrderSizeTier"] = pd.cut(df["Sales"], bins=bins, labels=labels, right=False)

    # Chronological sort
    df = df.sort_values(by="Order Date").reset_index(drop=True)

    return df

def filter_dataset(
    df: pd.DataFrame,
    start_date=None,
    end_date=None,
    regions=None,
    categories=None,
    products=None,
    salespersons=None
) -> pd.DataFrame:
    """
    Applies multi-criteria filtering to the sales dataset.
    
    Args:
        df: Input DataFrame
        start_date: Starting date (inclusive)
        end_date: Ending date (inclusive)
        regions: List of selected regions (None or empty means all)
        categories: List of selected categories
        products: List of selected products
        salespersons: List of selected salespersons
        
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    filtered = df.copy()

    # Date range filter
    if start_date is not None:
        start_ts = pd.to_datetime(start_date)
        filtered = filtered[filtered["Order Date"] >= start_ts]

    if end_date is not None:
        end_ts = pd.to_datetime(end_date)
        filtered = filtered[filtered["Order Date"] <= end_ts]

    # Categorical filters
    if regions:
        filtered = filtered[filtered["Region"].isin(regions)]

    if categories:
        filtered = filtered[filtered["Category"].isin(categories)]

    if products:
        filtered = filtered[filtered["Product"].isin(products)]

    if salespersons:
        filtered = filtered[filtered["Salesperson"].isin(salespersons)]

    return filtered

if __name__ == "__main__":
    test_df = load_sales_data()
    print("Dataset loaded successfully.")
    print("Shape:", test_df.shape)
    print("Columns:", list(test_df.columns))
    print(test_df.head(2))
