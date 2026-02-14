# Data-Analysis-Agent

## Overview
This project builds an **automated data science agent** that performs end-to-end **exploratory data analysis (EDA)** and **AutoML** with minimal human input.  
It replaces manual EDA workflows by orchestrating specialized agents over a compressed dataset representation using **ScaleDown**.

---

## Key Features
- Automated EDA for CSV, SQL, and Parquet data
- Profiling, visualization, and insight generation agents
- Anomaly detection and data quality checks
- Feature engineering suggestions
- Model recommendation and AutoML pipeline
- Auto-generated analysis reports

---

## Architecture
- **Ingestion Layer:** CSV / SQL / Parquet support  
- **ScaleDown Engine:** Compresses schema and statistics (~75% reduction)  
- **Agents:**  
  - Profiling Agent  
  - Visualization Agent  
  - Insight Generator  
  - Anomaly Detection Agent  
  - AutoML Agent  

---

## ScaleDown Benefits
- Reduces metadata size by ~75%
- Enables multi-table relationship analysis
- Cuts EDA time from hours to minutes
- Avoids repeated full-dataset scans

---

## Outputs
- Automated EDA reports
- Insight and anomaly summaries
- Feature engineering and model recommendations
- Productivity evaluation for data scientists

---

## Tech Stack
Python, Pandas/Polars, SQLAlchemy, Scikit-learn, Matplotlib/Seaborn

---

## License
MIT
