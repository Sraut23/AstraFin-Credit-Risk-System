# =========================================================
# AstraFin Credit Services
# Phase 4.8 - Power BI Dataset Builder
# =========================================================

import pandas as pd
from pathlib import Path

# =========================================================
# LOAD FILES
# =========================================================

customers_df = pd.read_csv(
    "../data/synthetic/customers.csv"
)

loans_df = pd.read_csv(
    "../data/synthetic/loan_cashflows.csv"
)

expected_loss_df = pd.read_csv(
    "../data/synthetic/expected_loss.csv"
)

writeoffs_df = pd.read_csv(
    "../data/synthetic/writeoffs.csv"
)

collections_df = pd.read_csv(
    "../data/synthetic/collections.csv"
)

# =========================================================
# COLLECTION AGGREGATION
# =========================================================

collection_summary = (

    collections_df

    .groupby("loan_id")

    .agg(

        total_recovered=("recovered_amount", "sum"),

        collection_cases=("collection_id", "count")

    )

    .reset_index()

)

# =========================================================
# WRITEOFF AGGREGATION
# =========================================================

writeoff_summary = (

    writeoffs_df

    .groupby("loan_id")

    .agg(

        writeoff_amount=("writeoff_amount", "sum"),

        net_credit_loss=("net_credit_loss", "sum"),

        lgd=("lgd", "mean")

    )

    .reset_index()

)

# =========================================================
# EXPECTED LOSS
# =========================================================

el_summary = expected_loss_df[

    [

        "loan_id",
        "pd",
        "lgd",
        "ead",
        "expected_loss",
        "risk_grade"

    ]

].copy()

# =========================================================
# CUSTOMER DIMENSION
# =========================================================

customer_dim = customers_df[

    [

        "customer_id",
        "monthly_income",
        "customer_segment",
        "risk_profile"

    ]

]

# =========================================================
# MASTER DATASET
# =========================================================

powerbi_df = (

    loans_df

    .merge(
        customer_dim,
        on="customer_id",
        how="left"
    )

    .merge(
        el_summary,
        on="loan_id",
        how="left"
    )

    .merge(
        collection_summary,
        on="loan_id",
        how="left"
    )

    .merge(
        writeoff_summary,
        on="loan_id",
        how="left"
    )

)

# =========================================================
# NULL HANDLING
# =========================================================

powerbi_df["total_recovered"] = (
    powerbi_df["total_recovered"]
    .fillna(0)
)

powerbi_df["collection_cases"] = (
    powerbi_df["collection_cases"]
    .fillna(0)
)

powerbi_df["writeoff_amount"] = (
    powerbi_df["writeoff_amount"]
    .fillna(0)
)

powerbi_df["net_credit_loss"] = (
    powerbi_df["net_credit_loss"]
    .fillna(0)
)

# =========================================================
# DATA QUALITY
# =========================================================

print("\n==========================")
print("POWER BI DATASET")
print("==========================")

print(
    f"\nRows: {len(powerbi_df):,}"
)

print(
    f"Columns: {powerbi_df.shape[1]}"
)

print("\nMissing Values")

print(
    powerbi_df.isnull()
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
)

# =========================================================
# EXPORT
# =========================================================

Path("../data/powerbi").mkdir(
    parents=True,
    exist_ok=True
)

output_file = (
    "../data/powerbi/powerbi_credit_risk_dataset.csv"
)

powerbi_df.to_csv(
    output_file,
    index=False
)

print("\n==========================")
print("FILE CREATED")
print("==========================")

print(output_file)