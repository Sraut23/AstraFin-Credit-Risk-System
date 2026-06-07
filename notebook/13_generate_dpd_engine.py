# =========================================================
# AstraFin Credit Services
# Phase 3.7 - DPD Engine
# =========================================================

import pandas as pd
import numpy as np
import os

# =========================================================
# LOAD REPAYMENTS
# =========================================================

repayments_df = pd.read_csv(
    "../data/synthetic/repayments.csv"
)

print(f"\nLoaded {len(repayments_df):,} repayments")

# =========================================================
# DPD CALCULATION
# =========================================================

repayments_df["days_past_due"] = (
    repayments_df["days_late"]
)

# =========================================================
# DPD BUCKETS
# =========================================================

def dpd_bucket(days):

    if days == 0:
        return "Current"

    elif days <= 30:
        return "1-30"

    elif days <= 60:
        return "31-60"

    elif days <= 90:
        return "61-90"

    else:
        return "90+"

repayments_df["dpd_bucket"] = (
    repayments_df["days_past_due"]
    .apply(dpd_bucket)
)

# =========================================================
# PAR FLAGS
# =========================================================

repayments_df["par30_flag"] = np.where(
    repayments_df["days_past_due"] >= 30,
    1,
    0
)

repayments_df["par60_flag"] = np.where(
    repayments_df["days_past_due"] >= 60,
    1,
    0
)

repayments_df["par90_flag"] = np.where(
    repayments_df["days_past_due"] >= 90,
    1,
    0
)

# =========================================================
# RBI STYLE NPA FLAG
# =========================================================

repayments_df["npa_flag"] = np.where(
    repayments_df["days_past_due"] >= 90,
    1,
    0
)

# =========================================================
# PORTFOLIO METRICS
# =========================================================

total_records = len(repayments_df)

par30_rate = (
    repayments_df["par30_flag"].sum()
    / total_records
) * 100

par60_rate = (
    repayments_df["par60_flag"].sum()
    / total_records
) * 100

par90_rate = (
    repayments_df["par90_flag"].sum()
    / total_records
) * 100

npa_rate = (
    repayments_df["npa_flag"].sum()
    / total_records
) * 100

# =========================================================
# VALIDATION
# =========================================================

print("\n==========================")
print("DPD DISTRIBUTION")
print("==========================")

print(
    repayments_df["dpd_bucket"]
    .value_counts(normalize=True)
)

print("\n==========================")
print("PORTFOLIO RISK")
print("==========================")

print(
    f"\nPAR30 : {par30_rate:.2f}%"
)

print(
    f"PAR60 : {par60_rate:.2f}%"
)

print(
    f"PAR90 : {par90_rate:.2f}%"
)

print(
    f"NPA    : {npa_rate:.2f}%"
)

# =========================================================
# EXPORT
# =========================================================

output_file = (
    "../data/synthetic/dpd_status.csv"
)

repayments_df.to_csv(
    output_file,
    index=False
)

print("\n==========================")
print("DPD FILE CREATED")
print("==========================")

print(output_file)