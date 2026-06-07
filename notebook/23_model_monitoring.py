# =========================================================
# AstraFin Credit Services
# Phase 4.7 - Model Monitoring Framework
# PSI Monitoring
# =========================================================

import pandas as pd
import numpy as np

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(
    "../data/synthetic/pd_model_dataset.csv"
)

# =========================================================
# CREATE BASELINE VS CURRENT
# =========================================================

# Historical Portfolio
baseline = df.sample(
    frac=0.50,
    random_state=42
)

# Current Portfolio
current = df.drop(
    baseline.index
)

print("\nBaseline Records:", len(baseline))
print("Current Records:", len(current))

# =========================================================
# PSI FUNCTION
# =========================================================

def calculate_psi(
    expected,
    actual,
    buckets=10
):

    breakpoints = np.percentile(
        expected,
        np.arange(
            0,
            buckets + 1
        ) / buckets * 100
    )

    expected_counts = pd.cut(
        expected,
        bins=breakpoints,
        include_lowest=True,
        duplicates="drop"
    ).value_counts(
        normalize=True
    )

    actual_counts = pd.cut(
        actual,
        bins=breakpoints,
        include_lowest=True,
        duplicates="drop"
    ).value_counts(
        normalize=True
    )

    psi = np.sum(

        (
            expected_counts -
            actual_counts
        )

        *

        np.log(

            (
                expected_counts + 1e-6
            )

            /

            (
                actual_counts + 1e-6
            )

        )

    )

    return round(
        psi,
        4
    )

# =========================================================
# NUMERIC FEATURES
# =========================================================

numeric_features = [

    "credit_score",
    "monthly_income",
    "loan_amount",
    "interest_rate",
    "tenure_months",
    "existing_loans",
    "total_outstanding",
    "monthly_obligations",
    "dti_ratio",
    "previous_defaults"

]

# =========================================================
# PSI CALCULATION
# =========================================================

psi_results = []

for feature in numeric_features:

    psi = calculate_psi(

        baseline[feature],

        current[feature]

    )

    if psi < 0.10:

        status = "Stable"

    elif psi < 0.25:

        status = "Moderate Shift"

    else:

        status = "Significant Drift"

    psi_results.append({

        "feature":
            feature,

        "psi":
            psi,

        "status":
            status

    })

# =========================================================
# PSI DATAFRAME
# =========================================================

psi_df = pd.DataFrame(
    psi_results
)

# =========================================================
# SUMMARY
# =========================================================

print("\n==========================")
print("PSI RESULTS")
print("==========================")

print(
    psi_df
)

print("\n==========================")
print("DRIFT SUMMARY")
print("==========================")

print(
    psi_df["status"]
    .value_counts()
)

# =========================================================
# OVERALL PORTFOLIO STATUS
# =========================================================

max_psi = psi_df["psi"].max()

if max_psi < 0.10:

    portfolio_status = "Stable"

elif max_psi < 0.25:

    portfolio_status = (
        "Moderate Shift"
    )

else:

    portfolio_status = (
        "Significant Drift"
    )

summary_df = pd.DataFrame({

    "portfolio_status":
        [portfolio_status],

    "max_psi":
        [max_psi],

    "features_monitored":
        [len(numeric_features)]

})

print("\nPortfolio Status")

print(summary_df)

# =========================================================
# EXPORT
# =========================================================

psi_df.to_csv(

    "../data/synthetic/psi_report.csv",

    index=False

)

summary_df.to_csv(

    "../data/synthetic/model_monitoring_summary.csv",

    index=False

)

print("\n==========================")
print("FILES CREATED")
print("==========================")

print("psi_report.csv")
print("model_monitoring_summary.csv")