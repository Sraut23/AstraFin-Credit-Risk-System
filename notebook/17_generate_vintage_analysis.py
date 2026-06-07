# =========================================================
# AstraFin Credit Services
# Phase 4.1 - Vintage Analysis Engine
# =========================================================

import pandas as pd
import numpy as np

# =========================================================
# LOAD FILES
# =========================================================

loans_df = pd.read_csv(
    "../data/synthetic/loan_cashflows.csv"
)

dpd_df = pd.read_csv(
    "../data/synthetic/dpd_status.csv"
)

# =========================================================
# DATE PREP
# =========================================================

loans_df["disbursement_date"] = pd.to_datetime(
    loans_df["disbursement_date"]
)

loans_df["vintage_month"] = (
    loans_df["disbursement_date"]
    .dt.to_period("M")
    .astype(str)
)

# =========================================================
# MAX DPD PER LOAN
# =========================================================

loan_dpd = (
    dpd_df
    .groupby("loan_id")
    ["days_past_due"]
    .max()
    .reset_index()
)

# =========================================================
# MERGE
# =========================================================

vintage_df = loans_df.merge(
    loan_dpd,
    on="loan_id",
    how="left"
)

# =========================================================
# DELINQUENCY FLAGS
# =========================================================

vintage_df["dpd30_flag"] = np.where(
    vintage_df["days_past_due"] >= 30,
    1,
    0
)

vintage_df["dpd60_flag"] = np.where(
    vintage_df["days_past_due"] >= 60,
    1,
    0
)

vintage_df["dpd90_flag"] = np.where(
    vintage_df["days_past_due"] >= 90,
    1,
    0
)

# =========================================================
# VINTAGE SUMMARY
# =========================================================

vintage_summary = (
    vintage_df
    .groupby("vintage_month")
    .agg(
        total_loans=("loan_id", "count"),
        dpd30=("dpd30_flag", "sum"),
        dpd60=("dpd60_flag", "sum"),
        dpd90=("dpd90_flag", "sum")
    )
    .reset_index()
)

# =========================================================
# RATES
# =========================================================

vintage_summary["dpd30_rate"] = round(
    vintage_summary["dpd30"]
    /
    vintage_summary["total_loans"]
    * 100,
    2
)

vintage_summary["dpd60_rate"] = round(
    vintage_summary["dpd60"]
    /
    vintage_summary["total_loans"]
    * 100,
    2
)

vintage_summary["dpd90_rate"] = round(
    vintage_summary["dpd90"]
    /
    vintage_summary["total_loans"]
    * 100,
    2
)

# =========================================================
# VALIDATION
# =========================================================

print("\n==========================")
print("VINTAGE ANALYSIS")
print("==========================")

print(
    f"\nTotal Vintages: "
    f"{len(vintage_summary)}"
)

print("\nSample")

print(
    vintage_summary.head()
)

print("\nAverage DPD30 Rate")

print(
    round(
        vintage_summary[
            "dpd30_rate"
        ].mean(),
        2
    )
)

print("\nAverage DPD90 Rate")

print(
    round(
        vintage_summary[
            "dpd90_rate"
        ].mean(),
        2
    )
)

# =========================================================
# EXPORT
# =========================================================

output_file = (
    "../data/synthetic/vintage_analysis.csv"
)

vintage_summary.to_csv(
    output_file,
    index=False
)

print("\n==========================")
print("vintage_analysis.csv created")
print("==========================")

print(output_file)