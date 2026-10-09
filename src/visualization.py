
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"
REPORTS_DIR = PROJECT_ROOT / "reports"
CHARTS_DIR = REPORTS_DIR / "charts"


def create_visualizations():
    """Create and save insurance analytics charts."""

    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    policies = pd.read_csv(CLEANED_DATA_DIR / "policies_cleaned.csv")
    claims = pd.read_csv(CLEANED_DATA_DIR / "claims_cleaned.csv")
    payments = pd.read_csv(CLEANED_DATA_DIR / "payments_cleaned.csv")

    sns.set_theme(style="whitegrid")

    # Chart 1: Premium by policy type
    premium_by_type = (
        policies.groupby("policy_type")["premium_amount"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(9, 5))
    premium_by_type.plot(kind="bar")
    plt.title("Total Premium by Policy Type")
    plt.xlabel("Policy Type")
    plt.ylabel("Total Premium")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "premium_by_policy_type.png", dpi=150)
    plt.close()

    # Chart 2: Claims by status
    claims_by_status = claims["claim_status"].value_counts()

    plt.figure(figsize=(8, 5))
    claims_by_status.plot(kind="bar")
    plt.title("Number of Claims by Status")
    plt.xlabel("Claim Status")
    plt.ylabel("Number of Claims")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "claims_by_status.png", dpi=150)
    plt.close()

    # Chart 3: Payments by status
    payments_by_status = payments["payment_status"].value_counts()

    plt.figure(figsize=(8, 5))
    payments_by_status.plot(kind="bar")
    plt.title("Number of Payments by Status")
    plt.xlabel("Payment Status")
    plt.ylabel("Number of Payments")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "payments_by_status.png", dpi=150)
    plt.close()

    print("Charts saved to:", CHARTS_DIR)
    print("1. premium_by_policy_type.png")
    print("2. claims_by_status.png")
    print("3. payments_by_status.png")


if __name__ == "__main__":
    create_visualizations()
