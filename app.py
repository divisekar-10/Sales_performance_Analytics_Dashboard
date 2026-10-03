"""
Sales Performance Analytics Dashboard
Academic Project Prototype for Sales Performance Monitoring & Analytics
Designed for Undergraduate AI & Data Science Curriculum (8-12 Weeks Duration)
"""

import os
import io
import pandas as pd
import streamlit as st

# Set page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Sales Performance Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import internal modular services
from src.data_loader import load_sales_data, filter_dataset, ensure_dataset_exists
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

# Custom CSS for polished academic appearance
st.markdown("""
<style>
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 14px 18px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetric"]:hover {
        border-color: #3B82F6;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.08);
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.65rem;
        font-weight: 700;
        color: #0F172A;
    }
    /* Header Container */
    .project-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        color: white;
        padding: 24px 30px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
    }
    .project-title {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .project-subtitle {
        font-size: 0.95rem;
        color: #DBEAFE;
        margin-top: 6px;
        margin-bottom: 0;
    }
    .badge-bar {
        margin-top: 14px;
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
    }
    .badge {
        background: rgba(255, 255, 255, 0.18);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #F8FAFC;
    }
    /* Section card */
    .insight-card {
        background-color: #F8FAFC;
        border-left: 4px solid #2563EB;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 12px;
    }
    .risk-card {
        background-color: #FEF2F2;
        border-left: 4px solid #EF4444;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 12px;
        color: #991B1B;
    }
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        padding: 8px 20px;
        font-weight: 600;
        border-radius: 6px 6px 0 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def get_cached_sales_data():
    """Cached loader for raw dataset to optimize rendering performance."""
    return load_sales_data()

def render_header():
    """Renders the standard academic project header banner."""
    st.markdown("""
    <div class="project-header">
        <h1 class="project-title">Sales Performance Analytics Dashboard</h1>
        <p class="project-subtitle">
            An Interactive Decision-Support System for Multi-Dimensional Sales Monitoring, Margin Analytics & Strategic Forecasting
        </p>
        <div class="badge-bar">
            <span class="badge">Project: Individual Academic Prototype</span>
            <span class="badge">Course: Artificial Intelligence & Data Science</span>
            <span class="badge">Duration: 8-12 Weeks</span>
            <span class="badge">Engine: Streamlit & Plotly Core</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def initialize_session_state(raw_df):
    """Initializes or resets default filter parameters in session state."""
    min_date = raw_df["Order Date"].min().date()
    max_date = raw_df["Order Date"].max().date()
    
    if "filter_date_range" not in st.session_state:
        st.session_state["filter_date_range"] = (min_date, max_date)
    if "filter_regions" not in st.session_state:
        st.session_state["filter_regions"] = []
    if "filter_categories" not in st.session_state:
        st.session_state["filter_categories"] = []
    if "filter_products" not in st.session_state:
        st.session_state["filter_products"] = []
    if "filter_salespersons" not in st.session_state:
        st.session_state["filter_salespersons"] = []

def reset_filters_callback(min_date, max_date):
    """Callback to restore filters to original baseline."""
    st.session_state["filter_date_range"] = (min_date, max_date)
    st.session_state["filter_regions"] = []
    st.session_state["filter_categories"] = []
    st.session_state["filter_products"] = []
    st.session_state["filter_salespersons"] = []

def render_sidebar(raw_df):
    """Builds interactive filter controls in the sidebar."""
    min_date = raw_df["Order Date"].min().date()
    max_date = raw_df["Order Date"].max().date()
    
    with st.sidebar:
        st.markdown("### 🎛️ Analytics Filter Panel")
        st.caption("Customize the analysis scope across temporal, geographic, and organizational dimensions.")
        
        # Reset Filters Button
        if st.button("🔄 Reset All Filters", use_container_width=True):
            reset_filters_callback(min_date, max_date)
            st.rerun()

        st.divider()

        # 1. Date Range Picker
        date_selection = st.date_input(
            "📅 Date Range",
            value=st.session_state.get("filter_date_range", (min_date, max_date)),
            min_value=min_date,
            max_value=max_date,
            help="Filter sales records by order confirmation date"
        )
        if isinstance(date_selection, (tuple, list)) and len(date_selection) == 2:
            start_d, end_d = date_selection
        elif isinstance(date_selection, (tuple, list)) and len(date_selection) == 1:
            start_d = end_d = date_selection[0]
        else:
            start_d, end_d = min_date, max_date

        # 2. Region Multi-select
        all_regions = sorted(raw_df["Region"].unique().tolist())
        selected_regions = st.multiselect(
            "🌍 Geographic Region",
            options=all_regions,
            default=st.session_state.get("filter_regions", []),
            placeholder="All Regions (Active)"
        )

        # 3. Category Multi-select
        all_categories = sorted(raw_df["Category"].unique().tolist())
        selected_categories = st.multiselect(
            "📦 Product Category",
            options=all_categories,
            default=st.session_state.get("filter_categories", []),
            placeholder="All Categories (Active)"
        )

        # 4. Product Multi-select (dynamically filtered by category if selected)
        product_pool = raw_df.copy()
        if selected_categories:
            product_pool = product_pool[product_pool["Category"].isin(selected_categories)]
        all_products = sorted(product_pool["Product"].unique().tolist())
        selected_products = st.multiselect(
            "🏷️ Specific Products",
            options=all_products,
            default=st.session_state.get("filter_products", []),
            placeholder="All Products (Active)"
        )

        # 5. Salesperson Multi-select (dynamically filtered by region if selected)
        rep_pool = raw_df.copy()
        if selected_regions:
            rep_pool = rep_pool[rep_pool["Region"].isin(selected_regions)]
        all_salespersons = sorted(rep_pool["Salesperson"].unique().tolist())
        selected_salespersons = st.multiselect(
            "👤 Sales Representative",
            options=all_salespersons,
            default=st.session_state.get("filter_salespersons", []),
            placeholder="All Representatives (Active)"
        )

        st.divider()
        st.markdown("#### ⚙️ Data Administration")
        if st.button("⚡ Regenerate Dataset", help="Recreates synthetic sales dataset with fresh randomness"):
            from data.generate_dataset import generate_sales_data
            generate_sales_data()
            st.cache_data.clear()
            st.success("New dataset generated!")
            st.rerun()

        st.caption("Sales Performance Analytics v1.0 • Academic Build")

    return start_d, end_d, selected_regions, selected_categories, selected_products, selected_salespersons

def render_kpi_cards(kpis: dict, total_raw_count: int, filtered_count: int):
    """Renders the top row of high-impact KPI scorecards."""
    st.markdown("### 📌 Executive Key Performance Indicators (KPIs)")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric(
            label="Total Sales",
            value=kpis["fmt_total_sales"],
            help="Gross revenue generated across filtered transactions"
        )
    with col2:
        st.metric(
            label="Total Profit",
            value=kpis["fmt_total_profit"],
            help="Cumulative net profit after deducting production/acquisition costs"
        )
    with col3:
        st.metric(
            label="Profit Margin",
            value=kpis["fmt_profit_margin"],
            help="Operating margin = (Total Profit / Total Sales) * 100"
        )
    with col4:
        st.metric(
            label="Total Orders",
            value=kpis["fmt_total_orders"],
            help=f"Volume: {filtered_count:,} records ({filtered_count/total_raw_count*100:.1f}% of total data)"
        )
    with col5:
        st.metric(
            label="Units Sold",
            value=kpis["fmt_total_quantity"],
            help="Aggregate volume of physical & digital items transacted"
        )
    with col6:
        st.metric(
            label="Avg Order Value",
            value=kpis["fmt_avg_order_value"],
            help="AOV = Total Sales / Total Orders"
        )

def main():
    render_header()

    # Load dataset
    raw_df = get_cached_sales_data()
    initialize_session_state(raw_df)

    # Sidebar Filter Controls
    start_d, end_d, sel_regions, sel_cats, sel_prods, sel_reps = render_sidebar(raw_df)

    # Apply Filters
    df = filter_dataset(
        raw_df,
        start_date=start_d,
        end_date=end_d,
        regions=sel_regions,
        categories=sel_cats,
        products=sel_prods,
        salespersons=sel_reps
    )

    # Error handling for empty filter scenario
    if df.empty:
        st.warning(
            "⚠️ **No records match your selected filter criteria.** "
            "Please broaden your filter parameters in the left sidebar or click **'Reset All Filters'**."
        )
        st.stop()

    # Compute KPI Metrics
    kpis = calculate_kpis(df)
    render_kpi_cards(kpis, len(raw_df), len(df))

    st.markdown("<br>", unsafe_allow_html=True)

    # Compute Aggregations
    monthly_df = get_monthly_aggregation(df)
    regional_df = get_regional_aggregation(df)
    category_df = get_category_aggregation(df)
    top_products_df = get_top_performers(df, entity_col="Product", top_n=10)
    top_salespersons_df = get_top_performers(df, entity_col="Salesperson", top_n=10)
    insights = generate_business_insights(df)

    # Main Tabbed Interface
    tab_overview, tab_trends, tab_regional, tab_performers, tab_data = st.tabs([
        "📊 Executive Overview & Insights",
        "📈 Sales & Profit Trends",
        "🗺️ Regional & Category Deep-Dive",
        "🏆 Top Performers & Leaderboard",
        "📋 Data Explorer & Export"
    ])

    # -------------------------------------------------------------
    # TAB 1: EXECUTIVE OVERVIEW & INSIGHTS
    # -------------------------------------------------------------
    with tab_overview:
        st.subheader("Executive Summary & Automated Strategic Findings")
        
        # Summary callout
        st.markdown(f"""
        <div class="insight-card">
            <span style="font-size: 1.1rem; color: #1E293B;">
                {insights["summary_statement"]}
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🎯 Key Analytical Highlights")
        h_cols = st.columns(3)
        for idx, item in enumerate(insights["highlights"]):
            with h_cols[idx % 3]:
                st.markdown(f"""
                <div style="background: white; border: 1px solid #E2E8F0; padding: 14px 16px; border-radius: 8px; margin-bottom: 12px;">
                    <div style="font-size: 1.2rem; margin-bottom: 4px;">{item['icon']} <b>{item['title']}</b></div>
                    <div style="font-size: 0.9rem; color: #334155;">{item['detail']}</div>
                </div>
                """, unsafe_allow_html=True)

        # Dual Axis Trend Chart
        st.markdown("#### 📊 Monthly Sales vs. Net Profit Dynamic")
        st.plotly_chart(plot_sales_vs_profit_monthly(monthly_df), use_container_width=True)

        # Risk Factors & Recommendations Side-by-Side
        r_col1, r_col2 = st.columns(2)
        with r_col1:
            st.markdown("#### ⚠️ Operational Risk & Margin Leakage")
            if insights["risk_factors"]:
                for risk in insights["risk_factors"]:
                    st.markdown(f"""
                    <div class="risk-card">
                        {risk}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ No critical margin leakage or territory deficits observed under current parameters.")

        with r_col2:
            st.markdown("#### 💡 Strategic Action Recommendations")
            for rec in insights["recommendations"]:
                st.markdown(f"- {rec}", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 2: SALES & PROFIT TRENDS
    # -------------------------------------------------------------
    with tab_trends:
        st.subheader("Temporal Trends and Growth Analysis")
        
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            st.plotly_chart(plot_monthly_sales_trend(monthly_df), use_container_width=True)
        with t_col2:
            st.plotly_chart(plot_monthly_profit_trend(monthly_df), use_container_width=True)

        st.markdown("#### 🗓️ Day-of-Week & Order Volume Dynamic")
        d_col1, d_col2 = st.columns([1, 1])
        with d_col1:
            # Day of week aggregation
            dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            dow_df = df.groupby("DayOfWeek").agg(
                Sales=("Sales", "sum"),
                Orders=("Order ID", "nunique")
            ).reindex(dow_order).reset_index()
            
            import plotly.express as px
            dow_fig = px.bar(
                dow_df,
                x="DayOfWeek",
                y="Sales",
                color="Orders",
                labels={"DayOfWeek": "Day of the Week", "Sales": "Sales ($)", "Orders": "Order Count"},
                color_continuous_scale="Blues"
            )
            dow_fig.update_layout(
                title="<b>Sales Distribution by Day of Week</b>",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=40, r=20, t=50, b=40)
            )
            st.plotly_chart(dow_fig, use_container_width=True)

        with d_col2:
            st.markdown("##### 📋 Monthly Financial Summary Table")
            display_monthly = monthly_df.copy()
            display_monthly["Sales"] = display_monthly["Sales"].apply(lambda x: f"${x:,.2f}")
            display_monthly["Profit"] = display_monthly["Profit"].apply(lambda x: f"${x:,.2f}")
            display_monthly["Profit Margin"] = display_monthly["Profit Margin"].apply(lambda x: f"{x:.1f}%")
            display_monthly["MoM_Sales_Growth"] = display_monthly["MoM_Sales_Growth"].apply(
                lambda x: f"{x:+.1f}%" if pd.notnull(x) else "—"
            )
            st.dataframe(
                display_monthly.rename(columns={
                    "YearMonth": "Month",
                    "Orders": "Total Orders",
                    "Quantity": "Units Sold",
                    "MoM_Sales_Growth": "MoM Growth"
                }),
                use_container_width=True,
                height=320
            )

    # -------------------------------------------------------------
    # TAB 3: REGIONAL & CATEGORY DEEP-DIVE
    # -------------------------------------------------------------
    with tab_regional:
        st.subheader("Geographic and Product Category Performance")
        
        reg_col1, reg_col2 = st.columns(2)
        with reg_col1:
            st.plotly_chart(plot_sales_by_region(regional_df), use_container_width=True)
        with reg_col2:
            st.plotly_chart(plot_profit_by_region(regional_df), use_container_width=True)

        st.divider()

        cat_col1, cat_col2 = st.columns(2)
        with cat_col1:
            st.plotly_chart(plot_sales_by_category(category_df), use_container_width=True)
        with cat_col2:
            st.plotly_chart(plot_order_size_distribution(df), use_container_width=True)

        st.markdown("#### 📊 Category Profitability Matrix")
        styled_cat = category_df.copy()
        styled_cat["Sales"] = styled_cat["Sales"].apply(lambda x: f"${x:,.2f}")
        styled_cat["Profit"] = styled_cat["Profit"].apply(lambda x: f"${x:,.2f}")
        styled_cat["Profit Margin"] = styled_cat["Profit Margin"].apply(lambda x: f"{x:.1f}%")
        styled_cat["Sales_Share_Pct"] = styled_cat["Sales_Share_Pct"].apply(lambda x: f"{x:.1f}%")
        st.dataframe(styled_cat, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 4: TOP PERFORMERS & RELATIONSHIPS
    # -------------------------------------------------------------
    with tab_performers:
        st.subheader("Rankings and Transactional Relationships")
        
        top_col1, top_col2 = st.columns(2)
        with top_col1:
            st.plotly_chart(plot_top_products(top_products_df, top_n=10), use_container_width=True)
        with top_col2:
            st.plotly_chart(plot_top_salespersons(top_salespersons_df, top_n=10), use_container_width=True)

        st.divider()
        st.markdown("#### 🔍 Sales vs. Profit Order-Level Correlation (Breakeven Analysis)")
        st.caption("Each bubble represents an order. Point size reflects order quantity; color indicates category.")
        st.plotly_chart(plot_sales_vs_profit_scatter(df), use_container_width=True)

    # -------------------------------------------------------------
    # TAB 5: DATA EXPLORER & EXPORT
    # -------------------------------------------------------------
    with tab_data:
        st.subheader("Raw Data Explorer and Export Facility")
        st.caption("Inspect filtered transactional records, evaluate statistical summaries, and export data for offline analysis.")

        col_search, col_sort = st.columns([3, 1])
        with col_search:
            search_query = st.text_input("🔍 Search orders (by Customer, Product, or ID):", placeholder="e.g. Acme, ThinkPad...")
        with col_sort:
            sort_by = st.selectbox("Sort records by:", ["Order Date (Newest)", "Order Date (Oldest)", "Sales (High to Low)", "Profit (High to Low)"])

        display_df = df.copy()
        if search_query:
            query_lower = search_query.lower()
            mask = (
                display_df["Customer"].str.lower().str.contains(query_lower) |
                display_df["Product"].str.lower().str.contains(query_lower) |
                display_df["Order ID"].str.lower().str.contains(query_lower)
            )
            display_df = display_df[mask]

        if sort_by == "Order Date (Newest)":
            display_df = display_df.sort_values(by="Order Date", ascending=False)
        elif sort_by == "Order Date (Oldest)":
            display_df = display_df.sort_values(by="Order Date", ascending=True)
        elif sort_by == "Sales (High to Low)":
            display_df = display_df.sort_values(by="Sales", ascending=False)
        elif sort_by == "Profit (High to Low)":
            display_df = display_df.sort_values(by="Profit", ascending=False)

        # Show record count
        st.write(f"Showing **{len(display_df):,}** of **{len(df):,}** filtered records.")
        st.dataframe(
            display_df[[
                "Order ID", "Order Date", "Customer", "Product", "Category", 
                "Region", "Salesperson", "Quantity", "Unit Price", "Sales", "Cost", "Profit", "Profit Margin"
            ]],
            use_container_width=True,
            height=380
        )

        st.markdown("#### 📥 Data Download Options")
        d_col1, d_col2, d_col3 = st.columns(3)

        with d_col1:
            csv_data = display_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Filtered Data (CSV)",
                data=csv_data,
                file_name=f"sales_data_filtered_{start_d}_to_{end_d}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with d_col2:
            # Excel export buffer
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                display_df.to_excel(writer, index=False, sheet_name="FilteredSales")
            st.download_button(
                label="📊 Download Filtered Data (Excel)",
                data=buffer.getvalue(),
                file_name=f"sales_data_filtered_{start_d}_to_{end_d}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        with d_col3:
            # Executive Summary Report Download
            summary_text = f"""================================================================================
SALES PERFORMANCE ANALYTICS DASHBOARD - EXECUTIVE REPORT
Academic Submission: AI and Data Science Project
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
================================================================================

1. EXECUTIVE SUMMARY:
   {insights['summary_statement']}

2. KEY METRICS:
   - Total Gross Sales:     {kpis['fmt_total_sales']}
   - Total Net Profit:      {kpis['fmt_total_profit']}
   - Overall Profit Margin: {kpis['fmt_profit_margin']}
   - Total Orders Processed:{kpis['fmt_total_orders']}
   - Total Volume Sold:     {kpis['fmt_total_quantity']} units
   - Average Order Value:   {kpis['fmt_avg_order_value']}

3. DOMAIN HIGHLIGHTS:
   - Top Category (Sales):  {insights['metrics']['top_category']}
   - Leading Territory:     {insights['metrics']['top_region']}
   - Top Salesperson:       {insights['metrics']['top_salesperson']}
   - Best Selling Offering: {insights['metrics']['top_product']}
   - Peak Revenue Period:   {insights['metrics']['peak_month']}

4. STRATEGIC RECOMMENDATIONS:
""" + "\n".join([f"   - {r}" for r in insights['recommendations']]) + "\n\n" + """================================================================================"""
            
            st.download_button(
                label="📄 Download Executive Summary (TXT)",
                data=summary_text.encode('utf-8'),
                file_name=f"executive_sales_summary_{start_d}.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.divider()
        st.markdown("#### 📐 Statistical Distribution Summary")
        st.dataframe(
            display_df[["Quantity", "Unit Price", "Sales", "Cost", "Profit", "Profit Margin"]].describe().round(2),
            use_container_width=True
        )

if __name__ == "__main__":
    main()
