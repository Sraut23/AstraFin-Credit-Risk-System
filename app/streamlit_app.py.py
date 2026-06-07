# =========================================================
# AstraFin Credit Services
# Streamlit Credit Risk Scoring App
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AstraFin Credit Risk Engine",
    layout="wide"
)

# =========================================================
# LOAD MODEL
# =========================================================

model = joblib.load(
    "../data/models/xgboost_model.pkl"
)

# =========================================================
# TITLE
# =========================================================

st.title("🏦 AstraFin Credit Risk Engine")

st.markdown(
    "Real-Time Probability of Default (PD) Scoring"
)

# =========================================================
# INPUTS
# =========================================================

col1, col2 = st.columns(2)

with col1:

    credit_score = st.number_input(
        "Credit Score",
        300,
        900,
        700
    )

    monthly_income = st.number_input(
        "Monthly Income",
        10000,
        1000000,
        50000
    )

    loan_amount = st.number_input(
        "Loan Amount",
        10000,
        5000000,
        300000
    )

    interest_rate = st.number_input(
        "Interest Rate",
        5.0,
        40.0,
        12.0
    )

    tenure_months = st.number_input(
        "Tenure (Months)",
        6,
        120,
        36
    )

    existing_loans = st.number_input(
        "Existing Loans",
        0,
        10,
        1
    )

with col2:

    total_outstanding = st.number_input(
        "Total Outstanding",
        0,
        5000000,
        100000
    )

    monthly_obligations = st.number_input(
        "Monthly Obligations",
        0,
        200000,
        10000
    )

    dti_ratio = st.number_input(
        "DTI Ratio",
        0.0,
        1.0,
        0.25
    )

    previous_defaults = st.number_input(
        "Previous Defaults",
        0,
        5,
        0
    )

    risk_band = st.selectbox(
        "Risk Band",
        [
            "Low",
            "Medium",
            "High",
            "Very High"
        ]
    )

    risk_profile = st.selectbox(
        "Risk Profile",
        [
            "Low Risk",
            "Medium Risk",
            "High Risk"
        ]
    )

customer_segment = st.selectbox(

    "Customer Segment",

    [
        "Private Salaried",
        "Government Salaried",
        "Self Employed",
        "SME Owner",
        "Freelancer",
        "New-to-Credit"
    ]

)

# =========================================================
# ENCODING
# =========================================================

risk_band_map = {
    "High":0,
    "Low":1,
    "Medium":2,
    "Very High":3
}

risk_profile_map = {
    "High Risk":0,
    "Low Risk":1,
    "Medium Risk":2
}

customer_segment_map = {
    "Freelancer":0,
    "Government Salaried":1,
    "New-to-Credit":2,
    "Private Salaried":3,
    "SME Owner":4,
    "Self Employed":5
}

# =========================================================
# PREDICT
# =========================================================

if st.button("Calculate Risk"):

    input_df = pd.DataFrame([{

        "credit_score":
            credit_score,

        "monthly_income":
            monthly_income,

        "loan_amount":
            loan_amount,

        "interest_rate":
            interest_rate,

        "tenure_months":
            tenure_months,

        "existing_loans":
            existing_loans,

        "total_outstanding":
            total_outstanding,

        "monthly_obligations":
            monthly_obligations,

        "dti_ratio":
            dti_ratio,

        "previous_defaults":
            previous_defaults,

        "risk_band":
            risk_band_map[risk_band],

        "risk_profile":
            risk_profile_map[risk_profile],

        "customer_segment":
            customer_segment_map[
                customer_segment
            ]
    }])

    pd_score = model.predict_proba(
        input_df
    )[0][1]

    # =====================================================
    # RISK GRADE
    # =====================================================

    if pd_score < 0.03:

        grade = "A"
        decision = "APPROVE"

    elif pd_score < 0.08:

        grade = "B"
        decision = "APPROVE"

    elif pd_score < 0.15:

        grade = "C"
        decision = "REVIEW"

    elif pd_score < 0.25:

        grade = "D"
        decision = "REVIEW"

    else:

        grade = "E"
        decision = "REJECT"

    # =====================================================
    # OUTPUT
    # =====================================================

    st.success("Scoring Completed")

    st.metric(
        "Probability of Default",
        f"{pd_score:.2%}"
    )

    st.metric(
        "Risk Grade",
        grade
    )

    st.metric(
        "Decision",
        decision
    )

    st.write("### Summary")

    st.write(
        f"""
        PD Score: {pd_score:.2%}

        Risk Grade: {grade}

        Recommendation: {decision}
        """
    )