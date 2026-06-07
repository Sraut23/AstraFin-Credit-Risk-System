# =========================================================
# AstraFin Credit Services
# Phase 4.3 - PD Modeling Dataset
# =========================================================

import pandas as pd
import numpy as np

# =========================================================
# LOAD FILES
# =========================================================

customers_df = pd.read_csv(
    "../data/synthetic/customers.csv"
)

risk_profile_df = pd.read_csv(
    "../data/synthetic/risk_profile.csv"
)

assessments_df = pd.read_csv(
    "../data/synthetic/credit_assessments.csv"
)

loans_df = pd.read_csv(
    "../data/synthetic/loan_cashflows.csv"
)

# =========================================================
# LOAN LEVEL FEATURES
# =========================================================

loan_features = loans_df[
    [
        "loan_id",
        "customer_id",
        "loan_amount",
        "interest_rate",
        "tenure_months",
        "loan_status",
        "risk_band",
        "credit_score"
    ]
].copy()

# =========================================================
# TARGET VARIABLE
# =========================================================

loan_features["default_flag"] = np.where(
    loan_features["loan_status"] == "Defaulted",
    1,
    0
)

# =========================================================
# CUSTOMER FEATURES
# =========================================================

customer_features = customers_df[
    [
        "customer_id",
        "monthly_income",
        "customer_segment",
        "risk_profile"
    ]
]

# =========================================================
# RISK PROFILE FEATURES
# =========================================================

risk_features = risk_profile_df[
    [
        "customer_id",
        "existing_loans",
        "total_outstanding",
        "monthly_obligations",
        "dti_ratio",
        "previous_defaults"
    ]
]

# =========================================================
# MERGE ALL FEATURES
# =========================================================

model_df = (
    loan_features
    .merge(
        customer_features,
        on="customer_id",
        how="left"
    )
    .merge(
        risk_features,
        on="customer_id",
        how="left"
    )
)

# =========================================================
# DATA QUALITY CHECKS
# =========================================================

print("\n==========================")
print("MODEL DATASET SUMMARY")
print("==========================")

print(
    f"\nRows: {len(model_df):,}"
)

print(
    f"Columns: {model_df.shape[1]}"
)

print("\nDefault Rate")

print(
    round(
        model_df["default_flag"]
        .mean() * 100,
        2
    ),
    "%"
)

print("\nMissing Values")

print(
    model_df.isnull()
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
)

# =========================================================
# FEATURE PREVIEW
# =========================================================

print("\nSample Data")

print(
    model_df.head()
)

# =========================================================
# EXPORT
# =========================================================

output_file = (
    "../data/synthetic/pd_model_dataset.csv"
)

model_df.to_csv(
    output_file,
    index=False
)

print("\n==========================")
print("pd_model_dataset.csv created")
print("==========================")

print(output_file)