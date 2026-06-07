# =========================================================
# AstraFin Credit Services
# Phase 3.5 - EMI Schedule Generation
# Enterprise Chunk-Based Version
# =========================================================

import pandas as pd
import numpy as np
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import os

# =========================================================
# LOAD DATA
# =========================================================

loans_df = pd.read_csv(
    "../data/synthetic/loan_cashflows.csv"
)

# =========================================================
# OUTPUT FILE
# =========================================================

output_file = (
    "../data/synthetic/emi_schedule.csv"
)

# remove old file if exists
if os.path.exists(output_file):
    os.remove(output_file)

# =========================================================
# CONFIG
# =========================================================

CHUNK_SIZE = 50000

emi_id = 1
buffer = []

# =========================================================
# GENERATE EMI SCHEDULE
# =========================================================

for index, row in loans_df.iterrows():

    loan_id = row["loan_id"]

    principal = float(row["loan_amount"])

    annual_rate = float(
        row["interest_rate"]
    )

    monthly_rate = (
        annual_rate / 12 / 100
    )

    tenure = int(
        row["tenure_months"]
    )

    emi_amount = float(
        row["emi_amount"]
    )

    disbursement_date = pd.to_datetime(
        row["disbursement_date"]
    )

    outstanding = principal

    for emi_no in range(
        1,
        tenure + 1
    ):

        opening_balance = round(
            outstanding,
            2
        )

        interest_component = round(
            outstanding *
            monthly_rate,
            2
        )

        principal_component = round(
            emi_amount -
            interest_component,
            2
        )

        closing_balance = round(
            outstanding -
            principal_component,
            2
        )

        if closing_balance < 0:
            closing_balance = 0

        due_date = (
            disbursement_date +
            relativedelta(
                months=emi_no
            )
        )

        buffer.append({

            "emi_id":
                emi_id,

            "loan_id":
                loan_id,

            "emi_number":
                emi_no,

            "due_date":
                due_date,

            "emi_amount":
                emi_amount,

            "opening_balance":
                opening_balance,

            "principal_component":
                principal_component,

            "interest_component":
                interest_component,

            "closing_balance":
                closing_balance,

            "emi_status":
                "Scheduled"

        })

        emi_id += 1

        outstanding = closing_balance

        # =====================================
        # WRITE CHUNK
        # =====================================

        if len(buffer) >= CHUNK_SIZE:

            chunk_df = pd.DataFrame(
                buffer
            )

            write_header = (
                not os.path.exists(
                    output_file
                )
            )

            chunk_df.to_csv(
                output_file,
                mode="a",
                index=False,
                header=write_header
            )

            print(
                f"Written "
                f"{len(chunk_df):,} rows"
            )

            buffer = []

# =========================================================
# WRITE REMAINING RECORDS
# =========================================================

if len(buffer) > 0:

    chunk_df = pd.DataFrame(
        buffer
    )

    write_header = (
        not os.path.exists(
            output_file
        )
    )

    chunk_df.to_csv(
        output_file,
        mode="a",
        index=False,
        header=write_header
    )

    print(
        f"Written final "
        f"{len(chunk_df):,} rows"
    )

# =========================================================
# SUMMARY
# =========================================================

print("\n============================")
print("EMI SCHEDULE CREATED")
print("============================")

print(
    f"\nTotal EMI Records: "
    f"{emi_id - 1:,}"
)

print(
    f"\nFile Saved:"
)
print(output_file)