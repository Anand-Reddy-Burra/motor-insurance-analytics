
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"


def load_cleaned_data():
    names = ["customers", "policies", "vehicles", "claims", "payments"]
    data = {}

    for name in names:
        path = CLEANED_DATA_DIR / f"{name}_cleaned.csv"
        data[name] = pd.read_csv(path)

    return data


def analyze_insurance(data):
    policies = data["policies"]
    claims = data["claims"]
    payments = data["payments"]

    total_policies = len(policies)
    total_premium = policies["premium_amount"].sum()

    total_claims = len(claims)
    total_claim_amount = claims["claim_amount"].sum()

    approved_claims = (
        claims["claim_status"]
        .astype("string")
        .str.strip()
        .str.lower()
        .eq("approved")
        .sum()
    )

    approval_rate = (
        approved_claims / total_claims * 100
        if total_claims else 0
    )

    total_payments = len(payments)
    total_payment_amount = payments["payment_amount"].sum()

    completed_payments = (
        payments["payment_status"]
        .astype("string")
        .str.strip()
        .str.lower()
        .isin(["completed", "paid"])
        .sum()
    )

    payment_rate = (
        completed_payments / total_payments * 100
        if total_payments else 0
    )

    return {
        "Total Policies": total_policies,
        "Total Premium": round(total_premium, 2),
        "Total Claims": total_claims,
        "Total Claim Amount": round(total_claim_amount, 2),
        "Approved Claims": int(approved_claims),
        "Claim Approval Rate (%)": round(approval_rate, 2),
        "Total Payments": total_payments,
        "Total Payment Amount": round(total_payment_amount, 2),
        "Payment Completion Rate (%)": round(payment_rate, 2),
    }


if __name__ == "__main__":
    data = load_cleaned_data()
    results = analyze_insurance(data)

    print("\nMOTOR INSURANCE ANALYSIS")
    print("-" * 35)

    for metric, value in results.items():
        print(f"{metric}: {value}")

