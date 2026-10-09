
from src.data_loader import load_data
from src.validation import validate_data


def test_load_data_returns_five_datasets():
    data = load_data()

    assert set(data.keys()) == {
        "customers",
        "policies",
        "vehicles",
        "claims",
        "payments",
    }


def test_loaded_datasets_are_not_empty():
    data = load_data()

    for name, df in data.items():
        assert not df.empty, f"{name} dataset is empty"


def test_validation_returns_boolean():
    data = load_data()

    result = validate_data(data)

    assert isinstance(result, bool)
