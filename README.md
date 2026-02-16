# Trade Risk & Export Analytics System

## Overview

This project transforms raw export trade data into structured risk indicators that help assess:

- Country dependency exposure
- Sector instability
- Trade growth shocks
- Structural export concentration

Rather than focusing only on visualization, this project builds a small analytical pipeline that generates measurable trade risk features.

---

## Dataset

The dataset contains export records with the following fields:

- `HSCode` – Product classification code  
- `Commodity` – Product description  
- `value` – Export value  
- `country` – Destination country  
- `year` – Year of export  

Zero-value observations were removed to ensure economic validity.

---

## Project Pipeline

### 1. Data Cleaning
- Removal of missing and zero trade values
- Type correction
- Duplicate removal

Output: data/processed/export_cleaned.csv

---

### 2. Feature Engineering

The following trade risk indicators are computed:

#### Year-Level Features
- Total exports per year
- Year-over-year growth
- Rolling volatility (3-year window)
- Country concentration index (HHI)
- Growth shock detection (z-score based)

Output:
data/processed/yearly_risk_features.csv

#### Commodity-Level Features
- Standard deviation of export value per commodity

Output: data/processed/commodity_volatility.csv


---

## Key Risk Metrics

### 1. Country Concentration (HHI)
Measures export dependency on a limited number of countries.

Higher values indicate greater exposure to partner concentration risk.

---

### 2. Export Growth Volatility
Captures instability in total exports over time.

---

### 3. Shock Detection
Years with abnormal growth (|z-score| > 2) are flagged as potential trade shocks.

---

## Project Structure

data/
raw/
processed/
src/
feature_engineering.py
notebooks/
README.md


---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib / Seaborn

---

## Purpose

This project demonstrates how structured trade data can be transformed into actionable risk indicators relevant to:

- Trade analytics
- Supply chain exposure monitoring
- Market concentration assessment
- Economic trend analysis

It simulates a lightweight trade analytics engine rather than a simple visualization exercise.
