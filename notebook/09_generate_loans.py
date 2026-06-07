# =========================================================
# AstraFin Credit Services
# Phase 3.3 - Loan Generation Engine
# =========================================================

import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import timedelta

# =========================================================
# INITIALIZE
# =========================================================

fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)

# =========================================================
# LOAD FILES
# =========================================================

applications_df = pd.read_csv(
    "../data/synthetic/loan_applications.csv"
)

assessments_df = pd.read_csv(
    "../data/synthetic/credit_assessments.csv"
)

customers_df = pd.read_csv(
    "../data/synthetic/customers.csv"
)

products_df = pd.read_csv(
    "../data/synthetic/loan_products.csv"
)

branches_df = pd.read_csv(
    "../data/synthetic/branches.csv"
)

# =========================================================
# APPROVED APPLICATIONS ONLY
# =========================================================

approved_apps = applications_df[
    applications_df["application_status"] == "Approved"
].copy()

print(
    f"\nApproved Applications: {len(approved_apps):,}"
)

# =========================================================
# MERGE DATA
# =========================================================

approved_apps = (
    approved_apps
    .merge(
        assessments_df[
            [
                "application_id",
                "credit_score",
                "risk_band"
            ]
        ],
        on="application_id",
        how="left"
    )
)

approved_apps = (
    approved_apps
    .merge(
        customers_df[
            [
                "customer_id",
                "city",
                "state",
                "risk_profile"
            ]
        ],
        on="customer_id",
        how="left"
    )
)

# =========================================================
# BRANCH LOOKUP
# =========================================================

state_branch_map = (
    branches_df
    .groupby("state")["branch_id"]
    .apply(list)
    .to_dict()
)

# =========================================================
# RISK-BASED INTEREST RATE
# =========================================================

def assign_interest_rate(product, score):

    min_rate = product["min_interest_rate"]
    max_rate = product["max_interest_rate"]

    if score >= 800:
        return round(min_rate, 2)

    elif score >= 750:
        return round(
            min_rate + (max_rate-min_rate)*0.20,
            2
        )

    elif score >= 700:
        return round(
            min_rate + (max_rate-min_rate)*0.40,
            2
        )

    elif score >= 650:
        return round(
            min_rate + (max_rate-min_rate)*0.60,
            2
        )

    else:
        return round(max_rate, 2)

# =========================================================
# LOAN STATUS LOGIC
# =========================================================

def assign_loan_status(risk_band):

    if risk_band == "Low":

        return random.choices(
            [
                "Active",
                "Closed",
                "Defaulted"
            ],
            weights=[70, 28, 2],
            k=1
        )[0]

    elif risk_band == "Medium":

        return random.choices(
            [
                "Active",
                "Closed",
                "Defaulted"
            ],
            weights=[72, 22, 6],
            k=1
        )[0]

    elif risk_band == "High":

        return random.choices(
            [
                "Active",
                "Closed",
                "Defaulted"
            ],
            weights=[70, 15, 15],
            k=1
        )[0]

    else:

        return random.choices(
            [
                "Active",
                "Closed",
                "Defaulted"
            ],
            weights=[60, 10, 30],
            k=1
        )[0]

# =========================================================
# GENERATE LOANS
# =========================================================

loans = []

loan_id = 1

for _, row in approved_apps.iterrows():

    product = products_df[
        products_df["product_id"] ==
        row["product_id"]
    ].iloc[0]

    branch_id = random.choice(
        state_branch_map[row["state"]]
    )

    score = row["credit_score"]

    rate = assign_interest_rate(
        product,
        score
    )

    disbursement_date = (
        pd.to_datetime(
            row["application_date"]
        )
        +
        timedelta(
            days=random.randint(1, 15)
        )
    )

    status = assign_loan_status(
        row["risk_band"]
    )

    loans.append({

        "loan_id": loan_id,

        "application_id":
            row["application_id"],

        "customer_id":
            row["customer_id"],

        "product_id":
            row["product_id"],

        "branch_id":
            branch_id,

        "loan_amount":
            row["requested_amount"],

        "interest_rate":
            rate,

        "tenure_months":
            row["requested_tenure"],

        "disbursement_date":
            disbursement_date,

        "loan_status":
            status,

        "risk_band":
            row["risk_band"],

        "credit_score":
            score

    })

    loan_id += 1

# =========================================================
# DATAFRAME
# =========================================================

loans_df = pd.DataFrame(loans)

# =========================================================
# VALIDATION
# =========================================================

print("\n============================")
print("LOAN PORTFOLIO")
print("============================")

print(
    f"\nTotal Loans: {len(loans_df):,}"
)

print("\nLoan Status Distribution")

print(
    loans_df["loan_status"]
    .value_counts(normalize=True)
)

print("\nRisk Band Distribution")

print(
    loans_df["risk_band"]
    .value_counts(normalize=True)
)

print("\nInterest Rate Statistics")

print(
    loans_df["interest_rate"]
    .describe()
)

# =========================================================
# EXPORT
# =========================================================

loans_df.to_csv(
    "../data/synthetic/loans.csv",
    index=False
)

print("\nloans.csv saved successfully")