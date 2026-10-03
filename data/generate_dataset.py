"""
Sales Performance Analytics Dataset Generator
Generates a realistic, multi-year sales dataset with realistic distributions,
seasonal variations, product hierarchies, and financial relationships.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_sales_data(num_records=2500, output_path="data/sales_data.csv", seed=42):
    random.seed(seed)
    np.random.seed(seed)

    # Catalog definition: Category -> Products with baseline pricing and typical profit margins
    catalog = {
        "Technology": [
            {"product": "ThinkPad X1 Carbon Laptop", "base_price": 1450.0, "base_margin": 0.28},
            {"product": "Dell UltraSharp 27\" 4K Monitor", "base_price": 580.0, "base_margin": 0.32},
            {"product": "Sony WH-1000XM5 Headphones", "base_price": 380.0, "base_margin": 0.35},
            {"product": "Logitech MX Master 3S Mouse", "base_price": 99.0, "base_margin": 0.42},
            {"product": "Keychron Q3 Mechanical Keyboard", "base_price": 175.0, "base_margin": 0.38},
            {"product": "Anker 10-in-1 USB-C Docking Hub", "base_price": 130.0, "base_margin": 0.45},
            {"product": "Samsung 2TB Portable NVMe SSD", "base_price": 190.0, "base_margin": 0.30},
        ],
        "Furniture": [
            {"product": "Herman Miller Ergonomic Chair", "base_price": 1150.0, "base_margin": 0.25},
            {"product": "Electric Dual-Motor Standing Desk", "base_price": 680.0, "base_margin": 0.28},
            {"product": "Executive Teakwood Conference Table", "base_price": 1850.0, "base_margin": 0.22},
            {"product": "Steel Storage Lateral Filing Cabinet", "base_price": 340.0, "base_margin": 0.30},
            {"product": "Acoustic Fabric Office Partition", "base_price": 260.0, "base_margin": 0.33},
        ],
        "Office Supplies": [
            {"product": "HP LaserJet Pro Multi-function Printer", "base_price": 420.0, "base_margin": 0.24},
            {"product": "High-Yield Toner Cartridge Pack", "base_price": 125.0, "base_margin": 0.48},
            {"product": "Heavy-Duty Cross-Cut Paper Shredder", "base_price": 160.0, "base_margin": 0.36},
            {"product": "Magnetic Glass Dry-Erase Board", "base_price": 210.0, "base_margin": 0.40},
            {"product": "Premium Recycled Copy Paper (Carton)", "base_price": 48.0, "base_margin": 0.35},
        ],
        "Enterprise Software": [
            {"product": "Cloud Analytics Pro License (Annual)", "base_price": 1200.0, "base_margin": 0.72},
            {"product": "Cybersecurity Endpoint Protection Suite", "base_price": 950.0, "base_margin": 0.68},
            {"product": "Automated CRM Collaboration Seat", "base_price": 720.0, "base_margin": 0.65},
            {"product": "Cloud Data Backup & Recovery License", "base_price": 540.0, "base_margin": 0.70},
        ]
    }

    regions = ["North", "South", "East", "West", "Central"]
    
    # Regional weightings to model real-world business distribution
    region_weights = [0.24, 0.16, 0.28, 0.22, 0.10]

    salespersons_by_region = {
        "North": ["Sarah Jenkins", "Michael Chang"],
        "South": ["Amina Patel", "David Rodriguez"],
        "East": ["Emily Watson", "James Wilson"],
        "West": ["Robert Martinez", "Priya Sharma"],
        "Central": ["Daniel Kim", "Jessica Taylor"]
    }

    customers = [
        "Acme Global Technologies",
        "Nexus Logistics Group",
        "Pinnacle Healthcare Systems",
        "Vanguard Financial Solutions",
        "Summit Media Works",
        "Horizon Retail Partners",
        "Zenith Dynamics Ltd",
        "Bluebird Creative Labs",
        "Apollo Industrial Equipment",
        "Titan Cloud Infrastructure",
        "Beacon Legal Consulting",
        "Evergreen Renewable Energy",
        "Silverline Manufacturing",
        "Metro Education Foundation",
        "Cascade BioSciences"
    ]

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 6, 30)
    total_days = (end_date - start_date).days

    records = []

    for i in range(1, num_records + 1):
        order_id = f"ORD-{2024 + (i % 3)}-{10000 + i}"
        
        # Sample date with temporal growth & Q4 end-of-year seasonality boost
        day_offset = int(np.random.beta(a=1.3, b=1.1) * total_days)
        order_date = start_date + timedelta(days=day_offset)
        month = order_date.month

        # Seasonal multiplier (Q4 higher sales, Nov & Dec enterprise budget clearance)
        seasonal_prob = 1.0
        if month in [10, 11, 12]:
            seasonal_prob = 1.35
        elif month in [6, 7]:
            seasonal_prob = 1.15
        elif month in [1, 2]:
            seasonal_prob = 0.85

        # Select Region
        region = np.random.choice(regions, p=region_weights)
        salesperson = random.choice(salespersons_by_region[region])
        customer = random.choice(customers)

        # Select Category and Product
        category = random.choices(
            list(catalog.keys()),
            weights=[0.38, 0.22, 0.22, 0.18],
            k=1
        )[0]
        
        prod_meta = random.choice(catalog[category])
        product_name = prod_meta["product"]
        base_price = prod_meta["base_price"]
        base_margin = prod_meta["base_margin"]

        # Slight price fluctuation (+/- 8%)
        price_variation = np.random.uniform(0.92, 1.08)
        unit_price = round(base_price * price_variation, 2)

        # Quantity ordered: software usually fewer seats or batch, supplies high qty
        if category == "Office Supplies":
            quantity = int(np.random.choice(range(2, 26), p=np.linspace(0.12, 0.01, 24) / np.sum(np.linspace(0.12, 0.01, 24))))
        elif category == "Enterprise Software":
            quantity = random.randint(1, 8)
        elif category == "Furniture":
            quantity = random.randint(1, 10)
        else: # Technology
            quantity = random.randint(1, 12)

        # Base unit cost calculated from margin with slight variance
        # Margin variance (+/- 5%), with 2.5% chance of steep discount leading to slight loss/breakeven
        margin_noise = np.random.normal(0, 0.04)
        is_discounted = random.random() < 0.035
        
        if is_discounted:
            achieved_margin = random.uniform(-0.06, 0.04)  # End-of-quarter discount clearance
        else:
            achieved_margin = max(0.05, min(0.85, base_margin + margin_noise))

        unit_cost = round(unit_price * (1.0 - achieved_margin), 2)
        
        # Financial Totals
        sales = round(quantity * unit_price, 2)
        cost = round(quantity * unit_cost, 2)
        profit = round(sales - cost, 2)
        profit_margin = round((profit / sales) * 100, 2) if sales > 0 else 0.0

        records.append({
            "Order ID": order_id,
            "Order Date": order_date.strftime("%Y-%m-%d"),
            "Product": product_name,
            "Category": category,
            "Region": region,
            "Salesperson": salesperson,
            "Customer": customer,
            "Quantity": quantity,
            "Unit Price": unit_price,
            "Sales": sales,
            "Cost": cost,
            "Profit": profit,
            "Profit Margin": profit_margin
        })

    df = pd.DataFrame(records)
    # Sort chronologically by Order Date
    df["TempDate"] = pd.to_datetime(df["Order Date"])
    df = df.sort_values(by="TempDate").reset_index(drop=True)
    df = df.drop(columns=["TempDate"])

    # Ensure parent directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Successfully generated {len(df)} records at: {output_path}")
    print(f"Total Sales: ${df['Sales'].sum():,.2f}")
    print(f"Total Profit: ${df['Profit'].sum():,.2f}")
    print(f"Average Margin: {df['Profit Margin'].mean():.2f}%")
    return df

if __name__ == "__main__":
    generate_sales_data()
