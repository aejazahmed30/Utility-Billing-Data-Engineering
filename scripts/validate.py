import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA = BASE_DIR / "data" / "raw"

# Load data
customers = pd.read_csv(RAW_DATA / "customers.csv")
billing = pd.read_csv(RAW_DATA / "billing_history.csv")
meter = pd.read_csv(RAW_DATA / "meter_reads.csv")
tariff = pd.read_csv(RAW_DATA / "tariff_rates.csv")


def validate_dataframe(df, name):
    print("\n" + "=" * 60)
    print(f"VALIDATING {name.upper()}")
    print("=" * 60)

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nMissing Values")
    print(df.isnull().sum())

    print("\nDuplicate Rows")
    print(df.duplicated().sum())


validate_dataframe(customers, "customers")
validate_dataframe(billing, "billing")
validate_dataframe(meter, "meter")
validate_dataframe(tariff, "tariff")