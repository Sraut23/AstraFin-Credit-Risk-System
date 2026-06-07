# =========================================================
# AstraFin Credit Services
# Phase 3.9 - Write-Off Engine
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

loans_df = pd.read_csv(
    "../data/synthetic/loan_cashflows.csv"
)

collections_df = pd.read_csv(
    "../data/synthetic/collections.csv"
)

# =========================================================
# DEFAULTED LOANS ONLY
# =========================================================

defaulted_loans = loans_df[
    loans_df["loan_status"] == "Defaulted"
].copy()

print(
    f"\nDefaulted Loans: "
    f"{len(defaulted_loans):,}"
)

# =========================================================
# RECOVERY LOOKUP
# =========================================================

loan_recovery = (
    collections_df
    .groupby("loan_id")
    ["recovered_amount"]
    .sum()
    .reset_index()
)

defaulted_loans = defaulted_loans.merge(
    loan_recovery,
    on="loan_id",
    how="left"
)

defaulted_loans[
    "recovered_amount"
] = defaulted_loans[
    "recovered_amount"
].fillna(0)

# =========================================================
# GENERATE WRITEOFFS
# =========================================================

records = []

writeoff_id = 1

for _, row in defaulted_loans.iterrows():

    loan_amount = float(
        row["loan_amount"]
    )

    recovered = float(
        row["recovered_amount"]
    )

    # -------------------------------------
    # Outstanding Principal
    # -------------------------------------

    outstanding_principal = round(
        loan_amount *
        random.uniform(
            0.30,
            0.90
        ),
        2
    )

    # -------------------------------------
    # Write-Off Amount
    # -------------------------------------

    writeoff_amount = round(
        outstanding_principal *
        random.uniform(
            0.70,
            1.00
        ),
        2
    )

    # -------------------------------------
    # Recovery After Write-Off
    # -------------------------------------

    recovery_after_writeoff = round(
        writeoff_amount *
        random.uniform(
            0.05,
            0.35
        ),
        2
    )

    # -------------------------------------
    # Net Credit Loss
    # -------------------------------------

    net_credit_loss = round(
        writeoff_amount -
        recovery_after_writeoff,
        2
    )

    # -------------------------------------
    # LGD
    # -------------------------------------

    lgd = round(
        net_credit_loss /
        loan_amount,
        4
    )

    lgd = min(max(lgd, 0), 1)

    records.append({

        "writeoff_id":
            writeoff_id,

        "loan_id":
            row["loan_id"],

        "customer_id":
            row["customer_id"],

        "writeoff_date":
            pd.Timestamp.now()
            .date(),

        "loan_amount":
            loan_amount,

        "outstanding_principal":
            outstanding_principal,

        "writeoff_amount":
            writeoff_amount,

        "recovered_before_writeoff":
            recovered,

        "recovery_after_writeoff":
            recovery_after_writeoff,

        "net_credit_loss":
            net_credit_loss,

        "lgd":
            lgd

    })

    writeoff_id += 1

# =========================================================
# DATAFRAME
# =========================================================

writeoffs_df = pd.DataFrame(
    records
)

# =========================================================
# VALIDATION
# =========================================================

print("\n==========================")
print("WRITEOFF SUMMARY")
print("==========================")

print(
    f"\nWrite-Off Accounts: "
    f"{len(writeoffs_df):,}"
)

print("\nLGD Statistics")

print(
    writeoffs_df["lgd"]
    .describe()
)

print("\nTotal Write-Off Amount")

print(
    round(
        writeoffs_df[
            "writeoff_amount"
        ].sum(),
        2
    )
)

print("\nTotal Recovery After Write-Off")

print(
    round(
        writeoffs_df[
            "recovery_after_writeoff"
        ].sum(),
        2
    )
)

print("\nTotal Net Credit Loss")

print(
    round(
        writeoffs_df[
            "net_credit_loss"
        ].sum(),
        2
    )
)

# =========================================================
# EXPORT
# =========================================================

output_file = (
    "../data/synthetic/writeoffs.csv"
)

writeoffs_df.to_csv(
    output_file,
    index=False
)

print("\n==========================")
print("writeoffs.csv created")
print("==========================")

print(output_file)