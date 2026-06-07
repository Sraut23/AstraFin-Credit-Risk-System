# AstraFin Credit Risk Management Platform

## Project Overview

AstraFin Credit Risk Management Platform is an end-to-end banking and lending analytics project that simulates the complete loan lifecycle, from loan application and credit assessment to default prediction, collections, recoveries, and portfolio monitoring.

The project combines PostgreSQL, SQL Analytics, Python, Machine Learning, Power BI, and Streamlit to demonstrate how banks and NBFCs evaluate credit risk and make lending decisions.

---

## Business Problem

Financial institutions face significant losses when high-risk customers default on loans. The objective of this project is to:

* Assess customer creditworthiness
* Predict probability of default (PD)
* Monitor portfolio risk
* Estimate expected losses
* Track collections and recoveries
* Provide executive-level dashboards for decision-making

---

## Project Architecture

Loan Applications → Credit Assessment → Loan Approval → Loan Servicing → Collections → Recoveries → Risk Monitoring → Executive Reporting

---

## Technology Stack

### Database

* PostgreSQL
* SQL

### Programming

* Python
* Pandas
* NumPy

### Machine Learning

* Logistic Regression
* XGBoost

### Visualization

* Power BI

### Application

* Streamlit

---

## Database Tables

### Master Data

* branches
* employees
* customers
* loan_products
* credit_scores
* risk_profile
* collection_agents

### Loan Origination

* loan_applications
* credit_assessments
* loans

### Loan Lifecycle

* emi_schedule
* repayments
* loan_cashflows
* dpd_status
* collections
* writeoffs
* expected_loss

---

## Credit Risk Metrics

### Portfolio Metrics

* Total Portfolio
* Average Loan Amount
* Approval Rate
* Portfolio by Product
* Portfolio by State

### Credit Risk Metrics

* Default Rate
* Default Rate by Product
* Default Rate by State
* Top Risky Customers
* Top Risky Branches
* PAR30
* PAR60
* PAR90
* NPA Ratio

### Collections Metrics

* Recovery Rate
* Collection Efficiency
* Write-Off Analysis
* Net Credit Loss

### Risk Modeling Metrics

* Probability of Default (PD)
* Loss Given Default (LGD)
* Exposure at Default (EAD)
* Expected Loss

---

## Machine Learning Pipeline

### Objective

Predict whether a customer will default on a loan.

### Features Used

* Credit Score
* Monthly Income
* Debt-to-Income Ratio (DTI)
* Risk Band
* Previous Defaults
* Loan Characteristics

### Models Trained

* Logistic Regression
* XGBoost

### Evaluation Metrics

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC

### Model Monitoring

* Feature Importance
* Population Stability Index (PSI)
* Champion Model Selection

---

## Power BI Dashboards

### Executive Dashboard

* Total Loans
* Total Customers
* Total Portfolio
* Expected Loss
* Portfolio Distribution

### Credit Risk Dashboard

* Default Rate
* Expected Loss
* Risk Grade Analysis
* Risk Band Analysis
* Recovery Analysis

### Collections Dashboard

* Recovery Performance
* Collection Efficiency
* Write-Off Monitoring
* Net Credit Loss

### Model Monitoring Dashboard

* Model Comparison
* Feature Importance
* PSI Monitoring
* Champion Model Summary

---

## Streamlit Application

The Streamlit application allows users to:

* Enter customer risk attributes
* Calculate probability of default
* Categorize customer risk
* Simulate loan approval decisions

---

## Key Skills Demonstrated

* PostgreSQL Database Design
* Advanced SQL Analytics
* Credit Risk Modeling
* Probability of Default (PD)
* Expected Loss Modeling
* Data Engineering
* Machine Learning
* XGBoost
* Power BI Dashboarding
* Business Intelligence
* Financial Analytics

---

## Project Outcome

Built a complete credit risk and lending analytics platform that simulates real-world banking workflows, including loan origination, risk assessment, default prediction, portfolio monitoring, collections analytics, and executive reporting.
