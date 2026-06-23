import pandas as pd
import numpy as np

BUSINESS_DATA = {
    "Bakery": {
        "revenue": 75000,
        "customers": 420,
        "growth_score": 72,
        "inventory_health": 85,
        "top_products": ["Sourdough Bread", "Chocolate Croissant", "Birthday Cakes", "Muffins", "Baguettes"],
        "monthly_revenue": [58000, 61000, 63000, 67000, 70000, 75000],
        "monthly_customers": [310, 330, 350, 370, 400, 420],
        "product_demand": [45, 30, 15, 25, 20],
        "low_stock": ["Chocolate Chips", "Butter", "Vanilla Extract"],
        "business_desc": "A neighborhood artisan bakery known for handcrafted sourdough and seasonal pastries."
    },
    "Café": {
        "revenue": 120000,
        "customers": 680,
        "growth_score": 81,
        "inventory_health": 78,
        "top_products": ["Flat White", "Avocado Toast", "Cold Brew", "Croissant", "Matcha Latte"],
        "monthly_revenue": [95000, 100000, 105000, 110000, 115000, 120000],
        "monthly_customers": [510, 540, 570, 610, 645, 680],
        "product_demand": [55, 30, 40, 25, 35],
        "low_stock": ["Oat Milk", "Avocados", "Coffee Beans (Ethiopia)"],
        "business_desc": "A specialty coffee café with a curated food menu in a cozy urban setting."
    },
    "Gym": {
        "revenue": 90000,
        "customers": 310,
        "growth_score": 65,
        "inventory_health": 90,
        "top_products": ["Monthly Membership", "Personal Training", "Group Classes", "Protein Supplements", "Day Pass"],
        "monthly_revenue": [75000, 78000, 80000, 83000, 87000, 90000],
        "monthly_customers": [260, 270, 280, 290, 300, 310],
        "product_demand": [60, 20, 35, 15, 10],
        "low_stock": ["Whey Protein", "Resistance Bands", "Yoga Mats"],
        "business_desc": "A modern fitness center offering equipment, group classes, and personal training."
    },
    "Clothing Store": {
        "revenue": 210000,
        "customers": 850,
        "growth_score": 88,
        "inventory_health": 70,
        "top_products": ["Summer Dresses", "Denim Jeans", "Formal Shirts", "Sneakers", "Accessories"],
        "monthly_revenue": [160000, 170000, 180000, 190000, 200000, 210000],
        "monthly_customers": [640, 680, 720, 760, 800, 850],
        "product_demand": [40, 35, 25, 30, 20],
        "low_stock": ["Size M Dresses", "White Formal Shirts", "Running Shoes Size 8"],
        "business_desc": "A trendy fashion boutique catering to young urban professionals and style-conscious shoppers."
    },
    "Freelance Agency": {
        "revenue": 180000,
        "customers": 45,
        "growth_score": 78,
        "inventory_health": 95,
        "top_products": ["Web Design", "Brand Identity", "Social Media Management", "SEO Services", "Content Writing"],
        "monthly_revenue": [130000, 140000, 150000, 160000, 170000, 180000],
        "monthly_customers": [32, 35, 38, 40, 42, 45],
        "product_demand": [35, 25, 30, 20, 15],
        "low_stock": ["Design Licenses", "Stock Photo Credits", "Cloud Storage"],
        "business_desc": "A boutique creative agency delivering digital branding, design, and marketing services."
    },
}

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

def get_business_df(business_type: str) -> dict:
    data = BUSINESS_DATA.get(business_type, BUSINESS_DATA["Café"])
    
    revenue_df = pd.DataFrame({
        "Month": MONTHS,
        "Revenue (₹)": data["monthly_revenue"]
    })
    
    customer_df = pd.DataFrame({
        "Month": MONTHS,
        "Customers": data["monthly_customers"]
    })
    
    demand_df = pd.DataFrame({
        "Product": data["top_products"],
        "Demand Score": data["product_demand"]
    })
    
    return {
        "revenue_df": revenue_df,
        "customer_df": customer_df,
        "demand_df": demand_df,
        "kpis": {
            "revenue": data["revenue"],
            "customers": data["customers"],
            "growth_score": data["growth_score"],
            "inventory_health": data["inventory_health"],
        },
        "low_stock": data["low_stock"],
        "top_products": data["top_products"],
        "business_desc": data["business_desc"],
    }
