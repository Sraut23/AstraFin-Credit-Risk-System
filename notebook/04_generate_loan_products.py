# =========================================================
# AstraFin Credit Services
# Phase 3.1 - Loan Product Master Data Generation
# =========================================================

import pandas as pd
import numpy as np

# =========================================================
# LOAN PRODUCT CONFIGURATION
# =========================================================

loan_products = [

    {
        "product_id": 1,
        "product_name": "Personal Loan",
        "min_amount": 50000,
        "max_amount": 1000000,
        "min_interest_rate": 10.5,
        "max_interest_rate": 22.0,
        "max_tenure_months": 60,
        "risk_level": "Medium",
        "eligibility_income_multiplier": 20,
        "processing_fee_percent": 2.0,
        "default_probability_base": 0.06
    },

    {
        "product_id": 2,
        "product_name": "Business Loan",
        "min_amount": 100000,
        "max_amount": 2500000,
        "min_interest_rate": 12.0,
        "max_interest_rate": 26.0,
        "max_tenure_months": 84,
        "risk_level": "High",
        "eligibility_income_multiplier": 30,
        "processing_fee_percent": 2.5,
        "default_probability_base": 0.10
    },

    {
        "product_id": 3,
        "product_name": "Education Loan",
        "min_amount": 100000,
        "max_amount": 2000000,
        "min_interest_rate": 8.5,
        "max_interest_rate": 15.0,
        "max_tenure_months": 120,
        "risk_level": "Medium",
        "eligibility_income_multiplier": 25,
        "processing_fee_percent": 1.0,
        "default_probability_base": 0.05
    },

    {
        "product_id": 4,
        "product_name": "Vehicle Loan",
        "min_amount": 50000,
        "max_amount": 1500000,
        "min_interest_rate": 7.5,
        "max_interest_rate": 14.0,
        "max_tenure_months": 84,
        "risk_level": "Low",
        "eligibility_income_multiplier": 18,
        "processing_fee_percent": 1.5,
        "default_probability_base": 0.03
    },

    {
        "product_id": 5,
        "product_name": "Consumer Durable Loan",
        "min_amount": 10000,
        "max_amount": 200000,
        "min_interest_rate": 13.0,
        "max_interest_rate": 28.0,
        "max_tenure_months": 24,
        "risk_level": "Medium-High",
        "eligibility_income_multiplier": 8,
        "processing_fee_percent": 3.0,
        "default_probability_base": 0.08
    }

]

# =========================================================
# CREATE DATAFRAME
# =========================================================

loan_products_df = pd.DataFrame(loan_products)

# =========================================================
# DERIVED METRICS
# =========================================================

loan_products_df["avg_interest_rate"] = (
    loan_products_df["min_interest_rate"] +
    loan_products_df["max_interest_rate"]
) / 2

loan_products_df["max_amount_lakhs"] = (
    loan_products_df["max_amount"] / 100000
).round(2)

# =========================================================
# VALIDATION
# =========================================================

print("\n" + "=" * 60)
print("LOAN PRODUCT VALIDATION")
print("=" * 60)

print("\nTotal Products:")
print(len(loan_products_df))

print("\nNull Values:")
print(loan_products_df.isnull().sum())

print("\nDuplicate Product IDs:")
print(loan_products_df["product_id"].duplicated().sum())

print("\nRisk Distribution:")
print(loan_products_df["risk_level"].value_counts())

print("\nProduct Summary:")
print(
    loan_products_df[
        [
            "product_name",
            "risk_level",
            "max_amount_lakhs",
            "avg_interest_rate"
        ]
    ]
)

# =========================================================
# EXPORT
# =========================================================

output_path = "../data/synthetic/loan_products.csv"

loan_products_df.to_csv(
    output_path,
    index=False
)

print("\n" + "=" * 60)
print("CSV FILE SUCCESSFULLY SAVED")
print("=" * 60)
print(f"\nLocation: {output_path}")

# =========================================================
# SAMPLE DATA
# =========================================================

print("\nSample Data:")
print(loan_products_df.head())