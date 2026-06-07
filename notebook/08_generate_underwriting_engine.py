# =========================================================
# AstraFin Credit Services
# Phase 3.2 - Underwriting Engine
# =========================================================

import pandas as pd
import numpy as np
import random
from faker import Faker

# =========================================================
# INITIALIZE
# =========================================================

fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)

TARGET_APPLICATIONS = 120000

# =========================================================
# LOAD DATA
# =========================================================

customers_df = pd.read_csv(
    "../data/synthetic/customers.csv"
)

loan_products_df = pd.read_csv(
    "../data/synthetic/loan_products.csv"
)

credit_scores_df = pd.read_csv(
    "../data/synthetic/credit_scores.csv"
)

risk_profile_df = pd.read_csv(
    "../data/synthetic/risk_profile.csv"
)

# =========================================================
# LATEST CREDIT SCORE PER CUSTOMER
# =========================================================

latest_scores = (
    credit_scores_df
    .sort_values("score_date")
    .groupby("customer_id")
    .tail(1)
)

latest_scores = latest_scores[
    ["customer_id", "bureau_score"]
]

# =========================================================
# MERGE CUSTOMER BASE
# =========================================================

customer_base = (
    customers_df
    .merge(
        latest_scores,
        on="customer_id",
        how="left"
    )
    .merge(
        risk_profile_df,
        on="customer_id",
        how="left"
    )
)

# =========================================================
# PRODUCT PREFERENCE LOGIC
# =========================================================

def choose_product(segment):

    if segment == "Government Salaried":
        return random.choices(
            [1, 4, 3],
            weights=[60, 30, 10],
            k=1
        )[0]

    elif segment == "Private Salaried":
        return random.choices(
            [1, 4, 5],
            weights=[50, 25, 25],
            k=1
        )[0]

    elif segment == "SME Owner":
        return random.choices(
            [2, 1],
            weights=[80, 20],
            k=1
        )[0]

    elif segment == "Self Employed":
        return random.choices(
            [2, 1],
            weights=[60, 40],
            k=1
        )[0]

    elif segment == "Freelancer":
        return random.choices(
            [1, 5],
            weights=[50, 50],
            k=1
        )[0]

    else:
        return random.choices(
            [3, 5, 1],
            weights=[50, 30, 20],
            k=1
        )[0]

# =========================================================
# RISK BAND
# =========================================================

def risk_band(score):

    if score >= 750:
        return "Low"

    elif score >= 650:
        return "Medium"

    elif score >= 550:
        return "High"

    else:
        return "Very High"

# =========================================================
# UNDERWRITING DECISION
# =========================================================

def decision(score, dti):

    # LOW RISK

    if score >= 750 and dti < 0.45:

        return random.choices(
            ["Approved", "Manual Review"],
            weights=[95, 5],
            k=1
        )[0]

    # MEDIUM RISK

    elif score >= 650 and dti < 0.55:

        return random.choices(
            ["Approved", "Manual Review", "Rejected"],
            weights=[75, 20, 5],
            k=1
        )[0]

    # HIGH RISK

    elif score >= 550:

        return random.choices(
            ["Approved", "Manual Review", "Rejected"],
            weights=[40, 35, 25],
            k=1
        )[0]

    # VERY HIGH RISK

    else:

        return random.choices(
            ["Approved", "Manual Review", "Rejected"],
            weights=[10, 20, 70],
            k=1
        )[0]

# =========================================================
# APPLICATION CHANNELS
# =========================================================

channels = [
    "Branch",
    "Mobile App",
    "Website"
]

channel_weights = [
    55,
    30,
    15
]

# =========================================================
# PURPOSES
# =========================================================

purposes = [
    "Home Renovation",
    "Medical Emergency",
    "Education",
    "Business Expansion",
    "Vehicle Purchase",
    "Working Capital",
    "Debt Consolidation",
    "Consumer Electronics"
]

# =========================================================
# GENERATION
# =========================================================

applications = []
assessments = []

application_id = 1
assessment_id = 1

while application_id <= TARGET_APPLICATIONS:

    customer = customer_base.sample(1).iloc[0]

    customer_id = customer["customer_id"]

    product_id = choose_product(
        customer["customer_segment"]
    )

    product = loan_products_df[
        loan_products_df["product_id"] == product_id
    ].iloc[0]

    income = customer["monthly_income"]

    multiplier = product[
        "eligibility_income_multiplier"
    ]

    max_eligible_amount = (
        income * multiplier
    )

    requested_amount = random.randint(
        int(product["min_amount"]),
        int(
            min(
                product["max_amount"],
                max_eligible_amount
            )
        )
    )

    requested_tenure = random.randint(
        12,
        int(product["max_tenure_months"])
    )

    application_date = fake.date_between(
        start_date="-5y",
        end_date="today"
    )

    score = int(customer["bureau_score"])

    dti = float(customer["dti_ratio"])

    band = risk_band(score)

    app_decision = decision(
        score,
        dti
    )

    applications.append({

        "application_id": application_id,

        "customer_id": customer_id,

        "product_id": product_id,

        "application_date": application_date,

        "requested_amount": requested_amount,

        "requested_tenure": requested_tenure,

        "application_channel":
            random.choices(
                channels,
                weights=channel_weights,
                k=1
            )[0],

        "application_status":
            app_decision,

        "purpose":
            random.choice(purposes)

    })

    assessments.append({

        "assessment_id": assessment_id,

        "application_id": application_id,

        "credit_score": score,

        "dti_ratio": dti,

        "risk_band": band,

        "assessment_decision":
            app_decision,

        "assessment_date":
            application_date,

        "existing_loans":
            customer["existing_loans"],

        "total_outstanding":
            customer["total_outstanding"],

        "monthly_obligations":
            customer["monthly_obligations"]

    })

    application_id += 1
    assessment_id += 1

# =========================================================
# DATAFRAMES
# =========================================================

applications_df = pd.DataFrame(
    applications
)

assessments_df = pd.DataFrame(
    assessments
)

# =========================================================
# VALIDATION
# =========================================================

print("\n==============================")
print("APPLICATIONS")
print("==============================")

print(applications_df.shape)

print(
    applications_df[
        "application_status"
    ].value_counts(normalize=True)
)

print("\n==============================")
print("ASSESSMENTS")
print("==============================")

print(assessments_df.shape)

print(
    assessments_df[
        "risk_band"
    ].value_counts(normalize=True)
)

# =========================================================
# EXPORT
# =========================================================

applications_df.to_csv(
    "../data/synthetic/loan_applications.csv",
    index=False
)

assessments_df.to_csv(
    "../data/synthetic/credit_assessments.csv",
    index=False
)

print("\nFiles Saved Successfully")