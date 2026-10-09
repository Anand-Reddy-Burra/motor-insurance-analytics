
from src.insurance_analysis import analyze_insurance


def test_analysis_calculates_basic_metrics():
    data = {
        "policies": __import__("pandas").DataFrame({
            "premium_amount": [1000, 2000],
        }),
        "claims": __import__("pandas").DataFrame({
            "claim_amount": [500, 300],
            "claim_status": ["Approved", "Pending"],
        }),
        "payments": __import__("pandas").DataFrame({
            "payment_amount": [1000, 500],
            "payment_status": ["Completed", "Pending"],
        }),
    }

    results = analyze_insurance(data)

    assert results["Total Policies"] == 2
    assert results["Total Premium"] == 3000
    assert results["Total Claims"] == 2
    assert results["Total Claim Amount"] == 800
    assert results["Approved Claims"] == 1
    assert results["Total Payments"] == 2
