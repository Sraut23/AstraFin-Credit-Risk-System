# =========================================================
# AstraFin Credit Services
# Generate Risk Profiles
# =========================================================

import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

# =========================================================
# LOAD CUSTOMERS
# =========================================================

customers_df = pd.read_csv(
    "../data/synthetic/customers.csv"
)

# =========================================================
# GENERATE RISK PROFILE
# =========================================================

profiles = []

profile_id = 1

for _, customer in customers_df.iterrows():

    income = customer["monthly_income"]
    risk_profile = customer["risk_profile"]

    if risk_profile == "Low":

        existing_loans = random.randint(0, 2)
        previous_defaults = 0

    elif risk_profile == "Medium":

        existing_loans = random.randint(0, 4)
        previous_defaults = random.randint(0, 1)

    else:

        existing_loans = random.randint(1, 5)
        previous_defaults = random.randint(0, 3)

    monthly_obligations = round(
        income * random.uniform(0.05, 0.60),
        0
    )

    dti_ratio = round(
        monthly_obligations / income,
        2
    )

    total_outstanding = round(
        monthly_obligations *
        random.randint(10, 40),
        0
    )

    profiles.append({

        "profile_id": profile_id,

        "customer_id": customer["customer_id"],

        "existing_loans": existing_loans,

        "total_outstanding":
            total_outstanding,

        "monthly_obligations":
            monthly_obligations,

        "dti_ratio":
            dti_ratio,

        "previous_defaults":
            previous_defaults

    })

    profile_id += 1

# =========================================================
# DATAFRAME
# =========================================================

risk_profile_df = pd.DataFrame(profiles)

print("\nTotal Profiles:",
      len(risk_profile_df))

print("\nDTI Distribution:")
print(
    risk_profile_df["dti_ratio"]
    .describe()
)

# =========================================================
# EXPORT
# =========================================================

risk_profile_df.to_csv(
    "../data/synthetic/risk_profile.csv",
    index=False
)

print("\nrisk_profile.csv saved.")