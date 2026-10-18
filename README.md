# Capstone_Project_Omkarsawant
Mamaearth-Returns-Growth-Intelligence
Repository Structure
Mamaearth-Returns-Growth-Intelligence/
│
├── README.md
│
├── sql/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── reports.sql
│
├── data/
│   ├── customers.csv
│   ├── products.csv
│   └── orders.csv
│
├── analysis/
│   ├── clean_and_eda.py
│   └── visualize.py
│
├── visualizations/
│   ├── return_rate_by_payment.png
│   └── monthly_revenue_trend.png
│
└── narrator/



End-to-End Pipeline Flow
Plain Text
customers.csv
products.csv
orders.csv
│
▼
SQL Layer
(schema.sql + seed_data.sql + reports.sql)
│
▼
Python Analytics Layer
(clean_and_eda.py)
│
├── Cleaned metrics
├── Reconciliation outputs
├── Segmentation outputs
├── Correlation outputs
└── findings.json
│
▼
Visualization Layer
(visualize.py)
│
├── return_rate_by_payment.png
└── monthly_revenue_trend.png
│
▼
GenAI Narrator
(generate_narrative.py)
│
├── Gemini API Path
└── Offline Fallback Path
│
▼
SCR Executive Narrative
Technology Stack
Database
SQLite
Analytics
Python 3.x
Pandas
NumPy
Visualizations
Matplotlib
AI Layer
Google Gemini
google-genai SDK
Installation
Clone Repository
Shell
git clone https://github.com/<your-username>/mamaearth-returns-growth-intelligence.git
 
cd mamaearth-returns-growth-intelligence
Create Virtual Environment
Windows
Shell
python -m venv venv
 
venv\Scripts\activate
Linux / macOS
Shell
python -m venv venv
 
source venv/bin/activate
Install Dependencies
Shell
pip install pandas numpy matplotlib google-genai
PART 1 — SQL Relational Layer

The SQL layer creates the database schema, loads source data, and produces reporting outputs.

Step 1: Create SQLite Database
Shell
sqlite3 mamaearth.db
Step 2: Run Schema

Creates:

customers
products
orders
Shell
sqlite3 mamaearth.db < sql/schema.sql
Step 3: Load Seed Data

Load all records from:

customers.csv
products.csv
orders.csv
Shell
sqlite3 mamaearth.db < sql/seed_data.sql
Step 4: Validate Record Counts

Execute:

SQL
SELECT COUNT(*) FROM customers;

Expected:

Plain Text
45

Execute:

SQL
SELECT COUNT(*) FROM products;

Expected:

Plain Text
16

Execute:

SQL
SELECT COUNT(*) FROM orders;

Expected:

Plain Text
180
Step 5: Run Reports
Shell
sqlite3 mamaearth.db < sql/reports.sql
Reports Generated
Order Totals

Expected:

Plain Text
total_orders = 180
 
total_revenue = 99860.20
 
avg_order_value = 554.78
Missing Ratings

Expected:

Plain Text
COUNT(*) = 180
 
COUNT(rating) = 165
 
missing = 15
Customers With Zero Orders

Expected:

Plain Text
C045
Vihaan
Cities With Return Rate > 20%

Expected:

Plain Text
Jaipur 42.1%
Lucknow 30.6%
Bangalore 24.2%
Top Customers By Spending

Expected Top Customer:

Plain Text
C043 Reyansh
₹12920.00
Revenue By Category

Expected:

Plain Text
Haircare ₹44956.10
Skincare ₹27346.00
Babycare ₹16805.00
PersonalCare ₹10753.10
PART 2 — Python Analytics Layer

This stage operates directly on the raw CSV files and is independent of the database.

Run Analytics Pipeline
Shell
python analysis/clean_and_eda.py
Cleaning Performed
Payment Method Standardization

Before cleaning:

Plain Text
COD
cod
Card
card
CARD
UPI
upi

After cleaning:

Plain Text
CARD = 70
 
COD = 55
 
UPI = 55
Duplicate Removal

Natural key:

Plain Text
customer_id
product_id
order_date
quantity
discount_pct
payment_method
rating
returned

Dropped Orders:

Plain Text
O0176
O0177
O0178
O0179
O0180

Resulting Shape:

Plain Text
(175, 9)
Missing Value Treatment
Discount
Plain Text
NaN → 0

Affected Rows:

Plain Text
12
Rating

Imputed with median:

Plain Text
3.0
 

Affected Rows:

Plain Text
15
Revenue Reconciliation

Raw Revenue:

Plain Text
₹99,860.20
``

Cleaned Revenue:

Plain Text
₹97,358.30

Difference:

Plain Text
₹2,501.90

The entire reconciliation difference is caused by the five duplicated orders removed during cleaning.

Outlier Detection

Method:

Plain Text
IQR Method

Expected:

Plain Text
Q1 = 1
 
Q3 = 2
 
IQR = 1
 
Lower = -0.5
 
Upper = 3.5
 

Outlier Orders:

Plain Text
O0011
(quantity 25)
 
O0098
(quantity 30)

These records are flagged but not deleted.

Return Rate Analysis

Hypothesis:

Plain Text
COD has a higher return rate than other payment methods.

Result:

Plain Text
CARD = 14.7%
 
COD = 44.4%
 
UPI = 18.9%

Conclusion:

Plain Text
Confirmed
Multi-Level Segmentation

Grouping:

Python
payment_method
city_tier

Highest Risk Segment:

Plain Text
COD + Tier-2 Cities
 
54.5%
Correlation Analysis

Variables:

Plain Text
rating
returned
discount_pct
quantity

Result:

Plain Text
All pairwise correlations are negligible.

Business Conclusion:

Plain Text
"Higher discounts reduce returns"

Status:

Plain Text
Busted
Outlier-Corrected Monthly Revenue

True Monthly Revenue:

Plain Text
2026-01 11637.10
 
2026-02 13195.50
 
2026-03 20318.90
 
2026-04 9495.30
 
2026-05 13151.10
 
2026-06 11615.40
``

Finding:

Plain Text
January appears highest only due to two bulk outlier orders.
 
After removing outlier influence,
March becomes the true peak month.
findings.json Generation

At the end of the analytics pipeline, the script automatically creates:

Plain Text
narrator/findings.json

This file becomes the input for the GenAI layer.

No values are manually entered.

PART 2 Visualization Layer

After analytics completes:

Shell
python analysis/visualize.py
Generated Charts
1. Return Rate by Payment Method

File:

Plain Text
visualizations/return_rate_by_payment.png

Shows:

Plain Text
CARD vs COD vs UPI

with exact percentages displayed on bars.

2. Monthly Revenue Trend

File:

Plain Text
visualizations/monthly_revenue_trend.png

Uses:

Plain Text
Outlier-corrected revenue

Peak month:

Plain Text
March 2026
PART 3 — GenAI Insight Narrator

The AI layer transforms validated findings into an executive business summary.

Input:

Plain Text
narrator/findings.json

Output:

Plain Text
SCR Narrative
Running With Gemini API
Set Environment Variable
Windows
Shell
set GEMINI_API_KEY=your_api_key_here
``
Linux/macOS
Shell
export GEMINI_API_KEY=your_api_key_here
``
Run Narrative Generator
Shell
python narrator/generate_narrative.py
Offline Mode (No API Key Required)

If:

Plain Text
GEMINI_API_KEY is not set

or

Plain Text
Gemini request fails

the application automatically switches to:

Python
generate_scr_narrative_offline()

Benefits:

No API cost
No internet required
Fully reproducible
Fully gradable

Run exactly the same command:

Shell
python narrator/generate_narrative.py

No configuration is required.

Required Metrics Included In Narrative

The generated narrative must contain:

Plain Text
97,358.30
``

Cleaned Revenue

Plain Text
44.4
``

COD Return Rate

Plain Text
54.5
``

Highest Risk Segment Return Rate

Plain Text
2,501.90

Duplicate Reconciliation Delta

Plain Text
March

and

Plain Text
20,318.90

True Peak Month Revenue

Reproducibility Checklist

Follow the steps below in sequence:

Shell
# SQL Layer
sqlite3 mamaearth.db < sql/schema.sql
sqlite3 mamaearth.db < sql/seed_data.sql
sqlite3 mamaearth.db < sql/reports.sql
 
# Analytics Layer
python analysis/clean_and_eda.py
 
# Visualization Layer
python analysis/visualize.py
 
# GenAI Layer
python narrator/generate_narrative.py

Running the above sequence from raw source files will reproduce:

SQL reports
Data cleaning results
Revenue reconciliation
Segmentation findings
Correlation analysis
Visualizations
findings.json
SCR business narrative

without any manual intervention.

Key Business Findings
Cleaned revenue is ₹97,358.30.
Raw revenue is ₹99,860.20.
The ₹2,501.90 difference is entirely caused by duplicate orders.
COD has the highest return rate at 44.4%.
COD orders in Tier‑2 cities are the highest-risk segment at 54.5% returns.
Bulk-order outliers distort monthly performance reporting.
After correcting for outliers, March 2026 is the true revenue peak month at ₹20,318.90.
Discount percentage shows negligible correlation with returns.
    ├── findings.json
    ├── generate_narrative.py
    └── sample_output.txt
