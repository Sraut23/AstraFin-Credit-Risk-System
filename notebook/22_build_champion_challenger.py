# =========================================================
# AstraFin Credit Services
# Phase 4.6 - Champion Challenger Framework
# =========================================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

from sklearn.metrics import (
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score
)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(
    "../data/synthetic/pd_model_dataset.csv"
)

# =========================================================
# FEATURES
# =========================================================

target = "default_flag"

features = [

    "credit_score",
    "monthly_income",
    "loan_amount",
    "interest_rate",
    "tenure_months",
    "existing_loans",
    "total_outstanding",
    "monthly_obligations",
    "dti_ratio",
    "previous_defaults",
    "risk_band",
    "risk_profile",
    "customer_segment"

]

model_df = df[
    features + [target]
].copy()

# =========================================================
# ENCODE CATEGORICALS
# =========================================================

categorical_cols = [

    "risk_band",
    "risk_profile",
    "customer_segment"

]

for col in categorical_cols:

    le = LabelEncoder()

    model_df[col] = le.fit_transform(
        model_df[col]
    )

# =========================================================
# SPLIT
# =========================================================

X = model_df.drop(
    columns=[target]
)

y = model_df[target]

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

# =========================================================
# CLASS IMBALANCE
# =========================================================

negative_class = (
    y_train == 0
).sum()

positive_class = (
    y_train == 1
).sum()

scale_pos_weight = round(
    negative_class /
    positive_class,
    2
)

# =========================================================
# MODEL 1
# CHAMPION CANDIDATE
# =========================================================

log_model = LogisticRegression(

    max_iter=3000,

    class_weight="balanced",

    random_state=42

)

log_model.fit(
    X_train,
    y_train
)

log_probs = log_model.predict_proba(
    X_test
)[:,1]

log_preds = (
    log_probs >= 0.25
).astype(int)

# =========================================================
# MODEL 2
# CHALLENGER CANDIDATE
# =========================================================

xgb_model = XGBClassifier(

    n_estimators=300,

    max_depth=5,

    learning_rate=0.05,

    subsample=0.8,

    colsample_bytree=0.8,

    scale_pos_weight=scale_pos_weight,

    random_state=42,

    eval_metric="logloss"

)

xgb_model.fit(
    X_train,
    y_train
)

xgb_probs = xgb_model.predict_proba(
    X_test
)[:,1]

xgb_preds = (
    xgb_probs >= 0.20
).astype(int)

# =========================================================
# EVALUATION
# =========================================================

results = pd.DataFrame([

    {
        "model":"Logistic Regression",

        "roc_auc":
            roc_auc_score(
                y_test,
                log_probs
            ),

        "precision":
            precision_score(
                y_test,
                log_preds,
                zero_division=0
            ),

        "recall":
            recall_score(
                y_test,
                log_preds,
                zero_division=0
            ),

        "f1":
            f1_score(
                y_test,
                log_preds,
                zero_division=0
            )
    },

    {
        "model":"XGBoost",

        "roc_auc":
            roc_auc_score(
                y_test,
                xgb_probs
            ),

        "precision":
            precision_score(
                y_test,
                xgb_preds,
                zero_division=0
            ),

        "recall":
            recall_score(
                y_test,
                xgb_preds,
                zero_division=0
            ),

        "f1":
            f1_score(
                y_test,
                xgb_preds,
                zero_division=0
            )
    }

])

# =========================================================
# CHAMPION SELECTION
# =========================================================

champion = results.sort_values(
    by="roc_auc",
    ascending=False
).iloc[0]

# =========================================================
# RESULTS
# =========================================================

print("\n==========================")
print("MODEL COMPARISON")
print("==========================")

print(results)

print("\n==========================")
print("CHAMPION MODEL")
print("==========================")

print(
    champion["model"]
)

print(
    f"\nROC AUC: "
    f"{champion['roc_auc']:.4f}"
)

# =========================================================
# EXPORT
# =========================================================

results.to_csv(
    "../data/synthetic/model_comparison.csv",
    index=False
)

champion_df = pd.DataFrame(
    [champion]
)

champion_df.to_csv(
    "../data/synthetic/champion_model.csv",
    index=False
)

print("\n==========================")
print("FILES CREATED")
print("==========================")

print("model_comparison.csv")
print("champion_model.csv")