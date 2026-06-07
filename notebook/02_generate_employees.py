# =========================================================
# AstraFin Credit Services
# Phase 3.1 - Employee Master Data Generation
# =========================================================

# =========================
# IMPORT LIBRARIES
# =========================

import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime

# =========================
# INITIALIZE
# =========================

fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)

# =========================
# LOAD BRANCHES DATA
# =========================

branches_df = pd.read_csv("../data/synthetic/branches.csv")

# =========================
# EMPLOYEE CONFIGURATION
# =========================

TOTAL_EMPLOYEES = 500

designations = {
    "Branch Manager": {
        "min_salary": 80000,
        "max_salary": 180000,
        "weight": 1
    },

    "Risk Analyst": {
        "min_salary": 60000,
        "max_salary": 140000,
        "weight": 2
    },

    "Loan Officer": {
        "min_salary": 35000,
        "max_salary": 80000,
        "weight": 5
    },

    "Collection Executive": {
        "min_salary": 25000,
        "max_salary": 50000,
        "weight": 4
    },

    "Operations Executive": {
        "min_salary": 30000,
        "max_salary": 60000,
        "weight": 3
    },

    "Relationship Manager": {
        "min_salary": 40000,
        "max_salary": 90000,
        "weight": 3
    }
}

# =========================
# GENERATE EMPLOYEES
# =========================

employees = []

employee_id = 1

# =========================================================
# STEP 1 → CREATE ONE BRANCH MANAGER PER BRANCH
# =========================================================

for idx, branch in branches_df.iterrows():

    joining_date = fake.date_between(
        start_date='-10y',
        end_date='-5y'
    )

    salary = random.randint(80000, 180000)

    employees.append({

        "employee_id": employee_id,

        "employee_name": fake.name(),

        "designation": "Branch Manager",

        "branch_id": branch["branch_id"],

        "joining_date": joining_date,

        "salary": salary,

        "experience_years": random.randint(8, 20),

        "employee_grade": random.choice([
            "Senior Management",
            "Middle Management"
        ])
    })

    # update manager_id in branches table
    branches_df.loc[idx, "manager_id"] = employee_id

    employee_id += 1

# =========================================================
# STEP 2 → GENERATE REMAINING EMPLOYEES
# =========================================================

remaining_employees = TOTAL_EMPLOYEES - len(branches_df)

designation_list = list(designations.keys())
designation_weights = [
    designations[d]["weight"]
    for d in designation_list
]

for _ in range(remaining_employees):

    designation = random.choices(
        designation_list,
        weights=designation_weights,
        k=1
    )[0]

    branch = branches_df.sample(1).iloc[0]

    min_salary = designations[designation]["min_salary"]
    max_salary = designations[designation]["max_salary"]

    # joining date logic
    if designation in ["Risk Analyst", "Branch Manager"]:

        joining_date = fake.date_between(
            start_date='-8y',
            end_date='-2y'
        )

        experience = random.randint(4, 12)

    else:

        joining_date = fake.date_between(
            start_date='-5y',
            end_date='today'
        )

        experience = random.randint(1, 8)

    salary = random.randint(min_salary, max_salary)

    # salary increase with experience
    salary += experience * random.randint(1000, 3000)

    # employee grade logic
    if salary >= 120000:
        grade = "Senior Management"

    elif salary >= 70000:
        grade = "Middle Management"

    else:
        grade = "Junior Management"

    employees.append({

        "employee_id": employee_id,

        "employee_name": fake.name(),

        "designation": designation,

        "branch_id": branch["branch_id"],

        "joining_date": joining_date,

        "salary": salary,

        "experience_years": experience,

        "employee_grade": grade
    })

    employee_id += 1

# =========================
# CREATE DATAFRAME
# =========================

employees_df = pd.DataFrame(employees)

# =========================
# VALIDATION
# =========================

print("\n" + "=" * 60)
print("EMPLOYEE DATA VALIDATION")
print("=" * 60)

print(f"\nTotal Employees: {employees_df.shape[0]}")

print("\nNull Values:")
print(employees_df.isnull().sum())

print("\nDuplicate Employee IDs:")
print(employees_df["employee_id"].duplicated().sum())

print("\nDesignation Distribution:")
print(employees_df["designation"].value_counts())

print("\nEmployee Grade Distribution:")
print(employees_df["employee_grade"].value_counts())

print("\nSalary Statistics:")
print(employees_df["salary"].describe())

# =========================
# SAMPLE DATA
# =========================

print("\nSample Employee Data:")
print(employees_df.head())

# =========================
# EXPORT CSV FILES
# =========================

employees_output = "../data/synthetic/employees.csv"
branches_output = "../data/synthetic/branches.csv"

employees_df.to_csv(employees_output, index=False)

# update branches with manager IDs
branches_df.to_csv(branches_output, index=False)

print("\n" + "=" * 60)
print("CSV FILES SUCCESSFULLY SAVED")
print("=" * 60)

print(f"\nEmployees File: {employees_output}")
print(f"Updated Branches File: {branches_output}")