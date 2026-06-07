# =========================================================
# AstraFin Credit Services
# Phase 3.1 - Customer Master Data Generation
# =========================================================

import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import date

# =========================================================
# INITIALIZE
# =========================================================

fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)

TOTAL_CUSTOMERS = 50000

# =========================================================
# LOAD BRANCHES
# =========================================================

branches_df = pd.read_csv("../data/synthetic/branches.csv")

# =========================================================
# STATE-CITY MAPPING
# =========================================================

state_city_map = (
    branches_df.groupby("state")["city"]
    .apply(list)
    .to_dict()
)

states = list(state_city_map.keys())

# =========================================================
# CUSTOMER SEGMENTS
# =========================================================

segments = [
    "Government Salaried",
    "Private Salaried",
    "Self Employed",
    "SME Owner",
    "Freelancer",
    "New-to-Credit"
]

segment_weights = [
    15,
    35,
    20,
    10,
    8,
    12
]

# =========================================================
# INCOME GENERATION
# =========================================================

def generate_income(segment, age):

    if segment == "Government Salaried":
        base = random.randint(40000, 150000)

    elif segment == "Private Salaried":
        base = random.randint(25000, 250000)

    elif segment == "Self Employed":
        base = random.randint(30000, 300000)

    elif segment == "SME Owner":
        base = random.randint(50000, 500000)

    elif segment == "Freelancer":
        base = random.randint(20000, 120000)

    else:  # New-to-Credit
        base = random.randint(15000, 60000)

    # age-income relationship
    if age > 40:
        base *= random.uniform(1.05, 1.35)

    return round(base)

# =========================================================
# STABILITY SCORES
# =========================================================

def stability_scores(segment):

    if segment == "Government Salaried":
        return (
            random.randint(85, 100),
            random.randint(85, 100)
        )

    elif segment == "Private Salaried":
        return (
            random.randint(65, 90),
            random.randint(60, 90)
        )

    elif segment == "Self Employed":
        return (
            random.randint(50, 85),
            random.randint(50, 85)
        )

    elif segment == "SME Owner":
        return (
            random.randint(55, 90),
            random.randint(55, 90)
        )

    elif segment == "Freelancer":
        return (
            random.randint(35, 75),
            random.randint(35, 75)
        )

    else:
        return (
            random.randint(20, 60),
            random.randint(20, 60)
        )

# =========================================================
# RISK PROFILE
# =========================================================

def assign_risk(segment):

    if segment == "Government Salaried":
        return random.choices(
            ["Low", "Medium"],
            weights=[80, 20]
        )[0]

    elif segment == "Private Salaried":
        return random.choices(
            ["Low", "Medium", "High"],
            weights=[30, 55, 15]
        )[0]

    elif segment == "Self Employed":
        return random.choices(
            ["Medium", "High"],
            weights=[60, 40]
        )[0]

    elif segment == "SME Owner":
        return random.choices(
            ["Medium", "High"],
            weights=[40, 60]
        )[0]

    elif segment == "Freelancer":
        return random.choices(
            ["Medium", "High"],
            weights=[30, 70]
        )[0]

    else:
        return "High"

# =========================================================
# CUSTOMER GENERATION
# =========================================================

customers = []

for customer_id in range(1, TOTAL_CUSTOMERS + 1):

    segment = random.choices(
        segments,
        weights=segment_weights,
        k=1
    )[0]

    state = random.choice(states)
    city = random.choice(state_city_map[state])

    gender = random.choice(["Male", "Female"])

    age = random.randint(21, 65)

    today = date.today()

    dob = date(
    today.year - age,
    random.randint(1, 12),
    random.randint(1, 28)
    )

    income = generate_income(segment, age)

    income_stability, employment_stability = (
        stability_scores(segment)
    )

    risk_profile = assign_risk(segment)

    # future default propensity
    if risk_profile == "Low":
        default_propensity = round(
            random.uniform(0.01, 0.08), 3
        )

    elif risk_profile == "Medium":
        default_propensity = round(
            random.uniform(0.08, 0.20), 3
        )

    else:
        default_propensity = round(
            random.uniform(0.20, 0.50), 3
        )

    if segment == "Government Salaried":
        employment_type = "Permanent"

    elif segment == "Private Salaried":
        employment_type = random.choice(
            ["Permanent", "Contract"]
        )

    elif segment in ["SME Owner", "Self Employed"]:
        employment_type = "Business"

    elif segment == "Freelancer":
        employment_type = "Gig Worker"

    else:
        employment_type = "New Credit"

    education_level = random.choice([
        "High School",
        "Diploma",
        "Graduate",
        "Post Graduate",
        "Professional"
    ])

    years_at_current_job = random.randint(
        0,
        min(age - 20, 25)
    )

    customers.append({

        "customer_id": customer_id,

        "first_name": fake.first_name(),

        "last_name": fake.last_name(),

        "gender": gender,

        "dob": dob,

        "marital_status": random.choice([
            "Single",
            "Married",
            "Divorced"
        ]),

        "occupation": segment,

        "employment_type": employment_type,

        "monthly_income": income,

        "city": city,

        "state": state,

        "pincode": fake.postcode(),

        "customer_since": fake.date_between(
            start_date="-7y",
            end_date="today"
        ),

        "customer_segment": segment,

        "income_stability_score": income_stability,

        "employment_stability_score": employment_stability,

        "future_default_propensity": default_propensity,

        "risk_profile": risk_profile,

        "education_level": education_level,

        "years_at_current_job": years_at_current_job

    })

# =========================================================
# CREATE DATAFRAME
# =========================================================

customers_df = pd.DataFrame(customers)

# =========================================================
# VALIDATION
# =========================================================

print("\n" + "=" * 60)
print("CUSTOMER DATA VALIDATION")
print("=" * 60)

print(f"\nTotal Customers: {customers_df.shape[0]}")

print("\nNull Values:")
print(customers_df.isnull().sum())

print("\nDuplicate Customer IDs:")
print(customers_df["customer_id"].duplicated().sum())

print("\nRisk Profile Distribution:")
print(customers_df["risk_profile"].value_counts())

print("\nCustomer Segment Distribution:")
print(customers_df["customer_segment"].value_counts())

print("\nIncome Statistics:")
print(customers_df["monthly_income"].describe())

# =========================================================
# EXPORT
# =========================================================

output_path = "../data/synthetic/customers.csv"

customers_df.to_csv(
    output_path,
    index=False
)

print("\n" + "=" * 60)
print("CUSTOMERS CSV SUCCESSFULLY SAVED")
print("=" * 60)

print(f"\nLocation: {output_path}")