
from src.insurance_analysis import load_cleaned_data, analyze_insurance


def generate_insights(data):
    """Generate business insights from insurance data."""

    policies = data["policies"]
    claims = data["claims"]
    payments = data["payments"]

    insights = []

    # 1. Most popular policy type
    policy_counts = policies["policy_type"].value_counts()

    if not policy_counts.empty:
        top_type = policy_counts.idxmax()
        top_count = int(policy_counts.max())

        insights.append(
            f"Most common policy type: {top_type} ({top_count} policies)."
        )

    # 2. Policy type generating the highest premium
    premium_by_type = policies.groupby("policy_type")["premium_amount"].sum()

    if not premium_by_type.empty:
        top_premium_type = premium_by_type.idxmax()
        top_premium = premium_by_type.max()

        insights.append(
            f"Highest total premium comes from {top_premium_type}: "
            f"{top_premium:,.2f}."
        )

    # 3. Most frequent claim status
    claim_status_counts = claims["claim_status"].value_counts()

    if not claim_status_counts.empty:
        common_claim_status = claim_status_counts.idxmax()

        insights.append(
            f"Most frequent claim status: {common_claim_status} "
            f"({int(claim_status_counts.max())} claims)."
        )

    # 4. Most frequent payment status
    payment_status_counts = payments["payment_status"].value_counts()

    if not payment_status_counts.empty:
        common_payment_status = payment_status_counts.idxmax()

        insights.append(
            f"Most frequent payment status: {common_payment_status} "
            f"({int(payment_status_counts.max())} payments)."
        )

    # 5. Average claim amount
    if not claims.empty:
        average_claim = claims["claim_amount"].mean()

        insights.append(
            f"Average recorded claim amount: {average_claim:,.2f}."
        )

    # 6. Claims needing attention
    pending_claims = claims[
        claims["claim_status"]
        .astype("string")
        .str.strip()
        .str.lower()
        .eq("pending")
    ]

    insights.append(
        f"Claims currently marked pending: {len(pending_claims)}."
    )

    return insights


def save_insights(insights):
    """Save generated insights to a Markdown report."""

    from pathlib import Path

    project_root = Path(__file__).resolve().parent.parent
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    report_path = reports_dir / "business_report.md"

    with report_path.open("w", encoding="utf-8") as file:
        file.write("# Motor Insurance Business Insights\n\n")

        for number, insight in enumerate(insights, start=1):
            file.write(f"{number}. {insight}\n\n")

    print(f"Business report saved to: {report_path}")


if __name__ == "__main__":
    data = load_cleaned_data()
    results = analyze_insurance(data)

    print("\nMOTOR INSURANCE BUSINESS INSIGHTS")
    print("-" * 40)

    for insight in generate_insights(data):
        print("-", insight)

    print("\nKEY METRICS")
    for metric, value in results.items():
        print(f"{metric}: {value}")

    save_insights(generate_insights(data))
