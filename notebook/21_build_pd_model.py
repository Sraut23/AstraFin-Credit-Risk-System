# =========================================================
# AstraFin Credit Services
# Phase 4.5 - PD Model Development (Improved)
# =========================================================

import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from xgboost import XGBClassifier

import joblib

# =========================================================
# CREATE FOLDERS
# =========================================================

Path("../data/models").mkdir(
    parents=True,
    exist_ok=True
)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(
    "../data/synthetic/pd_model_dataset.csv"
)

print("\nDataset Loaded")
print(df.shape)

# =========================================================
# TARGET
# =========================================================

target = "default_flag"

# =========================================================
# FEATURES
# =========================================================

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

# =========================================================
# MODEL DATA
# =========================================================

model_df = df[
    features + [target]
].copy()

# =========================================================
# LABEL ENCODING
# =========================================================

categorical_cols = [

    "risk_band",
    "risk_profile",
    "customer_segment"

]

encoders = {}

for col in categorical_cols:

    le = LabelEncoder()

    model_df[col] = le.fit_transform(
        model_df[col]
    )

    encoders[col] = le

# =========================================================
# X / Y
# =========================================================

X = model_df.drop(
    columns=[target]
)

y = model_df[target]

# =========================================================
# SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

print("\nTrain Shape")
print(X_train.shape)

print("\nTest Shape")
print(X_test.shape)

# =========================================================
# CLASS IMBALANCE
# =========================================================

negative_class = (y_train == 0).sum()
positive_class = (y_train == 1).sum()

scale_pos_weight = round(
    negative_class / positive_class,
    2
)

print("\nScale Pos Weight")
print(scale_pos_weight)

# =========================================================
# LOGISTIC REGRESSION
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

# =========================================================
# LOGISTIC PREDICTIONS
# =========================================================

log_probs = log_model.predict_proba(
    X_test
)[:,1]

# Lower threshold for imbalanced portfolio
log_preds = (
    log_probs >= 0.25
).astype(int)

# =========================================================
# LOGISTIC METRICS
# =========================================================

print("\n========================")
print("LOGISTIC REGRESSION")
print("========================")

print(
    "ROC AUC:",
    round(
        roc_auc_score(
            y_test,
            log_probs
        ),
        4
    )
)

print(
    "Precision:",
    round(
        precision_score(
            y_test,
            log_preds
        ),
        4
    )
)

print(
    "Recall:",
    round(
        recall_score(
            y_test,
            log_preds
        ),
        4
    )
)

print(
    "F1:",
    round(
        f1_score(
            y_test,
            log_preds
        ),
        4
    )
)

print("\nConfusion Matrix")

print(
    confusion_matrix(
        y_test,
        log_preds
    )
)

# =========================================================
# XGBOOST
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

# =========================================================
# XGB PREDICTIONS
# =========================================================

xgb_probs = xgb_model.predict_proba(
    X_test
)[:,1]

# Lower threshold
xgb_preds = (
    xgb_probs >= 0.20
).astype(int)

# =========================================================
# XGB METRICS
# =========================================================

print("\n========================")
print("XGBOOST")
print("========================")

print(
    "ROC AUC:",
    round(
        roc_auc_score(
            y_test,
            xgb_probs
        ),
        4
    )
)

print(
    "Precision:",
    round(
        precision_score(
            y_test,
            xgb_preds,
            zero_division=0
        ),
        4
    )
)

print(
    "Recall:",
    round(
        recall_score(
            y_test,
            xgb_preds,
            zero_division=0
        ),
        4
    )
)

print(
    "F1:",
    round(
        f1_score(
            y_test,
            xgb_preds,
            zero_division=0
        ),
        4
    )
)

print("\nConfusion Matrix")

print(
    confusion_matrix(
        y_test,
        xgb_preds
    )
)

# =========================================================
# FEATURE IMPORTANCE
# =========================================================

importance_df = pd.DataFrame({

    "feature":
        X.columns,

    "importance":
        xgb_model.feature_importances_

})

importance_df = importance_df.sort_values(
    by="importance",
    ascending=False
)

print("\n========================")
print("TOP FEATURES")
print("========================")

print(
    importance_df.head(15)
)

# =========================================================
# SAVE MODELS
# =========================================================

joblib.dump(
    log_model,
    "../data/models/logistic_model.pkl"
)

joblib.dump(
    xgb_model,
    "../data/models/xgboost_model.pkl"
)

# =========================================================
# SAVE PREDICTIONS
# =========================================================

prediction_df = X_test.copy()

prediction_df["actual_default"] = y_test.values

prediction_df["logistic_pd"] = log_probs

prediction_df["xgb_pd"] = xgb_probs

prediction_df.to_csv(
    "../data/synthetic/pd_predictions.csv",
    index=False
)

# =========================================================
# SAVE FEATURE IMPORTANCE
# =========================================================

importance_df.to_csv(
    "../data/synthetic/feature_importance.csv",
    index=False
)

# =========================================================
# COMPLETE
# =========================================================

print("\n========================")
print("FILES CREATED")
print("========================")

print("pd_predictions.csv")
print("feature_importance.csv")
print("logistic_model.pkl")
print("xgboost_model.pkl")