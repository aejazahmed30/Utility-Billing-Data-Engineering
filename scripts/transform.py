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

# ============================================================
# 4. Clean numeric columns
# ============================================================

def clean_numeric_column(df, column):
    """
    Convert a column to numeric values.
    Invalid values are converted to NaN.
    """

    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df

# Billing numeric columns
billing = clean_numeric_column(billing, "total_bill_amount")
billing = clean_numeric_column(billing, "amount_paid")
billing = clean_numeric_column(billing, "outstanding_balance")

# Meter numeric columns
meter = clean_numeric_column(meter, "units_consumed")
meter = clean_numeric_column(meter, "cumulative_reading")
meter = clean_numeric_column(meter, "current_a")
meter = clean_numeric_column(meter, "power_factor")
meter = clean_numeric_column(meter, "peak_demand_kw")
meter = clean_numeric_column(meter, "reactive_units_kvar")

# Customer numeric columns
customers = clean_numeric_column(customers, "sanctioned_load_kw")
customers = clean_numeric_column(customers, "security_deposit")
customers = clean_numeric_column(customers, "avg_monthly_units")

# ============================================================
# 5. Numeric cleaning summary
# ============================================================

print("\n" + "=" * 60)
print("NUMERIC CLEANING SUMMARY")
print("=" * 60)

print(
    f"Billing invalid amounts after conversion: "
    f"{billing['total_bill_amount'].isna().sum()}"
)

print(
    f"Meter invalid units after conversion: "
    f"{meter['units_consumed'].isna().sum()}"
)


# ---------------------------------------------------------
# 6. Convert date/time columns
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