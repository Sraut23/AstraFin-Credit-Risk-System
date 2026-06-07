# =========================================================
# AstraFin Credit Services
# Phase 4.4 - Credit Risk EDA
# =========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(
    "../data/synthetic/pd_model_dataset.csv"
)

# =========================================================
# OUTPUT FOLDER
# =========================================================

output_dir = Path(
    "../data/eda_output"
)

output_dir.mkdir(
    parents=True,
    exist_ok=True
)

# =========================================================
# BASIC SUMMARY
# =========================================================

print("\n==========================")
print("PORTFOLIO SUMMARY")
print("==========================")

print(
    f"\nLoans: {len(df):,}"
)

default_rate = (
    df["default_flag"].mean() * 100
)

print(
    f"Default Rate: {default_rate:.2f}%"
)

# =========================================================
# CREDIT SCORE BUCKETS
# =========================================================

df["credit_score_bucket"] = pd.cut(
    df["credit_score"],
    bins=[300,550,650,750,900],
    labels=[
        "Poor",
        "Fair",
        "Good",
        "Excellent"
    ]
)

credit_score_risk = (
    df.groupby(
        "credit_score_bucket",
        observed=False
    )["default_flag"]
    .mean()
    .reset_index()
)

credit_score_risk[
    "default_rate"
] = (
    credit_score_risk[
        "default_flag"
    ] * 100
)

print("\nDEFAULT RATE BY CREDIT SCORE")

print(
    credit_score_risk[
        [
            "credit_score_bucket",
            "default_rate"
        ]
    ]
)

credit_score_risk.to_csv(
    output_dir /
    "default_by_credit_score.csv",
    index=False
)

# =========================================================
# RISK BAND ANALYSIS
# =========================================================

risk_band_analysis = (
    df.groupby(
        "risk_band"
    )["default_flag"]
    .mean()
    .reset_index()
)

risk_band_analysis[
    "default_rate"
] = (
    risk_band_analysis[
        "default_flag"
    ] * 100
)

print("\nDEFAULT RATE BY RISK BAND")

print(
    risk_band_analysis[
        [
            "risk_band",
            "default_rate"
        ]
    ]
)

risk_band_analysis.to_csv(
    output_dir /
    "default_by_risk_band.csv",
    index=False
)

# =========================================================
# CUSTOMER SEGMENT ANALYSIS
# =========================================================

segment_analysis = (
    df.groupby(
        "customer_segment"
    )["default_flag"]
    .mean()
    .reset_index()
)

segment_analysis[
    "default_rate"
] = (
    segment_analysis[
        "default_flag"
    ] * 100
)

print("\nDEFAULT RATE BY SEGMENT")

print(
    segment_analysis[
        [
            "customer_segment",
            "default_rate"
        ]
    ]
)

segment_analysis.to_csv(
    output_dir /
    "default_by_segment.csv",
    index=False
)

# =========================================================
# PREVIOUS DEFAULTS
# =========================================================

previous_default_analysis = (
    df.groupby(
        "previous_defaults"
    )["default_flag"]
    .mean()
    .reset_index()
)

previous_default_analysis[
    "default_rate"
] = (
    previous_default_analysis[
        "default_flag"
    ] * 100
)

print("\nDEFAULT RATE BY PREVIOUS DEFAULTS")

print(
    previous_default_analysis
)

previous_default_analysis.to_csv(
    output_dir /
    "default_by_previous_defaults.csv",
    index=False
)

# =========================================================
# DTI BUCKETS
# =========================================================

df["dti_bucket"] = pd.cut(
    df["dti_ratio"],
    bins=[
        0,
        0.2,
        0.4,
        0.6,
        1
    ],
    labels=[
        "Low",
        "Medium",
        "High",
        "Very High"
    ]
)

dti_analysis = (
    df.groupby(
        "dti_bucket",
        observed=False
    )["default_flag"]
    .mean()
    .reset_index()
)

dti_analysis[
    "default_rate"
] = (
    dti_analysis[
        "default_flag"
    ] * 100
)

print("\nDEFAULT RATE BY DTI")

print(
    dti_analysis
)

dti_analysis.to_csv(
    output_dir /
    "default_by_dti.csv",
    index=False
)

# =========================================================
# NUMERICAL CORRELATION
# =========================================================

numeric_cols = [
    "credit_score",
    "monthly_income",
    "loan_amount",
    "interest_rate",
    "tenure_months",
    "existing_loans",
    "total_outstanding",
    "monthly_obligations",
    "dti_ratio",
    "previous_defaults",
    "default_flag"
]

corr_matrix = (
    df[numeric_cols]
    .corr()
)

corr_matrix.to_csv(
    output_dir /
    "correlation_matrix.csv"
)

print("\nTOP CORRELATIONS WITH DEFAULT")

target_corr = (
    corr_matrix["default_flag"]
    .sort_values(
        ascending=False
    )
)

print(
    target_corr
)

# =========================================================
# HISTOGRAMS
# =========================================================

plots = [
    "credit_score",
    "monthly_income",
    "loan_amount",
    "interest_rate",
    "dti_ratio"
]

for col in plots:

    plt.figure(figsize=(8,5))

    df[col].hist(
        bins=40
    )

    plt.title(col)

    plt.tight_layout()

    plt.savefig(
        output_dir /
        f"{col}.png"
    )

    plt.close()

# =========================================================
# EXPORT CLEAN DATASET
# =========================================================

df.to_csv(
    output_dir /
    "eda_dataset.csv",
    index=False
)

print("\n==========================")
print("EDA COMPLETED")
print("==========================")

print(
    f"\nFiles saved to:"
)

print(output_dir)