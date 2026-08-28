import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Raw data folder
RAW_DATA = BASE_DIR / "data" / "raw"

print("=" * 50)
print("UTILITY BILLING ETL - EXTRACT STAGE")
print("=" * 50)

# Read datasets
customers = pd.read_csv(RAW_DATA / "customers.csv")
billing = pd.read_csv(RAW_DATA / "billing_history.csv")
meter = pd.read_csv(RAW_DATA / "meter_reads.csv")
tariff = pd.read_csv(RAW_DATA / "tariff_rates.csv")

print("\nDatasets Loaded Successfully!\n")

print(f"Customers : {customers.shape}")
print(f"Billing   : {billing.shape}")
print(f"Meter     : {meter.shape}")
print(f"Tariff    : {tariff.shape}")

print("\nCustomer Sample\n")
print(customers.head())

print("\nBilling Sample\n")
print(billing.head())

print("\n" + "="*60)
print("CUSTOMER DATA PROFILE")
print("="*60)

print("\nColumns:")
print(customers.columns.tolist())

print("\nData Types:")
print(customers.dtypes)

print("\nMissing Values:")
print(customers.isnull().sum())

print("\nDuplicate Rows:")
print(customers.duplicated().sum())

print("\nStatistics:")
print(customers.describe(include="all"))