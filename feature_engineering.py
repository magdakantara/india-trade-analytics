import pandas as pd
import numpy as np


INPUT_PATH = r"C:\Users\irene\OneDrive\Υπολογιστής\TuE\projects\india-trade-analytics\datasets\exports_cleaned.csv"
YEAR_FEATURES_OUTPUT = r"C:\Users\irene\OneDrive\Υπολογιστής\TuE\projects\india-trade-analytics\datasets\yearly_risk_features.csv"
COMMODITY_OUTPUT = r"C:\Users\irene\OneDrive\Υπολογιστής\TuE\projects\india-trade-analytics\datasets\commodity_volatility.csv"



df = pd.read_csv(INPUT_PATH)

# Total exports per year
yearly = (
    df.groupby("year")["value"]
    .sum()
    .reset_index()
    .rename(columns={"value": "total_exports"})
)

# Year-over-year growth
yearly["yoy_growth"] = yearly["total_exports"].pct_change()

# Rolling volatility (3-year window)
yearly["rolling_volatility"] = (
    yearly["total_exports"]
    .pct_change()
    .rolling(window=3)
    .std()
)


# Country Concentration (HHI)

country_year = (
    df.groupby(["year", "country"])["value"]
    .sum()
    .reset_index()
)

country_year["total_year"] = (
    country_year.groupby("year")["value"]
    .transform("sum")
)

country_year["country_share"] = (
    country_year["value"] / country_year["total_year"]
)

hhi = (
    country_year
    .groupby("year")["country_share"]
    .apply(lambda x: (x**2).sum())
    .reset_index(name="hhi")
)


# Merge Risk Features
risk_features = yearly.merge(hhi, on="year", how="left")

#  Shock Detection (Z-Score on Growth)
growth_mean = risk_features["yoy_growth"].mean()
growth_std = risk_features["yoy_growth"].std()

risk_features["growth_zscore"] = (
    (risk_features["yoy_growth"] - growth_mean) / growth_std
)

risk_features["shock_flag"] = (
    risk_features["growth_zscore"].abs() > 2
)


# Commodity Volatility
commodity_year = (
    df.groupby(["Commodity", "year"])["value"]
    .sum()
    .reset_index()
)

commodity_volatility = (
    commodity_year
    .groupby("Commodity")["value"]
    .std()
    .reset_index()
    .rename(columns={"value": "commodity_volatility"})
)


risk_features.to_csv(YEAR_FEATURES_OUTPUT, index=False)
commodity_volatility.to_csv(COMMODITY_OUTPUT, index=False)

print("Saved:", YEAR_FEATURES_OUTPUT)
print("Saved:", COMMODITY_OUTPUT)
