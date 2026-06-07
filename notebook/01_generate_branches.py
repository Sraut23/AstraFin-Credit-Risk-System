# =========================================================
# AstraFin Credit Services
# Phase 3.1 - Branch Master Data Generation
# =========================================================

# =========================
# IMPORT LIBRARIES
# =========================

import pandas as pd
import numpy as np
import random
from faker import Faker

# =========================
# INITIALIZE FAKER
# =========================

fake = Faker("en_IN")

# reproducibility
random.seed(42)
np.random.seed(42)

# =========================
# STATE → CITY MAPPING
# =========================

state_city_map = {
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"],
    "Karnataka": ["Bangalore", "Mysore", "Mangalore"],
    "Telangana": ["Hyderabad", "Warangal"],
    "Delhi": ["New Delhi"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara"],
    "West Bengal": ["Kolkata", "Siliguri"],
    "Uttar Pradesh": ["Lucknow", "Noida", "Kanpur"],
    "Rajasthan": ["Jaipur", "Udaipur"],
    "Madhya Pradesh": ["Indore", "Bhopal"]
}

# =========================
# STATE → REGION MAPPING
# =========================

region_map = {
    "Maharashtra": "West",
    "Gujarat": "West",

    "Karnataka": "South",
    "Tamil Nadu": "South",
    "Telangana": "South",

    "Delhi": "North",
    "Uttar Pradesh": "North",
    "Rajasthan": "North",

    "West Bengal": "East",

    "Madhya Pradesh": "Central"
}

# =========================
# GENERATE BRANCHES
# =========================

branches = []

branch_id = 1

for state, cities in state_city_map.items():

    for city in cities:

        # metro cities get more branches
        if city in ["Mumbai", "Bangalore", "Hyderabad", "New Delhi", "Chennai"]:
            branch_count = random.randint(3, 5)

        # large cities get medium number
        elif city in ["Pune", "Ahmedabad", "Kolkata"]:
            branch_count = random.randint(2, 3)

        # smaller cities get 1 branch
        else:
            branch_count = 1

        for i in range(branch_count):

            branch_name = f"AstraFin {city} Branch"

            if branch_count > 1:
                branch_name += f" {i+1}"

            branches.append({
                "branch_id": branch_id,
                "branch_name": branch_name,
                "city": city,
                "state": state,
                "region": region_map[state],
                "manager_id": None,
                "branch_open_date": fake.date_between(
                    start_date='-10y',
                    end_date='today'
                ),
                "branch_category": random.choice([
                    "Metro",
                    "Urban",
                    "Semi-Urban"
                ])
            })

            branch_id += 1

# =========================
# CREATE DATAFRAME
# =========================

branches_df = pd.DataFrame(branches)

# =========================
# VALIDATION
# =========================

print("\n" + "=" * 60)
print("BRANCH DATA VALIDATION")
print("=" * 60)

print(f"\nTotal Branches: {branches_df.shape[0]}")

print("\nNull Values:")
print(branches_df.isnull().sum())

print("\nDuplicate Branch IDs:")
print(branches_df['branch_id'].duplicated().sum())

print("\nState Distribution:")
print(branches_df['state'].value_counts())

print("\nRegion Distribution:")
print(branches_df['region'].value_counts())

# =========================
# SAMPLE DATA
# =========================

print("\nSample Branch Data:")
print(branches_df.head())

# =========================
# EXPORT CSV
# =========================

output_path = "../data/synthetic/branches.csv"

branches_df.to_csv(output_path, index=False)

print("\n" + "=" * 60)
print("CSV FILE SUCCESSFULLY SAVED")
print(f"Location: {output_path}")
print("=" * 60)