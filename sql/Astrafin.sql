SELECT current_database();

CREATE TABLE customers (

    customer_id INT PRIMARY KEY,

    first_name VARCHAR(100),
    last_name VARCHAR(100),

    gender VARCHAR(20),

    dob DATE,

    marital_status VARCHAR(50),

    occupation VARCHAR(100),

    employment_type VARCHAR(100),

    monthly_income NUMERIC(15,2),

    city VARCHAR(100),

    state VARCHAR(100),

    pincode VARCHAR(20),

    customer_since DATE,

    customer_segment VARCHAR(50),

    income_stability_score INT,

    employment_stability_score INT,

    future_default_propensity NUMERIC(10,4),

    risk_profile VARCHAR(50),

    education_level VARCHAR(100),

    years_at_current_job INT

);


CREATE TABLE loan_applications (

    application_id INT PRIMARY KEY,

    customer_id INT,

    product_id INT,

    application_date DATE,

    requested_amount NUMERIC(15,2),

    requested_tenure INT,

    application_channel VARCHAR(50),

    application_status VARCHAR(50),

    purpose VARCHAR(200)

);

CREATE TABLE loans (

    loan_id INT PRIMARY KEY,

    application_id INT,

    customer_id INT,

    product_id INT,

    branch_id INT,

    loan_amount NUMERIC(15,2),

    interest_rate NUMERIC(5,2),

    tenure_months INT,

    disbursement_date DATE,

    loan_status VARCHAR(50),

    risk_band VARCHAR(50),

    credit_score INT

);


SELECT COUNT(*) FROM branches;

DROP TABLE IF EXISTS branches;

CREATE TABLE branches (

    branch_id INT PRIMARY KEY,

    branch_name VARCHAR(200),

    city VARCHAR(100),

    state VARCHAR(100),

    region VARCHAR(50),

    manager_id NUMERIC,

    branch_open_date DATE,

    branch_category VARCHAR(50)

);

SELECT COUNT(*) FROM branches;


SELECT COUNT(*) FROM customers;


CREATE TABLE credit_scores (

    score_id INT PRIMARY KEY,

    customer_id INT,

    bureau_score INT,

    score_date DATE

);


CREATE TABLE risk_profile (

    profile_id INT PRIMARY KEY,

    customer_id INT,

    existing_loans INT,

    total_outstanding NUMERIC(15,2),

    monthly_obligations NUMERIC(15,2),

    dti_ratio NUMERIC(10,4),

    previous_defaults INT

);

SELECT COUNT(*) FROM risk_profile;


CREATE TABLE employees (

    employee_id INT PRIMARY KEY,

    employee_name VARCHAR(100),

    designation VARCHAR(100),

    branch_id INT,

    joining_date DATE,

    salary NUMERIC(12,2),

    experience_years INT,

    employee_grade VARCHAR(100)

);


CREATE TABLE loan_products (

    product_id INT PRIMARY KEY,

    product_name VARCHAR(100),

    min_amount NUMERIC(15,2),

    max_amount NUMERIC(15,2),

    min_interest_rate NUMERIC(5,2),

    max_interest_rate NUMERIC(5,2),

    max_tenure_months INT,

    risk_level VARCHAR(50),

    eligibility_income_multiplier INT,

    processing_fee_percent NUMERIC(5,2),

    default_probability_base NUMERIC(10,4),

    avg_interest_rate NUMERIC(5,2),

    max_amount_lakhs NUMERIC(10,2)

);


CREATE TABLE collection_agents (

    agent_id INT PRIMARY KEY,

    agent_name VARCHAR(100),

    branch_id INT,

    city VARCHAR(100),

    state VARCHAR(100),

    experience_years INT,

    specialization VARCHAR(100),

    recovery_capability_score INT,

    performance_tier VARCHAR(100),

    joining_date DATE

);

SELECT COUNT(*) FROM employees;
SELECT COUNT(*) FROM loan_products;
SELECT COUNT(*) FROM collection_agents;

select COUNT(*) as total_customers from customers;

select count(*) as total_application from loan_applications;

select count(*) as total_loans from loans;


-- approval Rate (59%)

select 
ROUND ( 100.0 * COUNT (distinct l.application_id)/
count (distinct a.application_id) )
as approval_rate
from loan_applications a
left join loans l 
on a.application_id = l.application_id;

-- Portfolio = All active loans given by the company (44,667,027,983)

select SUM(loan_amount)  as total_portfolio 
from loans ;

-- loand by risk band 

select risk_band,
count(*) as loans
from loans
group by risk_band 
order by loans desc;

-- portflio by product 

select p.product_name, sum(l.loan_amount) as portfolio
from loans l
join loan_products p
on l.product_id = p.product_id 
group by p.product_name 
order by portfolio desc;

--Top 10 Branches by Portfolio

select b.branch_name, sum(l.loan_amount) as portfolio
from loans l
join branches b
on b.branch_id = l.branch_id 
group by b.branch_name 
order by portfolio desc limit 10;

--Customers by Segment

SELECT
customer_segment,
COUNT(*) AS customers
FROM customers
GROUP BY customer_segment
ORDER BY customers DESC;


-- Average Income by Segment

select customer_segment, AVG (monthly_income) as avg_income
from customers
group by customer_segment
order by avg_income desc;


-- Applications by Status

SELECT
application_status,
COUNT(*) AS applications
FROM loan_applications
GROUP BY application_status
ORDER BY applications DESC;

-- Approval Rate by Product

select p.product_name,
round(100.0 * count(l.loan_id)/count(a.application_id),2) as approval_rate
from loan_applications a
join loan_products p 
on a.product_id = p.product_id 
left join loans l 
on a.application_id = l.application_id 
group by p.product_name;


SELECT
application_channel,
COUNT(*) AS applications
FROM loan_applications
GROUP BY application_channel
ORDER BY applications DESC;

-- application by channel 

select 
application_channel,
count(*) as applications
from loan_applications
group by application_channel
order by applications desc;


-- average loan amt by product 

select p.product_name, round(avg(l.loan_amount),2) as avg_Amt
from loans l
join loan_products p 
on p.product_id = l.product_id 
group by p.product_name 
order by avg_Amt desc;

-- Average Interest Rate by Product

SELECT
p.product_name,
ROUND(AVG(l.interest_rate),2) avg_rate
FROM loans l
JOIN loan_products p
ON l.product_id = p.product_id
GROUP BY p.product_name;

-- Top 10 Customers by Loan Amount

SELECT
customer_id,
SUM(loan_amount) total_loan
FROM loans
GROUP BY customer_id
ORDER BY total_loan DESC
LIMIT 10;

SELECT
p.product_name,
ROUND(AVG(l.tenure_months),2) avg_tenure
FROM loans l
JOIN loan_products p
ON l.product_id = p.product_id
GROUP BY p.product_name
order by avg_tenure desc;


-- branch productivity 

SELECT
b.branch_name,
COUNT(l.loan_id) loans_disbursed
FROM branches b
LEFT JOIN loans l
ON b.branch_id = l.branch_id
GROUP BY b.branch_name
ORDER BY loans_disbursed DESC;

-- Default Rate 

WITH loan_stats AS
(
    SELECT
        COUNT(*) AS total_loans,
        SUM(
            CASE
                WHEN loan_status='Defaulted'
                THEN 1
                ELSE 0
            END
        ) AS defaulted_loans
    FROM loans
)

SELECT
    total_loans,
    defaulted_loans,

    ROUND(
        100.0 * defaulted_loans / total_loans,
        2
    ) AS default_rate
FROM loan_stats;


-- Default Rate by Risk Band  (Which risk category defaults most?)

WITH risk_rate AS (
    SELECT
        risk_band,
        COUNT(*) AS total_loans,

        SUM(
            CASE
                WHEN loan_status = 'Defaulted'
                THEN 1
                ELSE 0
            END
        ) AS defaulted_loans

    FROM loans
    GROUP BY risk_band
)

SELECT
    risk_band,
    total_loans,
    defaulted_loans,

    ROUND(
        100.0 * defaulted_loans / total_loans,
        2
    ) AS default_rate

FROM risk_rate
ORDER BY default_rate DESC;

-- Default Rate by Customer Segment

with cust_seg as (
select c.customer_segment, count(*) as total_loans,
SUM(case
	when loan_status = 'Defaulted'
	then 1
	else 0
end
) as defaulted_rate
from loans l
join customers c
on c.customer_id =  l.customer_id
group by c.customer_segment 
)
select 
customer_segment,
    total_loans,
    defaulted_rate,
    ROUND(
        100.0 * defaulted_rate / total_loans,
        2
    ) AS default_rate
FROM cust_seg
ORDER BY default_rate DESC;

-- Default Rate by Product

with prod_rate as (select
p.product_name,count(*) as total_loans,
SUM(case
	when loan_status = 'Defaulted'
	then 1
	else 0
end
) as defaulted_loans
from loans l
join loan_products p
on l.product_id = p.product_id 
group by product_name
)
select product_name, total_loans, defaulted_loans,
round ( 100.0 * defaulted_loans / total_loans,2) as default_rate
from prod_rate
order by default_rate desc;

-- default rate by state

with state_rate as (select
b.state,count(*) as total_loans,
SUM(case
	when loan_status = 'Defaulted'
	then 1
	else 0
end
) as defaulted_loans
from loans l
join branches b
on l.branch_id = b.branch_id 
group by state
)
select state, total_loans, defaulted_loans,
round ( 100.0 * defaulted_loans / total_loans,2) as default_rate
from state_rate
order by default_rate desc;


-- Top 10 Riskiest Branches

WITH branch_defaults AS (

    SELECT

        b.branch_id,
        b.branch_name,

        COUNT(*) AS total_loans,

        SUM(
            CASE
                WHEN l.loan_status = 'Defaulted'
                THEN 1
                ELSE 0
            END
        ) AS defaulted_loans

    FROM loans l

    JOIN branches b
        ON l.branch_id = b.branch_id

    GROUP BY
        b.branch_id,
        b.branch_name

)

SELECT

    branch_id,
    branch_name,

    total_loans,

    defaulted_loans,

    ROUND(
        100.0 * defaulted_loans / total_loans,
        2
    ) AS default_rate

FROM branch_defaults

ORDER BY default_rate DESC

LIMIT 10;


-- Top 10 Riskiest Customers

SELECT

    c.customer_id,

    c.first_name,
    c.last_name,

    c.customer_segment,

    rp.previous_defaults,

    rp.dti_ratio,

    rp.total_outstanding,

    cs.bureau_score

FROM customers c

JOIN risk_profile rp
    ON c.customer_id = rp.customer_id

JOIN credit_scores cs
    ON c.customer_id = cs.customer_id

ORDER BY

    rp.previous_defaults DESC,

    rp.dti_ratio DESC,

    cs.bureau_score ASC

LIMIT 10;

-- credit assessment

CREATE TABLE credit_assessments (

    assessment_id INT PRIMARY KEY,
    application_id INT,
    credit_score INT,
    dti_ratio NUMERIC(10,4),
    risk_band VARCHAR(50),
    approval_probability NUMERIC(10,4),
    assessment_date DATE

);

DROP TABLE IF EXISTS credit_assessments;

CREATE TABLE credit_assessments (

    assessment_id INT PRIMARY KEY,

    application_id INT,

    credit_score INT,

    dti_ratio NUMERIC(10,4),

    risk_band VARCHAR(50),

    assessment_decision VARCHAR(50),

    assessment_date DATE,

    existing_loans INT,

    total_outstanding NUMERIC(15,2),

    monthly_obligations NUMERIC(15,2)

);

DROP TABLE IF EXISTS loan_cashflows;

CREATE TABLE loan_cashflows (

    loan_id INT PRIMARY KEY,

    application_id INT,

    customer_id INT,

    product_id INT,

    branch_id INT,

    loan_amount NUMERIC(15,2),

    interest_rate NUMERIC(5,2),

    tenure_months INT,

    disbursement_date DATE,

    loan_status VARCHAR(50),

    risk_band VARCHAR(50),

    credit_score INT,

    emi_amount NUMERIC(15,2),

    total_payment NUMERIC(15,2),

    total_interest NUMERIC(15,2)

);


CREATE TABLE emi_schedule (

    emi_id BIGINT PRIMARY KEY,

    loan_id INT,

    emi_number INT,

    due_date DATE,

    emi_amount NUMERIC(15,2),

    opening_balance NUMERIC(15,2),

    principal_component NUMERIC(15,2),

    interest_component NUMERIC(15,2),

    closing_balance NUMERIC(15,2),

    emi_status VARCHAR(50)

);



CREATE TABLE repayments (

    repayment_id BIGINT PRIMARY KEY,

    loan_id INT,

    emi_id BIGINT,

    payment_date DATE,

    amount_paid NUMERIC(15,2),

    payment_status VARCHAR(50),

    days_late INT,

    recovery_payment_flag BOOLEAN

);


CREATE TABLE dpd_status (

    repayment_id BIGINT PRIMARY KEY,

    loan_id INT,

    emi_id BIGINT,

    payment_date DATE,

    amount_paid NUMERIC(15,2),

    payment_status VARCHAR(50),

    days_late INT,

    recovery_payment_flag BOOLEAN,

    days_past_due INT,

    dpd_bucket VARCHAR(20),

    par30_flag INT,

    par60_flag INT,

    par90_flag INT,

    npa_flag INT

);



CREATE TABLE collections (

    collection_id BIGINT PRIMARY KEY,

    loan_id INT,

    emi_id BIGINT,

    days_past_due INT,

    dpd_bucket VARCHAR(20),

    agent_id INT,

    collection_strategy VARCHAR(100),

    contact_mode VARCHAR(50),

    promise_to_pay BOOLEAN,

    recovered_amount NUMERIC(15,2)

);


CREATE TABLE writeoffs (

    writeoff_id INT PRIMARY KEY,

    loan_id INT,

    customer_id INT,

    writeoff_date DATE,

    loan_amount NUMERIC(15,2),

    outstanding_principal NUMERIC(15,2),

    writeoff_amount NUMERIC(15,2),

    recovered_before_writeoff NUMERIC(15,2),

    recovery_after_writeoff NUMERIC(15,2),

    net_credit_loss NUMERIC(15,2),

    lgd NUMERIC(10,4)

);



CREATE TABLE expected_loss (

    loan_id INT PRIMARY KEY,

    application_id INT,

    customer_id INT,

    product_id INT,

    branch_id INT,

    loan_amount NUMERIC(15,2),

    interest_rate NUMERIC(5,2),

    tenure_months INT,

    disbursement_date DATE,

    loan_status VARCHAR(50),

    risk_band VARCHAR(50),

    credit_score INT,

    emi_amount NUMERIC(15,2),

    total_payment NUMERIC(15,2),

    total_interest NUMERIC(15,2),

    lgd NUMERIC(10,4),

    pd NUMERIC(10,6),

    ead NUMERIC(15,2),

    expected_loss NUMERIC(15,2),

    risk_grade VARCHAR(10)

);


SELECT *
FROM dpd_status
LIMIT 5;


-- PAR 30 

SELECT

    COUNT(*) AS total_accounts,

    SUM(par30_flag) AS par30_accounts,

    ROUND(
        100.0 * SUM(par30_flag) / COUNT(*),
        2
    ) AS par30_rate

FROM dpd_status;

-- PAR 60 

SELECT

    COUNT(*) AS total_accounts,

    SUM(par60_flag) AS par60_accounts,

    ROUND(
        100.0 * SUM(par60_flag) / COUNT(*),
        2
    ) AS par60_rate

FROM dpd_status;

-- PAR 90

SELECT

    COUNT(*) AS total_accounts,

    SUM(par90_flag) AS par90_accounts,

    ROUND(
        100.0 * SUM(par90_flag) / COUNT(*),
        2
    ) AS par90_rate

FROM dpd_status;

-- npa ratio (Non-Performing Asset Ratio) DPD >90
 
SELECT

    COUNT(*) AS total_accounts,

    SUM(npa_flag) AS npa_accounts,

    ROUND(
        100.0 * SUM(npa_flag) / COUNT(*),
        2
    ) AS npa_ratio

FROM dpd_status;


-- Collection Efficiency
-- How much money was recovered through collection efforts?

SELECT

    COUNT(*) AS total_collection_cases,

    SUM(recovered_amount) AS total_recovered_amount,

    ROUND(
        AVG(recovered_amount),
        2
    ) AS avg_recovery_per_case

FROM collections;


-- Recovery Rate

SELECT

    SUM(writeoff_amount) AS total_writeoff,

    SUM(recovery_after_writeoff) AS total_recovery,

    ROUND(
        100.0 *
        SUM(recovery_after_writeoff)
        /
        NULLIF(SUM(writeoff_amount),0),
        2
    ) AS recovery_rate

FROM writeoffs;

-- Write-Off Analysis
-- Which loans generated the biggest losses?

SELECT

    loan_id,

    customer_id,

    writeoff_amount,

    net_credit_loss,

    lgd

FROM writeoffs

ORDER BY net_credit_loss DESC

LIMIT 10;

-- writeoff level summary 

SELECT

    COUNT(*) AS writeoff_accounts,

    SUM(writeoff_amount) AS total_writeoff,

    SUM(net_credit_loss) AS total_credit_loss,

    ROUND(
        AVG(lgd),
        2
    ) AS avg_lgd

FROM writeoffs;


-- Expected Loss Analysis
-- PD  = Probability of Default
-- LGD = Loss Given Default
-- EAD = Exposure at Default

SELECT

    COUNT(*) AS total_loans,

    SUM(expected_loss) AS portfolio_expected_loss,

    ROUND(
        AVG(pd),
        4
    ) AS avg_pd,

    ROUND(
        AVG(lgd),
        4
    ) AS avg_lgd

FROM expected_loss;


-- Top 5 Customers by Loan Amount in Each State

WITH ranked_customers AS (

    SELECT

        c.state,

        c.customer_id,

        c.first_name,

        c.last_name,

        l.loan_amount,

        ROW_NUMBER() OVER (

            PARTITION BY c.state

            ORDER BY l.loan_amount DESC

        ) AS rn

    FROM customers c

    JOIN loans l

        ON c.customer_id = l.customer_id

)

SELECT *

FROM ranked_customers

WHERE rn <= 5

ORDER BY state, loan_amount DESC;


-- Rank Branches by Total Loan Portfolio

SELECT

    b.branch_name,

    SUM(l.loan_amount) AS portfolio,

    RANK() OVER (

        ORDER BY SUM(l.loan_amount) DESC

    ) AS branch_rank

FROM branches b

JOIN loans l

    ON b.branch_id = l.branch_id

GROUP BY b.branch_name;

-- Top 3 Riskiest Branches in Each State

WITH branch_risk AS (

    SELECT

        c.state,

        b.branch_name,

        COUNT(*) AS total_loans,

        SUM(

            CASE

                WHEN l.loan_status = 'Defaulted'

                THEN 1

                ELSE 0

            END

        ) AS defaults

    FROM loans l

    JOIN customers c

        ON l.customer_id = c.customer_id

    JOIN branches b

        ON l.branch_id = b.branch_id

    GROUP BY

        c.state,

        b.branch_name

),

ranked AS (

    SELECT *,

        RANK() OVER (

            PARTITION BY state

            ORDER BY defaults DESC

        ) AS rnk

    FROM branch_risk

)

SELECT *

FROM ranked

WHERE rnk <= 3;


-- Running Portfolio Growth

SELECT

    DATE_TRUNC(
        'month',
        disbursement_date
    ) AS month,

    SUM(loan_amount) AS monthly_disbursement,

    SUM(

        SUM(loan_amount)

    ) OVER (

        ORDER BY DATE_TRUNC(
            'month',
            disbursement_date
        )

    ) AS running_portfolio

FROM loans

GROUP BY 1

ORDER BY 1;

-- Loan Portfolio Summary View

CREATE OR REPLACE VIEW vw_loan_portfolio AS

SELECT

    l.loan_id,

    c.customer_id,

    c.first_name,

    c.last_name,

    c.state,

    p.product_name,

    l.loan_amount,

    l.interest_rate,

    l.loan_status,

    l.risk_band

FROM loans l

JOIN customers c

    ON l.customer_id = c.customer_id

JOIN loan_products p

    ON l.product_id = p.product_id;
    

SELECT *
FROM vw_loan_portfolio
LIMIT 10;
    
    
-- Default Analysis View
    
CREATE OR REPLACE VIEW vw_default_analysis AS

SELECT

    risk_band,

    COUNT(*) total_loans,

    SUM(

        CASE

            WHEN loan_status='Defaulted'

            THEN 1

            ELSE 0

        END

    ) default_loans,

    ROUND(

        100.0 *

        SUM(

            CASE

                WHEN loan_status='Defaulted'

                THEN 1

                ELSE 0

            END

        )

        /

        COUNT(*),

        2

    ) default_rate

FROM loans

GROUP BY risk_band;

SELECT *
FROM vw_default_analysis;


-- Expected Loss Dashboard View

CREATE OR REPLACE VIEW vw_expected_loss AS

SELECT

    risk_grade,

    COUNT(*) total_loans,

    SUM(expected_loss) portfolio_expected_loss,

    AVG(pd) avg_pd,

    AVG(lgd) avg_lgd

FROM expected_loss

GROUP BY risk_grade;

SELECT *
FROM vw_expected_loss;


