
import pandas as pd
from pathlib import Path

from src.data_loader import load_data


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"


def clean_dataframe(df):
    """Clean a DataFrame by removing duplicates and trimming text."""

    df = df.copy()

    # Remove completely duplicated rows
    df = df.drop_duplicates()

    # Remove duplicate records based on ID columns
    id_columns = [
        col for col in df.columns
        if col.endswith("_id")
    ]

    for col in id_columns:
        df[col] = df[col].astype("string").str.strip()

    # Trim extra spaces from text columns
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].str.strip()

    # Standardize empty strings as missing values
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    return df


def clean_all_data(data):
    """Clean and save all five insurance datasets."""

    CLEANED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    cleaned_data = {}

    for name, df in data.items():
        cleaned_df = clean_dataframe(df)

        output_path = CLEANED_DATA_DIR / f"{name}_cleaned.csv"
        cleaned_df.to_csv(output_path, index=False)

        cleaned_data[name] = cleaned_df

        print(f"{name}: {len(df)} rows -> {len(cleaned_df)} rows")
        print(f"Saved: {output_path.name}")

    return cleaned_data


if __name__ == "__main__":
    raw_data = load_data()
    clean_all_data(raw_data)
    print("\nData cleaning completed!")
