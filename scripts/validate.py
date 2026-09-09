import pandas as pd
from pathlib import Path


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DATA = BASE_DIR / "data" / "processed"


# ============================================================
# 2. LOAD PROCESSED DATA
# ============================================================

customers = pd.read_csv(PROCESSED_DATA / "customers_clean.csv")
billing = pd.read_csv(PROCESSED_DATA / "billing_history_clean.csv")
meter = pd.read_csv(PROCESSED_DATA / "meter_reads_clean.csv")
tariff = pd.read_csv(PROCESSED_DATA / "tariff_rates_clean.csv")


print("=" * 60)
print("UTILITY BILLING ETL - DATA QUALITY VALIDATION")
print("=" * 60)


# ============================================================
# 3. BASIC DATASET VALIDATION
# ============================================================

def validate_dataframe(df, name):

    print(f"\n{'=' * 60}")
    print(f"VALIDATING {name.upper()}")
    print("=" * 60)

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    # Missing values
    missing_values = df.isnull().sum().sum()

    print(f"Missing values: {missing_values}")

    # Duplicate rows
    duplicate_rows = df.duplicated().sum()

    print(f"Duplicate rows: {duplicate_rows}")

    return missing_values, duplicate_rows


# ============================================================
# 4. VALIDATE ALL DATASETS
# ============================================================

validate_dataframe(customers, "Customers")
validate_dataframe(billing, "Billing")
validate_dataframe(meter, "Meter")
validate_dataframe(tariff, "Tariff")


# ============================================================
# 5. CUSTOMER ID VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMER ID VALIDATION")
print("=" * 60)

invalid_customer_ids = customers["customer_id"].isnull().sum()

print(f"Missing customer IDs: {invalid_customer_ids}")


# ============================================================
# 6. BILLING AMOUNT VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("BILLING AMOUNT VALIDATION")
print("=" * 60)

if "total_bill_amount" in billing.columns:

    billing_amount = pd.to_numeric(
        billing["total_bill_amount"],
        errors="coerce"
    )

    invalid_amounts = billing_amount.isna().sum()

    negative_amounts = (billing_amount < 0).sum()

    print(f"Invalid billing amounts: {invalid_amounts}")
    print(f"Negative billing amounts: {negative_amounts}")

else:

    print("total_bill_amount column not found.")

# ============================================================
# 7. METER READING VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("METER READING VALIDATION")
print("=" * 60)

if "units_consumed" in meter.columns:

    meter_units = pd.to_numeric(
        meter["units_consumed"],
        errors="coerce"
    )

    invalid_units = meter_units.isna().sum()

    negative_units = (meter_units < 0).sum()

    print(f"Invalid units consumed: {invalid_units}")
    print(f"Negative units consumed: {negative_units}")

else:

    print("units_consumed column not found.")

# ============================================================
# 8. DATASET COLUMN INSPECTION
# ============================================================

print("\n" + "=" * 60)
print("DATASET COLUMN NAMES")
print("=" * 60)

print("\nCustomers:")
print(customers.columns.tolist())

print("\nBilling:")
print(billing.columns.tolist())

print("\nMeter:")
print(meter.columns.tolist())

print("\nTariff:")
print(tariff.columns.tolist())

# ============================================================
# 9. VALIDATION COMPLETED
# ============================================================

print("\n" + "=" * 60)
print("DATA QUALITY VALIDATION COMPLETED")
print("=" * 60)