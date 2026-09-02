import pandas as pd
from pathlib import Path


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA = BASE_DIR / "data" / "raw"
PROCESSED_DATA = BASE_DIR / "data" / "processed"


# Create processed directory if it does not exist
PROCESSED_DATA.mkdir(parents=True, exist_ok=True)


print("=" * 60)
print("UTILITY BILLING ETL - TRANSFORM STAGE")
print("=" * 60)


# Load raw datasets
customers = pd.read_csv(RAW_DATA / "customers.csv")
billing = pd.read_csv(RAW_DATA / "billing_history.csv")
meter = pd.read_csv(RAW_DATA / "meter_reads.csv")
tariff = pd.read_csv(RAW_DATA / "tariff_rates.csv")


print("\nRaw datasets loaded successfully!")

print(f"Customers : {customers.shape}")
print(f"Billing   : {billing.shape}")
print(f"Meter     : {meter.shape}")
print(f"Tariff    : {tariff.shape}")


# ---------------------------------------------------------
# 1. Standardize column names
# ---------------------------------------------------------

def standardize_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


customers = standardize_columns(customers)
billing = standardize_columns(billing)
meter = standardize_columns(meter)
tariff = standardize_columns(tariff)


print("\nColumn names standardized.")


# ---------------------------------------------------------
# 2. Remove duplicate rows
# ---------------------------------------------------------

print("\nDuplicate rows before cleaning:")

print(f"Customers : {customers.duplicated().sum()}")
print(f"Billing   : {billing.duplicated().sum()}")
print(f"Meter     : {meter.duplicated().sum()}")
print(f"Tariff    : {tariff.duplicated().sum()}")


customers = customers.drop_duplicates()
billing = billing.drop_duplicates()
meter = meter.drop_duplicates()
tariff = tariff.drop_duplicates()


print("\nDuplicate rows removed.")


# ---------------------------------------------------------
# 3. Clean string columns
# ---------------------------------------------------------

def clean_string_columns(df):
    for column in df.select_dtypes(include="str").columns:
        df[column] = df[column].str.strip()

    return df


customers = clean_string_columns(customers)
billing = clean_string_columns(billing)
meter = clean_string_columns(meter)
tariff = clean_string_columns(tariff)


print("String columns cleaned.")


# ---------------------------------------------------------
# 4. Convert date/time columns
# ---------------------------------------------------------

def convert_date_columns(df):
    for column in df.columns:

        if (
            "date" in column.lower()
            or "time" in column.lower()
            or column.lower() in ["created_at", "updated_at", "last_updated"]
        ):
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    return df


customers = convert_date_columns(customers)
billing = convert_date_columns(billing)
meter = convert_date_columns(meter)
tariff = convert_date_columns(tariff)


print("Date/time columns converted.")


# ---------------------------------------------------------
# 5. Save processed datasets
# ---------------------------------------------------------

customers.to_csv(
    PROCESSED_DATA / "customers_clean.csv",
    index=False
)

billing.to_csv(
    PROCESSED_DATA / "billing_history_clean.csv",
    index=False
)

meter.to_csv(
    PROCESSED_DATA / "meter_reads_clean.csv",
    index=False
)

tariff.to_csv(
    PROCESSED_DATA / "tariff_rates_clean.csv",
    index=False
)


print("\nProcessed datasets saved successfully!")

print("=" * 60)
print("TRANSFORM STAGE COMPLETED")
print("=" * 60)