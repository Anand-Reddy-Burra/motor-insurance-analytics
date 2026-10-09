
import pandas as pd

from src.validation import validate_data


def test_validation_rejects_missing_required_columns():
    data = {
        "customers": pd.DataFrame({
            "customer_id": ["C001"],
        }),
        "policies": pd.DataFrame(),
        "vehicles": pd.DataFrame(),
        "claims": pd.DataFrame(),
        "payments": pd.DataFrame(),
    }

    assert validate_data(data) is False
