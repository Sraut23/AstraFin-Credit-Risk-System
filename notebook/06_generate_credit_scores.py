# =========================================================
# AstraFin Credit Services
# Generate Credit Scores
# =========================================================

import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)

# =========================================================
# LOAD CUSTOMERS
# =========================================================

customers_df = pd.read_csv("../data/synthetic/customers.csv")

# =========================================================
# GENERATE CREDIT SCORES
# =========================================================

records = []

score_id = 1

for _, customer in customers_df.iterrows():

    customer_id = customer["customer_id"]
    risk_profile = customer["risk_profile"]

    score_pulls = random.randint(1, 3)

    for _ in range(score_pulls):

        if risk_profile == "Low":
            bureau_score = random.randint(720, 850)

        elif risk_profile == "Medium":
            bureau_score = random.randint(620, 780)

        else:
            bureau_score = random.randint(450, 700)

        records.append({
            "score_id": score_id,
            "customer_id": customer_id,
            "bureau_score": bureau_score,
            "score_date": fake.date_between(
                start_date="-5y",
                end_date="today"
            )
        })

        score_id += 1

# =========================================================
# DATAFRAME
# =========================================================

credit_scores_df = pd.DataFrame(records)

print("\nTotal Score Records:",
      len(credit_scores_df))

print("\nScore Distribution:")
print(
    credit_scores_df["bureau_score"]
    .describe()
)

# =========================================================
# EXPORT
# =========================================================

credit_scores_df.to_csv(
    "../data/synthetic/credit_scores.csv",
    index=False
)

print("\ncredit_scores.csv saved.")