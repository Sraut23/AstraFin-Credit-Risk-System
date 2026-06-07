# =========================================================
# AstraFin Credit Services
# Phase 4.2 - Roll Rate Matrix
# =========================================================

import pandas as pd
import numpy as np

# =========================================================
# LOAD DPD DATA
# =========================================================

dpd_df = pd.read_csv(
    "../data/synthetic/dpd_status.csv"
)

# =========================================================
# DPD BUCKET ORDER
# =========================================================

bucket_order = {
    "Current": 0,
    "1-30": 1,
    "31-60": 2,
    "61-90": 3,
    "90+": 4
}

# =========================================================
# MAX DPD PER LOAN
# =========================================================

loan_dpd = (
    dpd_df
    .groupby("loan_id")["days_past_due"]
    .max()
    .reset_index()
)

# =========================================================
# ASSIGN CURRENT BUCKET
# =========================================================

def bucket(days):

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

loan_dpd["current_bucket"] = (
    loan_dpd["days_past_due"]
    .apply(bucket)
)

# =========================================================
# SIMULATE NEXT MONTH BUCKET
# =========================================================

next_buckets = []

for current in loan_dpd["current_bucket"]:

    if current == "Current":

        next_bucket = np.random.choice(
            ["Current", "1-30"],
            p=[0.90, 0.10]
        )

    elif current == "1-30":

        next_bucket = np.random.choice(
            ["Current", "1-30", "31-60"],
            p=[0.35, 0.45, 0.20]
        )

    elif current == "31-60":

        next_bucket = np.random.choice(
            ["1-30", "31-60", "61-90"],
            p=[0.20, 0.50, 0.30]
        )

    elif current == "61-90":

        next_bucket = np.random.choice(
            ["31-60", "61-90", "90+"],
            p=[0.15, 0.45, 0.40]
        )

    else:

        next_bucket = np.random.choice(
            ["61-90", "90+"],
            p=[0.10, 0.90]
        )

    next_buckets.append(
        next_bucket
    )

loan_dpd["next_bucket"] = (
    next_buckets
)

# =========================================================
# ROLL RATE MATRIX
# =========================================================

roll_matrix = pd.crosstab(
    loan_dpd["current_bucket"],
    loan_dpd["next_bucket"],
    normalize="index"
)

roll_matrix = round(
    roll_matrix * 100,
    2
)

# =========================================================
# VALIDATION
# =========================================================

print("\n==========================")
print("ROLL RATE MATRIX (%)")
print("==========================")

print(
    roll_matrix
)

# =========================================================
# EXPORT MATRIX
# =========================================================

roll_matrix.to_csv(
    "../data/synthetic/roll_rate_matrix.csv"
)

# =========================================================
# EXPORT TRANSITIONS
# =========================================================

loan_dpd.to_csv(
    "../data/synthetic/roll_rate_transitions.csv",
    index=False
)

print("\n==========================")
print("FILES CREATED")
print("==========================")

print(
    "roll_rate_matrix.csv"
)

print(
    "roll_rate_transitions.csv"
)