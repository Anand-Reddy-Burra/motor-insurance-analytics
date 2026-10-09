import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_data():
    customers = pd.read_csv(RAW_DATA_DIR / "customers.csv")
    policies = pd.read_csv(RAW_DATA_DIR / "policies.csv")
    vehicles = pd.read_csv(RAW_DATA_DIR / "vehicles.csv")
    claims = pd.read_csv(RAW_DATA_DIR / "claims.csv")
    payments = pd.read_csv(RAW_DATA_DIR / "payments.csv")

    return {
        "customers": customers,
        "policies": policies,
        "vehicles": vehicles,
        "claims": claims,
        "payments": payments,
    }


if __name__ == "__main__":
    data = load_data()

    for name, df in data.items():
        print(f"\n{name.upper()}")
        print(df.head())
        print("Number of rows:", len(df))