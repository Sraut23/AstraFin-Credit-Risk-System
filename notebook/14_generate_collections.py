# =========================================================
# AstraFin Credit Services
# Phase 3.8 - Collections Engine
# =========================================================

import pandas as pd
import numpy as np
import random

# =========================================================
# INITIALIZE
# =========================================================

random.seed(42)
np.random.seed(42)

# =========================================================
# LOAD FILES
# =========================================================

dpd_df = pd.read_csv(
    "../data/synthetic/dpd_status.csv"
)

agents_df = pd.read_csv(
    "../data/synthetic/collection_agents.csv"
)

# =========================================================
# FILTER DELINQUENT ACCOUNTS
# =========================================================

collections_df = dpd_df[
    dpd_df["days_past_due"] > 0
].copy()

print(
    f"\nDelinquent Records: "
    f"{len(collections_df):,}"
)

# =========================================================
# COLLECTION STRATEGY
# =========================================================

def get_strategy(days):

    if days <= 30:

        return (
            "Reminder Call",
            "SMS"
        )

    elif days <= 60:

        return (
            "Collection Call",
            "Phone"
        )

    elif days <= 90:

        return (
            "Field Visit",
            "Visit"
        )

    else:

        return (
            "Recovery Action",
            "Legal Notice"
        )

# =========================================================
# GENERATE COLLECTIONS
# =========================================================

records = []

collection_id = 1

agent_ids = (
    agents_df["agent_id"]
    .tolist()
)

for _, row in collections_df.iterrows():

    days = row["days_past_due"]

    strategy, mode = get_strategy(days)

    assigned_agent = random.choice(
        agent_ids
    )

    promise_to_pay = random.choices(
        [True, False],
        weights=[65, 35],
        k=1
    )[0]

    # =====================================
    # RECOVERY PERCENTAGE
    # =====================================

    if days <= 30:

        recovery_pct = random.uniform(
            0.70,
            1.00
        )

    elif days <= 60:

        recovery_pct = random.uniform(
            0.40,
            0.90
        )

    elif days <= 90:

        recovery_pct = random.uniform(
            0.20,
            0.70
        )

    else:

        recovery_pct = random.uniform(
            0.05,
            0.40
        )

    # =====================================
    # FIXED RECOVERY AMOUNT LOGIC
    # =====================================

    base_amount = max(
        float(row["amount_paid"]),
        1000
    )

    recovered_amount = round(
        base_amount * recovery_pct,
        2
    )

    records.append({

        "collection_id":
            collection_id,

        "loan_id":
            row["loan_id"],

        "emi_id":
            row["emi_id"],

        "days_past_due":
            days,

        "dpd_bucket":
            row["dpd_bucket"],

        "agent_id":
            assigned_agent,

        "collection_strategy":
            strategy,

        "contact_mode":
            mode,

        "promise_to_pay":
            promise_to_pay,

        "recovered_amount":
            recovered_amount

    })

    collection_id += 1

# =========================================================
# CREATE DATAFRAME
# =========================================================

collections_result = pd.DataFrame(
    records
)

# =========================================================
# VALIDATION
# =========================================================

print("\n==========================")
print("COLLECTIONS SUMMARY")
print("==========================")

print(
    f"\nCollection Cases: "
    f"{len(collections_result):,}"
)

print("\nStrategy Distribution")

print(
    collections_result[
        "collection_strategy"
    ]
    .value_counts(normalize=True)
)

print("\nPromise To Pay")

print(
    collections_result[
        "promise_to_pay"
    ]
    .value_counts(normalize=True)
)

print("\nRecovery Amount Statistics")

print(
    collections_result[
        "recovered_amount"
    ]
    .describe()
)

print("\nTotal Recovery Amount")

print(
    round(
        collections_result[
            "recovered_amount"
        ].sum(),
        2
    )
)

# =========================================================
# EXPORT
# =========================================================

output_file = (
    "../data/synthetic/collections.csv"
)

collections_result.to_csv(
    output_file,
    index=False
)

print("\n==========================")
print("collections.csv created")
print("==========================")

print(output_file)