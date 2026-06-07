# =========================================================
# AstraFin Credit Services
# Phase 3.6 - Repayment Generation Engine
# =========================================================

import pandas as pd
import numpy as np
import random
import os

# =========================================================
# INITIALIZE
# =========================================================

random.seed(42)
np.random.seed(42)

# =========================================================
# LOAD FILES
# =========================================================

emi_df = pd.read_csv(
    "../data/synthetic/emi_schedule.csv"
)

loans_df = pd.read_csv(
    "../data/synthetic/loan_cashflows.csv"
)

# =========================================================
# LOAN STATUS LOOKUP
# =========================================================

loan_status_map = dict(
    zip(
        loans_df["loan_id"],
        loans_df["loan_status"]
    )
)

# =========================================================
# OUTPUT FILE
# =========================================================

output_file = (
    "../data/synthetic/repayments.csv"
)

if os.path.exists(output_file):
    os.remove(output_file)

# =========================================================
# CONFIG
# =========================================================

CHUNK_SIZE = 50000

repayment_id = 1

buffer = []

# =========================================================
# GENERATE REPAYMENTS
# =========================================================

for _, row in emi_df.iterrows():

    loan_id = row["loan_id"]

    emi_id = row["emi_id"]

    due_date = pd.to_datetime(
        row["due_date"]
    )

    emi_amount = float(
        row["emi_amount"]
    )

    loan_status = loan_status_map[
        loan_id
    ]

    # =====================================
    # CLOSED LOANS
    # =====================================

    if loan_status == "Closed":

        payment_status = random.choices(
            [
                "Paid On Time",
                "Paid Late"
            ],
            weights=[90, 10],
            k=1
        )[0]

        if payment_status == "Paid On Time":

            days_late = 0

        else:

            days_late = random.randint(
                1,
                15
            )

        amount_paid = emi_amount

    # =====================================
    # ACTIVE LOANS
    # =====================================

    elif loan_status == "Active":

        payment_status = random.choices(
            [
                "Paid On Time",
                "Paid Late",
                "Partial Payment",
                "Missed"
            ],
            weights=[
                70,
                15,
                10,
                5
            ],
            k=1
        )[0]

        if payment_status == "Paid On Time":

            amount_paid = emi_amount
            days_late = 0

        elif payment_status == "Paid Late":

            amount_paid = emi_amount

            days_late = random.randint(
                1,
                30
            )

        elif payment_status == "Partial Payment":

            amount_paid = round(
                emi_amount *
                random.uniform(
                    0.30,
                    0.80
                ),
                2
            )

            days_late = random.randint(
                5,
                45
            )

        else:

            amount_paid = 0

            days_late = random.randint(
                30,
                90
            )

    # =====================================
    # DEFAULTED LOANS
    # =====================================

    else:

        payment_status = random.choices(
            [
                "Missed",
                "Partial Payment",
                "Recovery Payment"
            ],
            weights=[
                65,
                25,
                10
            ],
            k=1
        )[0]

        if payment_status == "Recovery Payment":

            amount_paid = round(
                emi_amount *
                random.uniform(
                    0.50,
                    1.50
                ),
                2
            )

            days_late = random.randint(
                60,
                180
            )

        elif payment_status == "Partial Payment":

            amount_paid = round(
                emi_amount *
                random.uniform(
                    0.20,
                    0.70
                ),
                2
            )

            days_late = random.randint(
                30,
                120
            )

        else:

            amount_paid = 0

            days_late = random.randint(
                60,
                180
            )

    # =====================================
    # PAYMENT DATE
    # =====================================

    payment_date = (
        due_date +
        pd.Timedelta(days=days_late)
    )

    recovery_flag = (
        payment_status ==
        "Recovery Payment"
    )

    buffer.append({

        "repayment_id":
            repayment_id,

        "loan_id":
            loan_id,

        "emi_id":
            emi_id,

        "payment_date":
            payment_date,

        "amount_paid":
            amount_paid,

        "payment_status":
            payment_status,

        "days_late":
            days_late,

        "recovery_payment_flag":
            recovery_flag

    })

    repayment_id += 1

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
# FINAL WRITE
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

print("\n==========================")
print("REPAYMENTS CREATED")
print("==========================")

print(
    f"\nTotal Repayments: "
    f"{repayment_id - 1:,}"
)

print(
    "\nFile Saved:"
)

print(output_file)