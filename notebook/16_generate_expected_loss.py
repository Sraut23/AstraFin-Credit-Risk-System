# =========================================================
# AstraFin Credit Services
# Phase 4.0 - Expected Loss Engine
# Basel Framework
# =========================================================

import pandas as pd
import numpy as np

# =========================================================
# LOAD FILES
# =========================================================

loans_df = pd.read_csv(
    "../data/synthetic/loan_cashflows.csv"
)

writeoffs_df = pd.read_csv(
    "../data/synthetic/writeoffs.csv"
)

# =========================================================
# LGD LOOKUP
# =========================================================

lgd_lookup = (
    writeoffs_df
    .groupby("loan_id")["lgd"]
    .mean()
    .reset_index()
)

# =========================================================
# MERGE
# =========================================================

risk_df = loans_df.merge(
    lgd_lookup,
    on="loan_id",
    how="left"
)

# =========================================================
# FILL NON-DEFAULTED LGD
# =========================================================

portfolio_avg_lgd = round(
    writeoffs_df["lgd"].mean(),
    4
)

risk_df["lgd"] = (
    risk_df["lgd"]
    .fillna(portfolio_avg_lgd)
)

# =========================================================
# PD ASSIGNMENT
# =========================================================

def assign_pd(risk_band):

    if risk_band == "Low":
        return np.random.uniform(
            0.01,
            0.03
        )

    elif risk_band == "Medium":
        return np.random.uniform(
            0.03,
            0.08
        )

    elif risk_band == "High":
        return np.random.uniform(
            0.08,
            0.20
        )

    else:
        return np.random.uniform(
            0.20,
            0.45
        )

risk_df["pd"] = (
    risk_df["risk_band"]
    .apply(assign_pd)
)

# =========================================================
# EAD
# =========================================================

risk_df["ead"] = (
    risk_df["loan_amount"]
)

# =========================================================
# EXPECTED LOSS
# =========================================================

risk_df["expected_loss"] = round(
    risk_df["pd"]
    *
    risk_df["lgd"]
    *
    risk_df["ead"],
    2
)

# =========================================================
# RISK GRADE
# =========================================================

def risk_grade(pd_value):

    if pd_value < 0.03:
        return "A"

    elif pd_value < 0.08:
        return "B"

    elif pd_value < 0.15:
        return "C"

    elif pd_value < 0.25:
        return "D"

    else:
        return "E"

risk_df["risk_grade"] = (
    risk_df["pd"]
    .apply(risk_grade)
)

# =========================================================
# VALIDATION
# =========================================================

print("\n==========================")
print("EXPECTED LOSS SUMMARY")
print("==========================")

print(
    f"\nLoans Analysed: "
    f"{len(risk_df):,}"
)

print("\nRisk Grade Distribution")

print(
    risk_df["risk_grade"]
    .value_counts(normalize=True)
)

print("\nPD Statistics")

print(
    risk_df["pd"]
    .describe()
)

print("\nLGD Statistics")

print(
    risk_df["lgd"]
    .describe()
)

print("\nExpected Loss Statistics")

print(
    risk_df["expected_loss"]
    .describe()
)

print("\nPortfolio Expected Loss")

print(
    round(
        risk_df[
            "expected_loss"
        ].sum(),
        2
    )
)

# =========================================================
# EXPORT
# =========================================================

output_file = (
    "../data/synthetic/expected_loss.csv"
)

risk_df.to_csv(
    output_file,
    index=False
)

print("\n==========================")
print("expected_loss.csv created")
print("==========================")

print(output_file)