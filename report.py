import os
import pandas as pd
import matplotlib.pyplot as plt

CLEAN_DATA_PATH = r"C:\Users\irene\OneDrive\Υπολογιστής\TuE\projects\india-trade-analytics\datasets\exports_cleaned.csv"
YEAR_FEATURES_PATH = r"C:\Users\irene\OneDrive\Υπολογιστής\TuE\projects\india-trade-analytics\datasets\yearly_risk_features.csv"
COM_VOL_PATH = r"C:\Users\irene\OneDrive\Υπολογιστής\TuE\projects\india-trade-analytics\datasets\commodity_volatility.csv"

REPORT_DIR = r"C:\Users\irene\OneDrive\Υπολογιστής\TuE\projects\india-trade-analytics\report"
PLOT_DIR = r'C:\Users\irene\OneDrive\Υπολογιστής\TuE\projects\india-trade-analytics\report\plots'

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)

# Load
df = pd.read_csv(CLEAN_DATA_PATH)
year_feat = pd.read_csv(YEAR_FEATURES_PATH)
com_vol = pd.read_csv(COM_VOL_PATH)

# Identify latest year

latest_year = int(df["year"].max())

# Executive summary (latest year row)
latest_row = year_feat[year_feat["year"] == latest_year].copy()

latest_row.to_csv(f"{REPORT_DIR}/executive_summary_latest_year.csv", index=False)


top_countries = (
    df[df["year"] == latest_year]
    .groupby("country")["value"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
    .rename(columns={"value": "export_value"})
)
top_countries.to_csv(f"{REPORT_DIR}/top_countries_{latest_year}.csv", index=False)


top_commodities = (
    df[df["year"] == latest_year]
    .groupby("Commodity")["value"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
    .rename(columns={"value": "export_value"})
)
top_commodities.to_csv(f"{REPORT_DIR}/top_commodities_{latest_year}.csv", index=False)


most_volatile = (
    com_vol.sort_values("commodity_volatility", ascending=False)
    .head(20)
)
most_volatile.to_csv(f"{REPORT_DIR}/most_volatile_commodities.csv", index=False)

# Plots reports

#  Total exports over time
plt.figure()
plt.plot(year_feat["year"], year_feat["total_exports"])
plt.title("Total Exports Over Time")
plt.xlabel("Year")
plt.ylabel("Total Export Value")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/total_exports_over_time.png", dpi=200)
plt.close()

#  HHI over time
plt.figure()
plt.plot(year_feat["year"], year_feat["hhi"])
plt.title("Country Concentration (HHI) Over Time")
plt.xlabel("Year")
plt.ylabel("HHI")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/hhi_over_time.png", dpi=200)
plt.close()

# YoY growth with shock flags
plt.figure()
plt.plot(year_feat["year"], year_feat["yoy_growth"])
shocks = year_feat[year_feat["shock_flag"] == True]
plt.scatter(shocks["year"], shocks["yoy_growth"])
plt.title("Year-over-Year Export Growth (Shocks Highlighted)")
plt.xlabel("Year")
plt.ylabel("YoY Growth")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/yoy_growth_shocks.png", dpi=200)
plt.close()

# Top countries bar (latest year)
plt.figure()
top_countries.sort_values("export_value").plot(x="country", y="export_value", kind="barh", legend=False)
plt.title(f"Top Export Destinations ({latest_year})")
plt.xlabel("Export Value")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/top_countries_{latest_year}.png", dpi=200)
plt.close()

# Top commodities bar
plt.figure()
top_commodities.sort_values("export_value").plot(x="Commodity", y="export_value", kind="barh", legend=False)
plt.title(f"Top Export Commodities ({latest_year})")
plt.xlabel("Export Value")
plt.ylabel("Commodity")
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/top_commodities_{latest_year}.png", dpi=200)
plt.close()

print("Saved CSV reports to:", REPORT_DIR)
print("Saved plots to:", PLOT_DIR)