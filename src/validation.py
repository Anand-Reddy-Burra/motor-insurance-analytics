
def validate_data(data):
    """Check insurance datasets for basic data quality issues."""

    required_columns = {
        "customers": ["customer_id", "customer_name", "age", "city"],
        "policies": ["policy_id", "customer_id", "vehicle_id", "premium", "policy_status"],
        "vehicles": ["vehicle_id", "vehicle_type", "vehicle_age"],
        "claims": ["claim_id", "policy_id", "claim_amount", "claim_status"],
        "payments": ["payment_id", "policy_id", "payment_amount", "payment_status"],
    }

    all_valid = True

    for name, columns in required_columns.items():
        df = data[name]

        print(f"\nValidating {name}...")

        # Check required columns
        missing_columns = [col for col in columns if col not in df.columns]

        if missing_columns:
            print("Missing columns:", missing_columns)
            all_valid = False
            continue

        # Check missing values
        missing_values = df[columns].isnull().sum().sum()
        print("Missing values:", missing_values)

        # Check duplicate IDs
        id_column = columns[0]
        duplicate_ids = df[id_column].duplicated().sum()
        print("Duplicate IDs:", duplicate_ids)

        if missing_values > 0 or duplicate_ids > 0:
            all_valid = False

    print("\nValidation result:", "PASSED" if all_valid else "ISSUES FOUND")
    return all_valid
