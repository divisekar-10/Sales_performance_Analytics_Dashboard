"""
Automated Test Suite for Sales Performance Analytics Dashboard
Validates data ingestion, preprocessing, KPI algorithms, chart generators,
and business insights modules.
"""

import sys
import unittest
import pandas as pd
import numpy as np

from src.data_loader import load_sales_data, filter_dataset
from src.metrics import (
    calculate_kpis,
    get_monthly_aggregation,
    get_regional_aggregation,
    get_category_aggregation,
    get_top_performers
)
from src.charts import (
    plot_monthly_sales_trend,
    plot_monthly_profit_trend,
    plot_sales_vs_profit_monthly,
    plot_sales_by_region,
    plot_profit_by_region,
    plot_sales_by_category,
    plot_top_products,
    plot_top_salespersons,
    plot_sales_vs_profit_scatter,
    plot_order_size_distribution
)
from src.insights import generate_business_insights

class TestSalesAnalyticsDashboard(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Loads and prepares test data once for all test methods."""
        cls.df = load_sales_data()

    def test_01_dataset_integrity(self):
        """Verify that the dataset is loaded properly with all required fields."""
        required_columns = [
            "Order ID", "Order Date", "Product", "Category", "Region",
            "Salesperson", "Customer", "Quantity", "Unit Price",
            "Sales", "Cost", "Profit", "Profit Margin"
        ]
        for col in required_columns:
            self.assertIn(col, self.df.columns, f"Missing required column: {col}")
        
        self.assertGreater(len(self.df), 1000, "Dataset contains fewer records than expected.")
        self.assertFalse(self.df["Sales"].isnull().any(), "Sales column contains null values.")
        self.assertFalse(self.df["Profit"].isnull().any(), "Profit column contains null values.")
        print("[PASS] Test 01 Passed: Dataset integrity and schema validated.")

    def test_02_derived_features(self):
        """Verify that feature engineering correctly adds temporal and tier fields."""
        derived_cols = ["Year", "Month", "YearMonth", "Quarter", "DayOfWeek", "IsProfitable", "OrderSizeTier"]
        for col in derived_cols:
            self.assertIn(col, self.df.columns, f"Missing derived column: {col}")
        print("[PASS] Test 02 Passed: Derived features validated.")

    def test_03_kpi_calculations(self):
        """Verify mathematical formulas for KPIs."""
        kpis = calculate_kpis(self.df)
        
        # Check Total Sales = sum of sales
        expected_sales = self.df["Sales"].sum()
        self.assertAlmostEqual(kpis["total_sales"], expected_sales, places=2)

        # Check Total Profit = sum of profit
        expected_profit = self.df["Profit"].sum()
        self.assertAlmostEqual(kpis["total_profit"], expected_profit, places=2)

        # Check Profit Margin = (Profit / Sales) * 100
        expected_margin = (expected_profit / expected_sales) * 100.0
        self.assertAlmostEqual(kpis["profit_margin"], expected_margin, places=2)

        # Check Average Order Value = Sales / Orders
        expected_aov = expected_sales / self.df["Order ID"].nunique()
        self.assertAlmostEqual(kpis["avg_order_value"], expected_aov, places=2)

        # Check Total Quantity
        self.assertEqual(kpis["total_quantity"], int(self.df["Quantity"].sum()))
        print("[PASS] Test 03 Passed: All KPI mathematical formulas validated.")

    def test_04_filtering_logic(self):
        """Verify multi-criteria filtering accuracy."""
        # Test regional filter
        region_test = ["East", "West"]
        filtered = filter_dataset(self.df, regions=region_test)
        self.assertTrue(set(filtered["Region"].unique()).issubset(set(region_test)))

        # Test category filter
        cat_test = ["Technology"]
        filtered_cat = filter_dataset(self.df, categories=cat_test)
        self.assertEqual(list(filtered_cat["Category"].unique()), ["Technology"])

        # Test date range filter
        start = "2024-06-01"
        end = "2024-12-31"
        filtered_date = filter_dataset(self.df, start_date=start, end_date=end)
        self.assertTrue((filtered_date["Order Date"] >= pd.to_datetime(start)).all())
        self.assertTrue((filtered_date["Order Date"] <= pd.to_datetime(end)).all())
        print("[PASS] Test 04 Passed: Dynamic filtering logic validated.")

    def test_05_aggregations(self):
        """Verify monthly, regional, category, and performer aggregation tables."""
        monthly = get_monthly_aggregation(self.df)
        self.assertFalse(monthly.empty)
        self.assertIn("YearMonth", monthly.columns)
        self.assertIn("MoM_Sales_Growth", monthly.columns)

        regional = get_regional_aggregation(self.df)
        self.assertEqual(len(regional), self.df["Region"].nunique())

        category = get_category_aggregation(self.df)
        self.assertEqual(len(category), self.df["Category"].nunique())

        top_products = get_top_performers(self.df, "Product", top_n=5)
        self.assertEqual(len(top_products), 5)
        print("[PASS] Test 05 Passed: Metric aggregations validated.")

    def test_06_chart_generators(self):
        """Verify all Plotly figure generation functions execute without error."""
        monthly = get_monthly_aggregation(self.df)
        regional = get_regional_aggregation(self.df)
        category = get_category_aggregation(self.df)
        top_products = get_top_performers(self.df, "Product", top_n=5)
        top_reps = get_top_performers(self.df, "Salesperson", top_n=5)

        charts = [
            plot_monthly_sales_trend(monthly),
            plot_monthly_profit_trend(monthly),
            plot_sales_vs_profit_monthly(monthly),
            plot_sales_by_region(regional),
            plot_profit_by_region(regional),
            plot_sales_by_category(category),
            plot_top_products(top_products),
            plot_top_salespersons(top_reps),
            plot_sales_vs_profit_scatter(self.df),
            plot_order_size_distribution(self.df)
        ]

        for chart in charts:
            self.assertIsNotNone(chart)
            # Ensure figure object is valid
            self.assertTrue(hasattr(chart, "data"))
        print("[PASS] Test 06 Passed: All 10 Plotly chart rendering pipelines validated.")

    def test_07_insights_generation(self):
        """Verify that executive insights and risk recommendations generate accurately."""
        insights = generate_business_insights(self.df)
        self.assertIn("summary_statement", insights)
        self.assertIn("highlights", insights)
        self.assertIn("risk_factors", insights)
        self.assertIn("recommendations", insights)
        self.assertGreater(len(insights["highlights"]), 0)
        self.assertGreater(len(insights["recommendations"]), 0)
        print("[PASS] Test 07 Passed: Automated business insights engine validated.")

    def test_08_empty_filter_safety(self):
        """Verify graceful error-handling when no data matches filters."""
        empty_df = pd.DataFrame()
        empty_kpis = calculate_kpis(empty_df)
        self.assertEqual(empty_kpis["total_sales"], 0.0)
        self.assertEqual(empty_kpis["total_orders"], 0)

        empty_insights = generate_business_insights(empty_df)
        self.assertIn("No records match", empty_insights["summary_statement"])
        print("[PASS] Test 08 Passed: Graceful empty-filter safety validated.")

if __name__ == "__main__":
    unittest.main(verbosity=2)
