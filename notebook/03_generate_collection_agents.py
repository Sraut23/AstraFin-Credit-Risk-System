# =========================================================
# AstraFin Credit Services
# Phase 3.1 - Collection Agent Master Data Generation
# =========================================================

# =========================
# IMPORT LIBRARIES
# =========================

import pandas as pd
import numpy as np
import random
from faker import Faker

# =========================
# INITIALIZE
# =========================

fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)

# =========================
# LOAD BRANCHES
# =========================

branches_df = pd.read_csv("../data/synthetic/branches.csv")

# =========================
# CONFIGURATION
# =========================

TOTAL_AGENTS = 120

# Metro branches need more agents
metro_cities = [
    "Mumbai",
    "Bangalore",
    "Hyderabad",
    "New Delhi",
    "Chennai",
    "Pune",
    "Ahmedabad",
    "Kolkata"
]

# =========================
# SPECIALIZATION TYPES
# =========================

specializations = [
    "Early Bucket (1-30 DPD)",
    "Mid Bucket (31-60 DPD)",
    "Late Bucket (61-90 DPD)",
    "NPA Recovery",
    "Field Collections"
]

# =========================
# PERFORMANCE TIERS
# =========================

performance_tiers = [
    "Top Performer",
    "Average Performer",
    "Low Performer"
]

performance_weights = [20, 60, 20]

# =========================
# AGENT GENERATION
# =========================

agents = []

agent_id = 1

# Create branch allocation weights
branch_weights = []

for _, row in branches_df.iterrows():

    if row["city"] in metro_cities:
        branch_weights.append(3)
    else:
        branch_weights.append(1)

# Normalize
branch_weights = np.array(branch_weights)
branch_weights = branch_weights / branch_weights.sum()

# =========================
# GENERATE AGENTS
# =========================

for _ in range(TOTAL_AGENTS):

    selected_branch = branches_df.sample(
        n=1,
        weights=branch_weights
    ).iloc[0]

    experience = random.randint(1, 15)

    # Recovery capability depends on experience
    if experience >= 10:
        recovery_score = random.randint(80, 100)

    elif experience >= 5:
        recovery_score = random.randint(60, 85)

    else:
        recovery_score = random.randint(40, 70)

    # Performance Tier
    performance_tier = random.choices(
        performance_tiers,
        weights=performance_weights,
        k=1
    )[0]

    # Specialization Logic
    if experience >= 10:

        specialization = random.choice([
            "NPA Recovery",
            "Late Bucket (61-90 DPD)",
            "Field Collections"
        ])

    elif experience >= 5:

        specialization = random.choice([
            "Mid Bucket (31-60 DPD)",
            "Late Bucket (61-90 DPD)"
        ])

    else:

        specialization = random.choice([
            "Early Bucket (1-30 DPD)",
            "Mid Bucket (31-60 DPD)"
        ])

    joining_date = fake.date_between(
        start_date='-10y',
        end_date='today'
    )

    agents.append({

        "agent_id": agent_id,

        "agent_name": fake.name(),

        "branch_id": selected_branch["branch_id"],

        "city": selected_branch["city"],

        "state": selected_branch["state"],

        "experience_years": experience,

        "specialization": specialization,

        "recovery_capability_score": recovery_score,

        "performance_tier": performance_tier,

        "joining_date": joining_date

    })

    agent_id += 1

# =========================
# CREATE DATAFRAME
# =========================

agents_df = pd.DataFrame(agents)

# =========================
# VALIDATION
# =========================

print("\n" + "=" * 60)
print("COLLECTION AGENT DATA VALIDATION")
print("=" * 60)

print(f"\nTotal Agents: {agents_df.shape[0]}")

print("\nNull Values:")
print(agents_df.isnull().sum())

print("\nDuplicate Agent IDs:")
print(agents_df["agent_id"].duplicated().sum())

print("\nPerformance Tier Distribution:")
print(agents_df["performance_tier"].value_counts())

print("\nSpecialization Distribution:")
print(agents_df["specialization"].value_counts())

print("\nRecovery Capability Statistics:")
print(agents_df["recovery_capability_score"].describe())

# =========================
# SAMPLE DATA
# =========================

print("\nSample Data:")
print(agents_df.head())

# =========================
# EXPORT CSV
# =========================

output_path = "../data/synthetic/collection_agents.csv"

agents_df.to_csv(output_path, index=False)

print("\n" + "=" * 60)
print("CSV FILE SUCCESSFULLY SAVED")
print("=" * 60)

print(f"\nLocation: {output_path}")