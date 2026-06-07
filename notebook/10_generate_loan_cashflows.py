# =========================================================
# AstraFin Credit Services
# Phase 3.4 - Loan Cashflow Generation
# =========================================================

import pandas as pd
import numpy as np

# =========================================================
# LOAD LOANS
# =========================================================

loans_df = pd.read_csv(
    "../data/synthetic/loans.csv"
)

# =========================================================
# EMI CALCULATION FUNCTION
# =========================================================

def calculate_emi(principal, annual_rate, tenure_months):

    monthly_rate = annual_rate / 12 / 100

    if monthly_rate == 0:
        return principal / tenure_months

    emi = (
        principal *
        monthly_rate *
        ((1 + monthly_rate) ** tenure_months)
    ) / (
        ((1 + monthly_rate) ** tenure_months) - 1
    )

    return round(emi, 2)

# =========================================================
# CALCULATE CASHFLOWS
# =========================================================

emi_amounts = []
total_payments = []
total_interests = []

for _, row in loans_df.iterrows():

    principal = row["loan_amount"]
    rate = row["interest_rate"]
    tenure = row["tenure_months"]

    emi = calculate_emi(
        principal,
        rate,
        tenure
    )

    total_payment = round(
        emi * tenure,
        2
    )

    total_interest = round(
        total_payment - principal,
        2
    )

    emi_amounts.append(emi)
    total_payments.append(total_payment)
    total_interests.append(total_interest)

# =========================================================
# ADD CASHFLOW COLUMNS
# =========================================================

loans_df["emi_amount"] = emi_amounts

loans_df["total_payment"] = total_payments

loans_df["total_interest"] = total_interests

# =========================================================
# VALIDATION
# =========================================================

print("\n==============================")
print("LOAN CASHFLOW VALIDATION")
print("==============================")

print(
    f"\nTotal Loans: {len(loans_df):,}"
)

print("\nEMI Statistics")

print(
    loans_df["emi_amount"]
    .describe()
)

print("\nInterest Income Statistics")

print(
    loans_df["total_interest"]
    .describe()
)

print("\nPortfolio Summary")

print(
    loans_df[
        [
            "loan_amount",
            "emi_amount",
            "total_interest"
        ]
    ]
    .head()
)

# =========================================================
# PORTFOLIO METRICS
# =========================================================

print("\n==============================")
print("PORTFOLIO TOTALS")
print("==============================")

print(
    "\nTotal Principal:",
    round(
        loans_df["loan_amount"].sum(),
        2
    )
)

print(
    "Total Interest Income:",
    round(
        loans_df["total_interest"].sum(),
        2
    )
)

print(
    "Total Cash Inflow:",
    round(
        loans_df["total_payment"].sum(),
        2
    )
)

# =========================================================
# EXPORT
# =========================================================

output_path = (
    "../data/synthetic/loan_cashflows.csv"
)

loans_df.to_csv(
    output_path,
    index=False
)

print("\n==============================")
print("loan_cashflows.csv saved")
print("==============================")