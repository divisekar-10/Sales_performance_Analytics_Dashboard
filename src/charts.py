"""
Interactive Data Visualization Module
Builds responsive, presentation-ready Plotly charts for the
Sales Performance Analytics Dashboard.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Professional Academic / Corporate Color Palette
THEME = {
    "primary": "#1E88E5",      # Royal Blue for Sales
    "secondary": "#00897B",    # Teal Green for Profit
    "accent": "#FB8C00",       # Amber Orange
    "neutral": "#546E7A",      # Slate Grey
    "danger": "#E53935",       # Crimson Red for losses
    "background": "rgba(0,0,0,0)",
    "grid": "rgba(180, 190, 205, 0.2)",
    "font_family": "Segoe UI, Inter, sans-serif"
}

def _apply_standard_layout(fig, title: str, x_title: str, y_title: str):
    """Applies clean academic styling and typography to Plotly figures."""
    fig.update_layout(
        title={
            "text": f"<b>{title}</b>",
            "x": 0.02,
            "xanchor": "left",
            "font": {"size": 16, "family": THEME["font_family"], "color": "#1A202C"}
        },
        xaxis={
            "title": f"<b>{x_title}</b>",
            "showgrid": True,
            "gridcolor": THEME["grid"],
            "linecolor": "#CBD5E1"
        },
        yaxis={
            "title": f"<b>{y_title}</b>",
            "showgrid": True,
            "gridcolor": THEME["grid"],
            "linecolor": "#CBD5E1"
        },
        plot_bgcolor=THEME["background"],
        paper_bgcolor=THEME["background"],
        font={"family": THEME["font_family"], "color": "#334155", "size": 12},
        margin=dict(l=45, r=30, t=55, b=45),
        hoverlabel=dict(bgcolor="#1E293B", font_size=12, font_color="#FFFFFF")
    )
    return fig

def plot_monthly_sales_trend(monthly_df: pd.DataFrame):
    """
    Renders an interactive monthly sales line & area chart.
    """
    if monthly_df.empty:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_df["YearMonth"],
        y=monthly_df["Sales"],
        mode="lines+markers",
        name="Sales ($)",
        line=dict(color=THEME["primary"], width=3),
        marker=dict(size=7, color=THEME["primary"]),
        fill="tozeroy",
        fillcolor="rgba(30, 136, 229, 0.08)",
        hovertemplate="<b>Month</b>: %{x}<br><b>Sales</b>: $%{y:,.2f}<extra></extra>"
    ))

    # Add average line
    avg_sales = monthly_df["Sales"].mean()
    fig.add_hline(
        y=avg_sales,
        line_dash="dot",
        line_color=THEME["neutral"],
        annotation_text=f"Avg: ${avg_sales:,.0f}",
        annotation_position="bottom right"
    )

    _apply_standard_layout(fig, "Monthly Sales Trend Over Time", "Timeline (Year-Month)", "Total Sales ($)")
    return fig

def plot_monthly_profit_trend(monthly_df: pd.DataFrame):
    """
    Renders an interactive monthly profit line & area chart.
    """
    if monthly_df.empty:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_df["YearMonth"],
        y=monthly_df["Profit"],
        mode="lines+markers",
        name="Profit ($)",
        line=dict(color=THEME["secondary"], width=3),
        marker=dict(size=7, color=THEME["secondary"]),
        fill="tozeroy",
        fillcolor="rgba(0, 137, 123, 0.10)",
        hovertemplate="<b>Month</b>: %{x}<br><b>Profit</b>: $%{y:,.2f}<extra></extra>"
    ))

    avg_profit = monthly_df["Profit"].mean()
    fig.add_hline(
        y=avg_profit,
        line_dash="dot",
        line_color=THEME["neutral"],
        annotation_text=f"Avg: ${avg_profit:,.0f}",
        annotation_position="bottom right"
    )

    _apply_standard_layout(fig, "Monthly Profit Trend Over Time", "Timeline (Year-Month)", "Total Profit ($)")
    return fig

def plot_sales_vs_profit_monthly(monthly_df: pd.DataFrame):
    """
    Combined Monthly Sales vs. Profit Dual Bar and Line Chart.
    """
    if monthly_df.empty:
        return go.Figure()

    fig = go.Figure()
    # Bar for Sales
    fig.add_trace(go.Bar(
        x=monthly_df["YearMonth"],
        y=monthly_df["Sales"],
        name="Total Sales",
        marker_color="#90CAF9",
        hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>"
    ))
    # Bar for Profit
    fig.add_trace(go.Bar(
        x=monthly_df["YearMonth"],
        y=monthly_df["Profit"],
        name="Net Profit",
        marker_color=THEME["secondary"],
        hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.2f}<extra></extra>"
    ))
    # Line for Margin % (Secondary Y Axis)
    fig.add_trace(go.Scatter(
        x=monthly_df["YearMonth"],
        y=monthly_df["Profit Margin"],
        name="Margin (%)",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color=THEME["accent"], width=2.5),
        hovertemplate="<b>%{x}</b><br>Margin: %{y:.1f}%<extra></extra>"
    ))

    fig.update_layout(
        barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis2=dict(
            title="<b>Profit Margin (%)</b>",
            overlaying="y",
            side="right",
            showgrid=False,
            ticksuffix="%"
        )
    )
    _apply_standard_layout(fig, "Monthly Sales vs. Net Profit Comparison with Margin (%)", "Timeline (Year-Month)", "Amount ($)")
    return fig

def plot_sales_by_region(regional_df: pd.DataFrame):
    """
    Bar chart showing total sales across geographic regions.
    """
    if regional_df.empty:
        return go.Figure()

    fig = px.bar(
        regional_df,
        x="Region",
        y="Sales",
        text="Sales",
        color="Sales",
        color_continuous_scale="Blues",
        labels={"Sales": "Sales ($)", "Region": "Geographic Region"}
    )
    fig.update_traces(
        texttemplate="$%{text:,.2s}",
        textposition="outside",
        hovertemplate="<b>Region: %{x}</b><br>Sales: $%{y:,.2f}<extra></extra>"
    )
    fig.update_layout(coloraxis_showscale=False)
    _apply_standard_layout(fig, "Total Sales by Geographic Region", "Region", "Sales ($)")
    return fig

def plot_profit_by_region(regional_df: pd.DataFrame):
    """
    Bar chart showing net profit by region with margin annotations.
    """
    if regional_df.empty:
        return go.Figure()

    fig = px.bar(
        regional_df,
        x="Region",
        y="Profit",
        text="Profit Margin",
        color="Profit Margin",
        color_continuous_scale="Teal",
        labels={"Profit": "Profit ($)", "Profit Margin": "Margin (%)"}
    )
    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate="<b>Region: %{x}</b><br>Profit: $%{y:,.2f}<extra></extra>"
    )
    _apply_standard_layout(fig, "Net Profit & Margin (%) by Region", "Region", "Profit ($)")
    return fig

def plot_sales_by_category(category_df: pd.DataFrame):
    """
    Donut chart of sales distribution across categories.
    """
    if category_df.empty:
        return go.Figure()

    fig = px.pie(
        category_df,
        names="Category",
        values="Sales",
        hole=0.45,
        color_discrete_sequence=["#1E88E5", "#00897B", "#FB8C00", "#8E24AA", "#3949AB"]
    )
    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>Category: %{label}</b><br>Sales: $%{value:,.2f}<br>Share: %{percent}<extra></extra>"
    )
    fig.update_layout(
        title={
            "text": "<b>Sales Share by Product Category</b>",
            "x": 0.02,
            "xanchor": "left",
            "font": {"size": 16, "family": THEME["font_family"], "color": "#1A202C"}
        },
        paper_bgcolor=THEME["background"],
        plot_bgcolor=THEME["background"],
        font={"family": THEME["font_family"], "color": "#334155", "size": 12},
        margin=dict(l=30, r=30, t=55, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
    )
    return fig

def plot_top_products(products_df: pd.DataFrame, top_n=10):
    """
    Horizontal bar chart of top N products ranked by sales.
    """
    if products_df.empty:
        return go.Figure()

    # Sort ascending for horizontal bar representation
    sorted_df = products_df.sort_values(by="Sales", ascending=True)

    fig = go.Figure(go.Bar(
        x=sorted_df["Sales"],
        y=sorted_df["Product"],
        orientation="h",
        marker=dict(
            color=sorted_df["Profit Margin"],
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Margin %", thickness=15)
        ),
        hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.2f}<extra></extra>"
    ))

    _apply_standard_layout(fig, f"Top {len(sorted_df)} Products by Sales Revenue", "Total Sales ($)", "Product Name")
    fig.update_layout(margin=dict(l=220, r=40, t=55, b=45))
    return fig

def plot_top_salespersons(salesperson_df: pd.DataFrame, top_n=10):
    """
    Horizontal bar chart of top salespeople ranked by generated sales.
    """
    if salesperson_df.empty:
        return go.Figure()

    sorted_df = salesperson_df.sort_values(by="Sales", ascending=True)

    fig = go.Figure(go.Bar(
        x=sorted_df["Sales"],
        y=sorted_df["Salesperson"],
        orientation="h",
        marker=dict(color="#1976D2"),
        hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.2f}<br>Orders: %{customdata[0]}<br>Margin: %{customdata[1]:.1f}%<extra></extra>",
        customdata=np.stack((sorted_df["Orders"], sorted_df["Profit Margin"]), axis=-1)
    ))

    _apply_standard_layout(fig, f"Top {len(sorted_df)} Sales Representatives by Revenue", "Revenue Generated ($)", "Salesperson")
    fig.update_layout(margin=dict(l=150, r=30, t=55, b=45))
    return fig

def plot_sales_vs_profit_scatter(df: pd.DataFrame):
    """
    Scatter plot comparing Sales vs Profit for each transaction.
    Includes breakeven line (Profit = 0) and highlights category groupings.
    """
    if df.empty:
        return go.Figure()

    sample_size = min(len(df), 1200)
    sample_df = df.sample(sample_size, random_state=42) if len(df) > sample_size else df

    fig = px.scatter(
        sample_df,
        x="Sales",
        y="Profit",
        color="Category",
        size="Quantity",
        hover_data=["Order ID", "Product", "Region", "Salesperson", "Profit Margin"],
        color_discrete_sequence=["#1E88E5", "#00897B", "#FB8C00", "#8E24AA"],
        opacity=0.75
    )

    # Add Breakeven Baseline
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color=THEME["danger"],
        annotation_text="Breakeven (Profit = $0)",
        annotation_position="bottom right"
    )

    _apply_standard_layout(fig, "Order-Level Sales vs. Profit Relationship (Sample)", "Order Sales ($)", "Net Profit ($)")
    return fig

def plot_order_size_distribution(df: pd.DataFrame):
    """
    Bar chart showing order volume and revenue across order size tiers.
    """
    if df.empty or "OrderSizeTier" not in df.columns:
        return go.Figure()

    tier_df = df.groupby("OrderSizeTier", observed=False).agg(
        Order_Count=("Order ID", "nunique"),
        Total_Sales=("Sales", "sum")
    ).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=tier_df["OrderSizeTier"],
        y=tier_df["Order_Count"],
        name="Order Count",
        marker_color="#42A5F5",
        hovertemplate="<b>%{x}</b><br>Orders: %{y:,}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=tier_df["OrderSizeTier"],
        y=tier_df["Total_Sales"],
        name="Sales ($)",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color="#FF7043", width=3),
        hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>"
    ))

    fig.update_layout(
        yaxis2=dict(
            title="<b>Total Sales ($)</b>",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    _apply_standard_layout(fig, "Order Volume & Sales by Order Size Tier", "Order Size Category", "Number of Orders")
    return fig
