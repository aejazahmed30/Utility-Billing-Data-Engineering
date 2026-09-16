import pandas as pd
from pathlib import Path


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DATA = BASE_DIR / "data" / "processed"
CLEAN_DATA = BASE_DIR / "data" / "clean"
QUARANTINE_DATA = CLEAN_DATA / "quarantine"


# Create output directories if they do not exist
CLEAN_DATA.mkdir(parents=True, exist_ok=True)
QUARANTINE_DATA.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD PROCESSED DATA
# ============================================================

billing = pd.read_csv(
    PROCESSED_DATA / "billing_history_clean.csv"
)

meter = pd.read_csv(
    PROCESSED_DATA / "meter_reads_clean.csv"
)


print("=" * 60)
print("UTILITY BILLING ETL - DATA QUALITY CLEANING")
print("=" * 60)

print("\nProcessed datasets loaded successfully!")

print(f"Billing records : {len(billing)}")
print(f"Meter records   : {len(meter)}")


# ============================================================
# 3. BILLING DATA QUALITY CHECK
# ============================================================

print("\n" + "=" * 60)
print("BILLING DATA QUALITY CHECK")
print("=" * 60)


# Convert billing amount to numeric
billing["total_bill_amount"] = pd.to_numeric(
    billing["total_bill_amount"],
    errors="coerce"
)


# Identify invalid billing amounts
billing_invalid = billing[
    billing["total_bill_amount"].isna()
].copy()


# Identify negative billing amounts
billing_negative = billing[
    billing["total_bill_amount"] < 0
].copy()


# Add reason for rejection
billing_invalid["rejection_reason"] = (
    "Invalid or missing billing amount"
)

billing_negative["rejection_reason"] = (
    "Negative billing amount"
)


# Combine rejected billing records
billing_quarantine = pd.concat(
    [billing_invalid, billing_negative],
    ignore_index=True
)


# Remove invalid and negative records from final dataset
billing_clean = billing[
    billing["total_bill_amount"].notna()
    & (billing["total_bill_amount"] >= 0)
].copy()


print(f"Invalid billing records  : {len(billing_invalid)}")
print(f"Negative billing records : {len(billing_negative)}")
print(f"Final billing records    : {len(billing_clean)}")


# ============================================================
# 4. METER DATA QUALITY CHECK
# ============================================================

print("\n" + "=" * 60)
print("METER DATA QUALITY CHECK")
print("=" * 60)


# Convert units consumed to numeric
meter["units_consumed"] = pd.to_numeric(
    meter["units_consumed"],
    errors="coerce"
)


# Identify invalid meter readings
meter_invalid = meter[
    meter["units_consumed"].isna()
].copy()


# Identify negative meter readings
meter_negative = meter[
    meter["units_consumed"] < 0
].copy()


# Add rejection reasons
meter_invalid["rejection_reason"] = (
    "Invalid or missing units consumed"
)

meter_negative["rejection_reason"] = (
    "Negative units consumed"
)


# Combine rejected meter records
meter_quarantine = pd.concat(
    [meter_invalid, meter_negative],
    ignore_index=True
)


# Remove invalid and negative readings
meter_clean = meter[
    meter["units_consumed"].notna()
    & (meter["units_consumed"] >= 0)
].copy()


print(f"Invalid meter records  : {len(meter_invalid)}")
print(f"Negative meter records : {len(meter_negative)}")
print(f"Final meter records    : {len(meter_clean)}")


# ============================================================
# 5. SAVE CLEAN DATA
# ============================================================

billing_clean.to_csv(
    CLEAN_DATA / "billing_history_final.csv",
    index=False
)

meter_clean.to_csv(
    CLEAN_DATA / "meter_reads_final.csv",
    index=False
)


# ============================================================
# 6. SAVE QUARANTINED DATA
# ============================================================

billing_quarantine.to_csv(
    QUARANTINE_DATA / "billing_invalid.csv",
    index=False
)

meter_quarantine.to_csv(
    QUARANTINE_DATA / "meter_invalid.csv",
    index=False
)


# ============================================================
# 7. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DATA QUALITY CLEANING COMPLETED")
print("=" * 60)

print("\nClean datasets:")
print("  billing_history_final.csv")
print("  meter_reads_final.csv")

print("\nQuarantined datasets:")
print("  billing_invalid.csv")
print("  meter_invalid.csv")

print("\nAll output files saved successfully!")

print("=" * 60)