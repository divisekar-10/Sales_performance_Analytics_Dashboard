# Sales Performance Analytics Dashboard

**An End-to-End Decision Support System for Sales Performance Monitoring, Margin Analysis, and Strategic Forecasting**

---

## 📌 Project Overview
The **Sales Performance Analytics Dashboard** is an interactive, multi-dimensional business intelligence and data analytics platform. Designed specifically for an undergraduate Artificial Intelligence and Data Science capstone or academic internship project (8–12 weeks duration), it empowers business executives, sales leaders, and financial analysts to monitor sales velocity, optimize regional allocations, analyze product profitability, and identify operational bottlenecks in real time.

---

## 🚩 Problem Statement
In modern enterprise environments, sales transaction data is frequently scattered across disparate operational silos (ERP systems, CRM platforms, billing spreadsheets). As a consequence:
1. **Lack of Real-Time Visibility**: Leadership cannot track revenue or margin trends promptly.
2. **Margin Erosion**: Volume discounting often creates loss-making orders that remain unnoticed until financial year-end.
3. **Ineffective Resource Allocation**: Regional sales managers lack granular performance metrics on sales representatives and category profitability.
4. **Poor Decision-Making**: Raw tabular reports overwhelm stakeholders without providing actionable, automated business insights.

---

## 🎯 Project Objectives
- **Centralize & Harmonize Data**: Ingest, clean, and enrich raw sales transactional records into a structured analytical format.
- **Automate KPI Computation**: Calculate standardized business metrics (Total Revenue, Net Profit, Operating Margin %, Average Order Value, and Units Sold).
- **Interactive Multi-Dimensional Exploration**: Enable dynamic filtering by date ranges, geographic territories, product categories, and sales representatives.
- **Actionable Visual Analytics**: Deliver high-impact visual trends (monthly time series, regional breakdowns, category shares, salesperson leaderboards, and order-level profit correlation).
- **Executive Decision Support**: Automate diagnostic insights, flagging margin leakages, peak trading periods, and growth recommendations.
- **Data Portability**: Enable one-click export of filtered transactional data (CSV, Excel) and executive narrative reports.

---

## 🛠️ Technologies Used
| Component | Technology / Library | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core application logic and data pipelines |
| **User Interface** | Streamlit | Web application framework and reactive dashboard UI |
| **Data Processing** | Pandas, NumPy | Data cleaning, type casting, filtering, and aggregations |
| **Data Visualization** | Plotly (Express & Graph Objects) | Interactive, responsive charts with rich hover tooltips |
| **Data Export** | OpenPyXL, CSV | Exporting filtered subsets to Excel and CSV |
| **Testing** | Unittest | Automated unit and integration testing suite |

---

## 📊 Dataset Description
The dashboard includes a realistic, multi-year sales dataset generated with enterprise patterns (seasonal surges, regional weighting, and realistic profit margins).

### Attributes:
1. **Order ID**: Unique alphanumeric order identifier (e.g., `ORD-2024-10213`)
2. **Order Date**: Confirmation timestamp (daily granularity spanning 2024 to 2026)
3. **Product**: Catalog item name (e.g., ThinkPad X1 Laptop, 4K Monitor, Cloud Backup License)
4. **Category**: High-level domain (`Technology`, `Furniture`, `Office Supplies`, `Enterprise Software`)
5. **Region**: Geographic territory (`North`, `South`, `East`, `West`, `Central`)
6. **Salesperson**: Dedicated sales executive assigned to the transaction
7. **Customer**: B2B client enterprise name
8. **Quantity**: Count of items purchased in the order (1 to 25 units)
9. **Unit Price**: List selling price per single unit ($)
10. **Sales**: Gross revenue generated (`Quantity * Unit Price`)
11. **Cost**: Direct cost of goods sold (`Quantity * Unit Cost`)
12. **Profit**: Net financial return (`Sales - Cost`)
13. **Profit Margin**: Operating margin percentage (`(Profit / Sales) * 100`)

### Derived / Feature-Engineered Attributes:
- `Year`, `Month`, `Month_Num`, `YearMonth`, `Quarter`, `DayOfWeek`, `IsWeekend`
- `IsProfitable`: Boolean flag denoting positive net return
- `OrderSizeTier`: Transaction classification (`Small <$500`, `Medium $500–$2K`, `Large $2K–$5K`, `Enterprise >$5K`)

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher installed on your system.
- Pip package manager.

### Step 1: Clone or Navigate to the Project Directory
```bash
cd d:\Sales_Performance_Analystics_Dashboard
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 How to Run the Dashboard

### Method 1: Using the Python Launcher (Recommended)
```bash
python run.py
```

### Method 2: Direct Streamlit Command
```bash
python -m streamlit run app.py
```

### Method 3: Windows Batch Script (One-Click)
Double-click `run.bat` in the project root folder.

*The dashboard will automatically open in your default browser at `http://localhost:8501`.*

---

## 🧪 Running Automated Tests
To run the automated verification test suite:
```bash
python test_dashboard.py
```
This tests schema integrity, derived features, mathematical KPI accuracy, multi-criteria filtering, chart rendering pipelines, and empty filter error handling.

---

## 🖥️ Dashboard Structure & Features

### 1. Global Filter Panel (Sidebar)
- **Date Range Picker**: Dynamic temporal boundary filtering.
- **Geographic Region Multi-select**: Filter by North, South, East, West, or Central.
- **Product Category Multi-select**: Isolate specific product segments.
- **Specific Products Multi-select**: Granular product-level analysis.
- **Sales Representative Multi-select**: Individual performance tracking.
- **Reset All Filters**: Instant one-click restoration to baseline.
- **Regenerate Dataset**: Dynamic synthetic dataset generator with fresh seed distributions.

### 2. High-Impact KPI Scorecards
- **Total Sales**: Aggregate revenue generated across filtered records.
- **Total Profit**: Cumulative net return after COGS deduction.
- **Profit Margin (%)**: Overall weighted operating margin percentage.
- **Total Orders**: Count of unique transactions processed.
- **Units Sold**: Total physical and digital volume distributed.
- **Average Order Value (AOV)**: Revenue per completed transaction.

### 3. Five Dedicated Analytical Tabs:
1. **📊 Executive Overview & Insights**:
   - Automated natural-language executive findings.
   - Highlights: Revenue Engine, Profitability Champion, Geographic Stronghold, Top Rep, Flagship Product, Peak Month.
   - Combined Sales vs. Profit Dual-Axis Monthly Chart.
   - Operational Risk Flags (unprofitable orders, under-penetrated territories) & Strategic Recommendations.
2. **📈 Sales & Profit Trends**:
   - Monthly Sales Trend Line & Area Chart with average baseline.
   - Monthly Profit Trend Line & Area Chart.
   - Day-of-Week Sales Volume Distribution.
   - Monthly Financial Performance Summary Table with Month-over-Month (MoM) Growth %.
3. **🗺️ Regional & Category Deep-Dive**:
   - Total Sales by Geographic Region (Bar chart).
   - Net Profit & Margin by Region (Annotated Bar chart).
   - Category Sales Share (Donut chart).
   - Order Volume & Revenue by Size Tier (Small, Medium, Large, Enterprise).
   - Category Profitability Matrix Table.
4. **🏆 Top Performers & Leaderboard**:
   - Top 10 Products by Sales Revenue (colored by profit margin).
   - Top 10 Sales Representatives Leaderboard (Sales, Orders, Margin).
   - Order-Level Sales vs. Profit Scatter Plot with Breakeven Reference Line ($0 Profit).
5. **📋 Data Explorer & Export**:
   - Interactive transactional table with keyword search (Customer, Product, Order ID) and multi-column sorting.
   - Statistical distribution summary (`count`, `mean`, `std`, `min`, `quartiles`, `max`).
   - One-click downloads: Filtered CSV, Filtered Excel (`.xlsx`), and Executive Summary Text Report (`.txt`).

---

## 📈 Analytical Results from the Benchmark Dataset
- **Gross Revenue**: Over **\$7.89 Million** across 2,500 transactions.
- **Operating Profit**: Over **\$2.89 Million** with an overall average profit margin of **38.5%**.
- **Category Profit Leader**: `Enterprise Software` yields the highest margin (~68%), while `Technology` drives the largest total volume and revenue.
- **Geographic Leader**: The `East` and `North` territories represent the highest sales volume.
- **Operational Leakage Identified**: ~3.5% of transactions were marked down below cost during quarterly discount clearances, demonstrating the practical need for discount governance.

---

## 🔮 Future Enhancements
1. **Predictive Sales Forecasting**: Integrate ARIMA / Prophet / LSTM models to forecast next-quarter revenue.
2. **Customer Lifetime Value (CLV) & Churn Scoring**: Machine learning models for customer segmentation (RFM analysis).
3. **Live Database Connectors**: Direct integration with PostgreSQL, MySQL, Snowflake, or BigQuery.
4. **Role-Based Access Control (RBAC)**: Personalized views for regional managers vs. C-suite executives.

**##LIVE DEMO**

[OPEN LIVE PROJECT] https://sales-performance-analytics-dashboard-2.onrender.com/
