# Supplier Compliance & ESG Analyzer 🚗📦

A data-driven Python & Pandas project designed to clean, validate, and analyze supplier compliance, delivery performance, and ESG ratings (S-Rating) within an automotive supply chain. 

*Inspired by real-world logistics challenges at Skoda Auto (Volkswagen Group).*

---

## 🎯 Business Case & Objectives
In modern automotive supply chains, supply chain disruptions and ESG non-compliance can cost millions. This project automates the evaluation of raw, unstructured supplier databases by merging three distinct sources:
1. **Supplier Master Data:** Administrative registration details and DUNS numbers.
2. **ESG S-Rating Scores:** Environmental and social sustainability ratings (crucial automotive standard).
3. **Shipment Deliveries:** Transactional records of ordered vs. delivered parts, including lead times and defect quantities.

The system cleans the data, runs rigorous quality checks, calculates logistics KPIs, and automatically flags high-risk suppliers.

---

## 🛠️ Tech Stack & Skills Demonstrated
* **Python 3** (Core logic, custom validation functions)
* **Pandas** (Data merging, cleaning, string manipulation, clipping, and advanced `groupby` aggregations)
* **Matplotlib** (Automated generation of risk-visualizing charts)
* **Git & GitHub** (Version control and project management)

---

## 📊 Automated Pipeline Steps (How it Works)
1. **Data Loading & Merging:** Performs a relational multi-table `merge` (left-join) on `Supplier_ID`.
2. **Data Cleaning:** Trims whitespaces from vendor names, standardizes DUNS number formats, and handles missing values (`NaN` mapping to `Unknown`).
3. **Data Quality Validation:** Custom logic checks DUNS validity (exactly 9 digits) and registration completeness, flagging administrative errors.
4. **KPI Calculation:**
   * **Actual Lead Time:** Calculates elapsed days between order and delivery dates.
   * **On-Time Delivery (OTD %):** Percentage of shipments delivered within the target of 5 days.
   * **Defect Rate %:** Percentage of defective parts received out of total orders.
5. **ESG S-Rating & Risk Engine:** Automatically classifies suppliers into **Low**, **Medium**, and **High Risk** based on logistics, quality, and ESG thresholds. It safely handles `NaN` values to ensure missing certificates are flagged as Medium Risk.
6. **Data Export:** Saves the final structured dashboard to `data/supplier_compliance_report.csv`.
7. **Visualization:** Generates and saves a risk-coded bar chart under `plots/supplier_s_rating_chart.png`.

---

## 📈 Sample Executive Output
```text
==================================================
     EXECUTIVE SUPPLY CHAIN COMPLIANCE REPORT     
==================================================
Total Suppliers Analyzed: 8
🔴 High Risk Partners:   4 (Immediate Action Required)
🟡 Medium Risk Partners: 1 (Under Monitoring)
🟢 Low Risk Partners:    3 (Approved)
--------------------------------------------------
KEY CRITICAL FINDINGS:
1. Logistics Bottleneck: 'Bosch GmbH' has the worst On-Time Delivery rate (0.0%).
2. Quality Issue:        'Benteler Automotive' has the highest Defect Rate (5.00%).
3. High Risk Action List: Escalate contract reviews for: Bosch GmbH, Steel-Plast s.r.o., KautexTextron, Benteler Automotive
==================================================
🧠 Strategic Key Business Insights
Master Data Duplication Detected: Identified that Continental AG was registered under two different IDs (101 and 104), a classic ERP/SAP human-entry error.
Logistics Bottleneck: Both Bosch GmbH and Kautex Textron have an On-Time Delivery rate of 0% with average lead times exceeding 12 days, posing a severe threat to production line stability.
ESG Compliance Failure: Steel-Plast s.r.o. performs perfectly in delivery and quality, but is flagged as High Risk due to a critical S-Rating of 2.1, failing minimum sustainability compliance.
Quality Escalation: Benteler Automotive meets delivery targets but exhibits an unacceptable 5.00% Defect Rate, requiring immediate quality department intervention.
🚀 How to Run the Project
Clone this repository:
git clone https://github.com/your-username/supplier-esg-analyzer.git
cd supplier-esg-analyzer
Generate the raw test datasets:
python3 generate_data.py
Run the compliance analyzer:
python3 analyzer.py