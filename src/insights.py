"""
Business Insights and Executive Summary Engine
Generates automated, data-driven analytical observations and strategic
recommendations for academic evaluation and executive decision-making.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np

def generate_business_insights(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyzes the filtered dataset and generates synthesized executive findings,
    financial highlights, and operational recommendations.
    
    Returns:
        dict: Structured insights, key highlights, and recommendations.
    """
    if df.empty:
        return {
            "summary_statement": "No records match the selected filter criteria.",
            "highlights": [],
            "risk_factors": [],
            "recommendations": []
        }

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    margin = (total_profit / total_sales * 100) if total_sales > 0 else 0.0

    # 1. Best Category by Sales & Margin
    cat_summary = df.groupby("Category").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    ).reset_index()
    cat_summary["Margin"] = (cat_summary["Profit"] / cat_summary["Sales"] * 100).round(1)
    
    top_sales_cat = cat_summary.sort_values(by="Sales", ascending=False).iloc[0]
    top_margin_cat = cat_summary.sort_values(by="Margin", ascending=False).iloc[0]

    # 2. Regional Analysis
    reg_summary = df.groupby("Region").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    ).reset_index()
    reg_summary["Margin"] = (reg_summary["Profit"] / reg_summary["Sales"] * 100).round(1)
    
    top_reg = reg_summary.sort_values(by="Sales", ascending=False).iloc[0]
    lowest_reg = reg_summary.sort_values(by="Sales", ascending=True).iloc[0]

    # 3. Top Sales Representative
    rep_summary = df.groupby("Salesperson").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    ).reset_index()
    top_rep = rep_summary.sort_values(by="Sales", ascending=False).iloc[0]

    # 4. Top Product
    prod_summary = df.groupby("Product").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    ).reset_index()
    top_prod = prod_summary.sort_values(by="Sales", ascending=False).iloc[0]

    # 5. Temporal Peak Month
    monthly = df.groupby("YearMonth")["Sales"].sum().reset_index()
    peak_month = monthly.sort_values(by="Sales", ascending=False).iloc[0]

    # 6. Unprofitable Transactions / Risk Flags
    loss_orders = df[df["Profit"] < 0]
    loss_count = len(loss_orders)
    loss_amount = abs(loss_orders["Profit"].sum()) if loss_count > 0 else 0.0
    loss_pct = (loss_count / len(df) * 100)

    # Compile structured highlights
    highlights = [
        {
            "icon": "📈",
            "title": "Revenue Engine",
            "detail": f"<b>{top_sales_cat['Category']}</b> dominates gross revenue with <b>${top_sales_cat['Sales']:,.2f}</b> ({(top_sales_cat['Sales']/total_sales*100):.1f}% of total turnover)."
        },
        {
            "icon": "💎",
            "title": "Profitability Champion",
            "detail": f"<b>{top_margin_cat['Category']}</b> boasts the highest profit margin at <b>{top_margin_cat['Margin']}%</b>, delivering strong margin returns."
        },
        {
            "icon": "🌍",
            "title": "Geographic Stronghold",
            "detail": f"The <b>{top_reg['Region']}</b> territory spearheads sales with <b>${top_reg['Sales']:,.2f}</b>, operating at an average margin of <b>{top_reg['Margin']}%</b>."
        },
        {
            "icon": "⭐",
            "title": "Top Sales Representative",
            "detail": f"<b>{top_rep['Salesperson']}</b> closed <b>{top_rep['Orders']}</b> orders, generating <b>${top_rep['Sales']:,.2f}</b> in revenue."
        },
        {
            "icon": "🏆",
            "title": "Flagship Offering",
            "detail": f"<b>{top_prod['Product']}</b> is the highest revenue contributor, yielding <b>${top_prod['Sales']:,.2f}</b> total revenue."
        },
        {
            "icon": "📅",
            "title": "Peak Trading Period",
            "detail": f"<b>{peak_month['YearMonth']}</b> recorded the highest sales volume at <b>${peak_month['Sales']:,.2f}</b>."
        }
    ]

    # Compile operational risk factors
    risk_factors = []
    if loss_count > 0:
        risk_factors.append(
            f"Detected <b>{loss_count}</b> unprofitable transactions ({loss_pct:.1f}% of volume), incurring a cumulative margin drag of <b>${loss_amount:,.2f}</b> due to steep discounting."
        )
    if lowest_reg['Sales'] < (total_sales * 0.12):
        risk_factors.append(
            f"The <b>{lowest_reg['Region']}</b> region contributes under 12% (${lowest_reg['Sales']:,.2f}) of total sales, indicating potential under-penetration."
        )

    # Strategic Recommendations
    recommendations = [
        f"<b>Scale High-Margin Portfolio:</b> Accelerate bundle promotions for {top_margin_cat['Category']} products to boost blended operating margin.",
        f"<b>Territory Expansion in {lowest_reg['Region']}:</b> Allocate dedicated sales quotas and regional marketing to elevate {lowest_reg['Region']} revenue.",
        "<b>Discount Governance:</b> Implement approval thresholds on custom order discounting to eliminate negative margin transactions.",
        f"<b>Replicate Top Performer Strategies:</b> Host internal sales enablement workshops led by {top_rep['Salesperson']} to standardize closing best practices."
    ]

    summary_statement = (
        f"The organization generated <b>${total_sales:,.2f}</b> in gross sales and <b>${total_profit:,.2f}</b> in net profit, "
        f"achieving a healthy overall operating margin of <b>{margin:.1f}%</b> across {len(df):,} processed orders."
    )

    return {
        "summary_statement": summary_statement,
        "highlights": highlights,
        "risk_factors": risk_factors,
        "recommendations": recommendations,
        "metrics": {
            "top_category": top_sales_cat['Category'],
            "top_region": top_reg['Region'],
            "top_salesperson": top_rep['Salesperson'],
            "top_product": top_prod['Product'],
            "peak_month": peak_month['YearMonth'],
            "loss_orders": loss_count
        }
    }
