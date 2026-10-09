from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Motor Insurance Analytics",
    page_icon="🚗",
    layout="wide",
)

# Project directory
BASE_DIR = Path(__file__).resolve().parents[1]
CLEANED_DIR = BASE_DIR / "data" / "cleaned"
RAW_DIR = BASE_DIR / "data" / "raw"
REPORT_PATH = BASE_DIR / "reports" / "business_report.md"

st.title("🚗 Motor Insurance Analytics Dashboard")
st.caption("Analyze customers, vehicles, policies, claims, and payments.")


# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data(filename):
    """Load a cleaned CSV, falling back to the raw CSV."""
    cleaned_path = CLEANED_DIR / filename
    raw_path = RAW_DIR / filename

    if cleaned_path.exists():
        return pd.read_csv(cleaned_path)

    if raw_path.exists():
        return pd.read_csv(raw_path)

    return pd.DataFrame()


customers = load_data("customers_cleaned.csv")
vehicles = load_data("vehicles_cleaned.csv")
policies = load_data("policies_cleaned.csv")
claims = load_data("claims_cleaned.csv")
payments = load_data("payments_cleaned.csv")


# --------------------------------------------------
# 3. HELPER FUNCTIONS
# --------------------------------------------------
def money(value):
    """Format a number as currency."""
    if pd.isna(value):
        value = 0
    return f"${value:,.2f}"


def numeric_sum(df, column):
    """Safely calculate a numeric column total."""
    if df.empty or column not in df.columns:
        return 0.0

    return pd.to_numeric(df[column], errors="coerce").fillna(0).sum()


def prepare_dates(df, columns):
    """Convert available date columns to datetime."""
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")
    return df


policies = prepare_dates(
    policies,
    ["policy_start_date", "policy_end_date"],
)

claims = prepare_dates(
    claims,
    ["claim_date", "accident_date", "approval_date", "settlement_date"],
)

payments = prepare_dates(
    payments,
    ["payment_date"],
)


# --------------------------------------------------
# 4. SIDEBAR NAVIGATION AND FILTERS
# --------------------------------------------------
st.sidebar.title("🚗 Navigation")

page = st.sidebar.radio(
    "Select a page",
    [
        "Executive Dashboard",
        "Database Schema",
        "Customers",
        "Vehicles",
        "Policies",
        "Claims",
        "Payments",
        "Relationships",
        "Reports & Downloads",
    ],
)

st.sidebar.divider()
st.sidebar.subheader("Dashboard Filters")

filtered_policies = policies.copy()
filtered_claims = claims.copy()
filtered_payments = payments.copy()

# Policy type filter
if not policies.empty and "policy_type" in policies.columns:
    policy_types = sorted(
        policies["policy_type"].dropna().astype(str).unique().tolist()
    )

    selected_policy_types = st.sidebar.multiselect(
        "Policy Type",
        policy_types,
        default=policy_types,
    )

    filtered_policies = filtered_policies[
        filtered_policies["policy_type"].astype(str).isin(
            selected_policy_types
        )
    ]

# Policy status filter
if not policies.empty and "policy_status" in policies.columns:
    policy_statuses = sorted(
        policies["policy_status"].dropna().astype(str).unique().tolist()
    )

    selected_policy_statuses = st.sidebar.multiselect(
        "Policy Status",
        policy_statuses,
        default=policy_statuses,
    )

    filtered_policies = filtered_policies[
        filtered_policies["policy_status"].astype(str).isin(
            selected_policy_statuses
        )
    ]

# Claim status filter
if not claims.empty and "claim_status" in claims.columns:
    claim_statuses = sorted(
        claims["claim_status"].dropna().astype(str).unique().tolist()
    )

    selected_claim_statuses = st.sidebar.multiselect(
        "Claim Status",
        claim_statuses,
        default=claim_statuses,
    )

    filtered_claims = filtered_claims[
        filtered_claims["claim_status"].astype(str).isin(
            selected_claim_statuses
        )
    ]

# Payment status filter
if not payments.empty and "payment_status" in payments.columns:
    payment_statuses = sorted(
        payments["payment_status"].dropna().astype(str).unique().tolist()
    )

    selected_payment_statuses = st.sidebar.multiselect(
        "Payment Status",
        payment_statuses,
        default=payment_statuses,
    )

    filtered_payments = filtered_payments[
        filtered_payments["payment_status"].astype(str).isin(
            selected_payment_statuses
        )
    ]


# --------------------------------------------------
# 5. EXECUTIVE DASHBOARD
# --------------------------------------------------
if page == "Executive Dashboard":

    st.header("Executive Dashboard")
    st.write(
        "An overview of motor insurance business performance, "
        "policy premiums, claims, and payments."
    )

    # KPI calculations
    total_customers = len(customers)
    total_vehicles = len(vehicles)
    total_policies = len(filtered_policies)
    total_claims = len(filtered_claims)
    total_premium = numeric_sum(filtered_policies, "premium_amount")
    total_claim_amount = numeric_sum(filtered_claims, "claim_amount")
    total_payment_amount = numeric_sum(
        filtered_payments, "payment_amount"
    )

    # KPI cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Total Vehicles", f"{total_vehicles:,}")
    col3.metric("Total Policies", f"{total_policies:,}")
    col4.metric("Total Claims", f"{total_claims:,}")

    col5, col6, col7 = st.columns(3)

    col5.metric("Total Premium", money(total_premium))
    col6.metric("Total Claim Amount", money(total_claim_amount))
    col7.metric("Total Payments", money(total_payment_amount))

    st.divider()

    # Chart 1: Premium by policy type
    st.subheader("Premium Analysis")

    if (
        not filtered_policies.empty
        and "policy_type" in filtered_policies.columns
        and "premium_amount" in filtered_policies.columns
    ):
        premium_data = filtered_policies.copy()
        premium_data["premium_amount"] = pd.to_numeric(
            premium_data["premium_amount"], errors="coerce"
        )

        premium_by_type = (
            premium_data.groupby("policy_type", as_index=False)[
                "premium_amount"
            ]
            .sum()
            .dropna()
        )

        if not premium_by_type.empty:
            fig = px.bar(
                premium_by_type,
                x="policy_type",
                y="premium_amount",
                color="policy_type",
                title="Total Premium by Policy Type",
                labels={
                    "policy_type": "Policy Type",
                    "premium_amount": "Total Premium",
                },
                text_auto=".2s",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No premium data is available for the selected filters.")
    else:
        st.info("Policy type or premium amount data is unavailable.")

    # Chart 2: Claim status distribution
    st.subheader("Claims Analysis")

    col1, col2 = st.columns(2)

    with col1:
        if (
            not filtered_claims.empty
            and "claim_status" in filtered_claims.columns
        ):
            claim_status_data = (
                filtered_claims["claim_status"]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .rename_axis("claim_status")
                .reset_index(name="count")
            )

            fig = px.pie(
                claim_status_data,
                names="claim_status",
                values="count",
                hole=0.45,
                title="Claims by Status",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No claim status data is available.")

    # Chart 3: Claim amount by month
    with col2:
        if (
            not filtered_claims.empty
            and "claim_date" in filtered_claims.columns
            and "claim_amount" in filtered_claims.columns
        ):
            monthly_claims = filtered_claims.copy()
            monthly_claims["claim_amount"] = pd.to_numeric(
                monthly_claims["claim_amount"], errors="coerce"
            )
            monthly_claims = monthly_claims.dropna(
                subset=["claim_date", "claim_amount"]
            )

            if not monthly_claims.empty:
                monthly_claims["month"] = (
                    monthly_claims["claim_date"]
                    .dt.to_period("M")
                    .astype(str)
                )

                monthly_claim_data = (
                    monthly_claims.groupby("month", as_index=False)[
                        "claim_amount"
                    ]
                    .sum()
                    .sort_values("month")
                )

                fig = px.line(
                    monthly_claim_data,
                    x="month",
                    y="claim_amount",
                    markers=True,
                    title="Monthly Claim Amount",
                    labels={
                        "month": "Month",
                        "claim_amount": "Claim Amount",
                    },
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No dated claim amount data is available.")
        else:
            st.info("Claim date or claim amount data is unavailable.")

    # Chart 4: Payment status
    st.subheader("Payments Analysis")

    col1, col2 = st.columns(2)

    with col1:
        if (
            not filtered_payments.empty
            and "payment_status" in filtered_payments.columns
        ):
            payment_status_data = (
                filtered_payments["payment_status"]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .rename_axis("payment_status")
                .reset_index(name="count")
            )

            fig = px.bar(
                payment_status_data,
                x="payment_status",
                y="count",
                color="payment_status",
                title="Payments by Status",
                labels={
                    "payment_status": "Payment Status",
                    "count": "Number of Payments",
                },
                text_auto=True,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No payment status data is available.")

    # Chart 5: Monthly payment amount
    with col2:
        if (
            not filtered_payments.empty
            and "payment_date" in filtered_payments.columns
            and "payment_amount" in filtered_payments.columns
        ):
            monthly_payments = filtered_payments.copy()
            monthly_payments["payment_amount"] = pd.to_numeric(
                monthly_payments["payment_amount"], errors="coerce"
            )
            monthly_payments = monthly_payments.dropna(
                subset=["payment_date", "payment_amount"]
            )

            if not monthly_payments.empty:
                monthly_payments["month"] = (
                    monthly_payments["payment_date"]
                    .dt.to_period("M")
                    .astype(str)
                )

                monthly_payment_data = (
                    monthly_payments.groupby("month", as_index=False)[
                        "payment_amount"
                    ]
                    .sum()
                    .sort_values("month")
                )

                fig = px.line(
                    monthly_payment_data,
                    x="month",
                    y="payment_amount",
                    markers=True,
                    title="Monthly Payment Amount",
                    labels={
                        "month": "Month",
                        "payment_amount": "Payment Amount",
                    },
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No dated payment amount data is available.")
        else:
            st.info("Payment date or payment amount data is unavailable.")

    # Chart 6: Claims by damage severity
    st.subheader("Damage Severity Analysis")

    if (
        not filtered_claims.empty
        and "damage_severity" in filtered_claims.columns
    ):
        severity_data = (
            filtered_claims["damage_severity"]
            .fillna("Unknown")
            .astype(str)
            .value_counts()
            .rename_axis("damage_severity")
            .reset_index(name="count")
        )

        fig = px.bar(
            severity_data,
            x="damage_severity",
            y="count",
            color="damage_severity",
            title="Claims by Damage Severity",
            labels={
                "damage_severity": "Damage Severity",
                "count": "Number of Claims",
            },
            text_auto=True,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Damage severity data is unavailable.")

    # Preview tables
    st.divider()
    st.subheader("Recent Policies")

    if not filtered_policies.empty:
        st.dataframe(
            filtered_policies.head(10),
            use_container_width=True,
        )
    else:
        st.info("No policies match the selected filters.")

    st.subheader("Recent Claims")

    if not filtered_claims.empty:
        st.dataframe(
            filtered_claims.head(10),
            use_container_width=True,
        )
    else:
        st.info("No claims match the selected filters.")


# --------------------------------------------------
# 6. DATABASE SCHEMA
# --------------------------------------------------
elif page == "Database Schema":

    st.header("Database Schema")
    st.write("Primary keys (PK) uniquely identify records.")
    st.write("Foreign keys (FK) connect related tables.")

    schema = {
        "customers": {
            "Primary Key": "customer_id",
            "Foreign Keys": "None",
        },
        "vehicles": {
            "Primary Key": "vehicle_id",
            "Foreign Keys": "None",
        },
        "policies": {
            "Primary Key": "policy_id",
            "Foreign Keys": "customer_id, vehicle_id",
        },
        "claims": {
            "Primary Key": "claim_id",
            "Foreign Keys": "policy_id, customer_id",
        },
        "payments": {
            "Primary Key": "payment_id",
            "Foreign Keys": "claim_id, policy_id",
        },
    }

    st.dataframe(
        pd.DataFrame(schema).T.reset_index(names="Table"),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Table Columns")

    tables = {
        "Customers": customers,
        "Vehicles": vehicles,
        "Policies": policies,
        "Claims": claims,
        "Payments": payments,
    }

    for table_name, df in tables.items():
        with st.expander(f"{table_name} — {len(df)} rows"):
            if df.empty:
                st.warning("No data loaded.")
            else:
                st.write(
                    pd.DataFrame(
                        {
                            "Column": df.columns,
                            "Data Type": [
                                str(df[column].dtype)
                                for column in df.columns
                            ],
                        }
                    )
                )


# --------------------------------------------------
# 7. CUSTOMERS PAGE
# --------------------------------------------------
elif page == "Customers":

    st.header("Customer Records")

    if customers.empty:
        st.warning("Customer data was not found.")
    else:
        st.metric("Total Customers", len(customers))

        search = st.text_input(
            "Search customers",
            placeholder="Enter a customer ID or name",
        )

        result = customers.copy()

        if search:
            matches = result.astype(str).apply(
                lambda column: column.str.contains(
                    search, case=False, na=False
                )
            )
            result = result[matches.any(axis=1)]

        st.dataframe(result, use_container_width=True)

        st.download_button(
            "Download Customers CSV",
            data=result.to_csv(index=False).encode("utf-8"),
            file_name="customers.csv",
            mime="text/csv",
        )


# --------------------------------------------------
# 8. VEHICLES PAGE
# --------------------------------------------------
elif page == "Vehicles":

    st.header("Vehicle Records")

    if vehicles.empty:
        st.warning("Vehicle data was not found.")
    else:
        st.metric("Total Vehicles", len(vehicles))
        st.dataframe(vehicles, use_container_width=True)

        st.download_button(
            "Download Vehicles CSV",
            data=vehicles.to_csv(index=False).encode("utf-8"),
            file_name="vehicles.csv",
            mime="text/csv",
        )


# --------------------------------------------------
# 9. POLICIES PAGE
# --------------------------------------------------
elif page == "Policies":

    st.header("Policy Records")

    if filtered_policies.empty:
        st.warning("No policies match the selected filters.")
    else:
        col1, col2 = st.columns(2)
        col1.metric("Policies Shown", len(filtered_policies))
        col2.metric(
            "Premium Total",
            money(numeric_sum(filtered_policies, "premium_amount")),
        )

        st.dataframe(filtered_policies, use_container_width=True)

        st.download_button(
            "Download Filtered Policies CSV",
            data=filtered_policies.to_csv(index=False).encode("utf-8"),
            file_name="policies.csv",
            mime="text/csv",
        )


# --------------------------------------------------
# 10. CLAIMS PAGE
# --------------------------------------------------
elif page == "Claims":

    st.header("Claim Records")

    if filtered_claims.empty:
        st.warning("No claims match the selected filters.")
    else:
        col1, col2 = st.columns(2)
        col1.metric("Claims Shown", len(filtered_claims))
        col2.metric(
            "Claim Amount Total",
            money(numeric_sum(filtered_claims, "claim_amount")),
        )

        st.dataframe(filtered_claims, use_container_width=True)

        st.download_button(
            "Download Filtered Claims CSV",
            data=filtered_claims.to_csv(index=False).encode("utf-8"),
            file_name="claims.csv",
            mime="text/csv",
        )


# --------------------------------------------------
# 11. PAYMENTS PAGE
# --------------------------------------------------
elif page == "Payments":

    st.header("Payment Records")

    if filtered_payments.empty:
        st.warning("No payments match the selected filters.")
    else:
        col1, col2 = st.columns(2)
        col1.metric("Payments Shown", len(filtered_payments))
        col2.metric(
            "Payment Amount Total",
            money(numeric_sum(filtered_payments, "payment_amount")),
        )

        st.dataframe(filtered_payments, use_container_width=True)

        st.download_button(
            "Download Filtered Payments CSV",
            data=filtered_payments.to_csv(index=False).encode("utf-8"),
            file_name="payments.csv",
            mime="text/csv",
        )


# --------------------------------------------------
# 12. RELATIONSHIPS PAGE
# --------------------------------------------------
elif page == "Relationships":

    st.header("Table Relationships")

    st.markdown(
        """
        ```text
        customers
            |
            | customer_id
            v
        policies <------ vehicles
            |
            | policy_id
            v
        claims
            |
            | claim_id
            v
        payments
        ```
        """
    )

    st.subheader("Policies with Customer Details")

    if (
        not policies.empty
        and not customers.empty
        and "customer_id" in policies.columns
        and "customer_id" in customers.columns
    ):
        customer_policy = policies.merge(
            customers,
            on="customer_id",
            how="left",
            suffixes=("_policy", "_customer"),
        )
        st.dataframe(customer_policy, use_container_width=True)
    else:
        st.info("Customer-policy relationship columns are unavailable.")

    st.subheader("Policies with Vehicle Details")

    if (
        not policies.empty
        and not vehicles.empty
        and "vehicle_id" in policies.columns
        and "vehicle_id" in vehicles.columns
    ):
        vehicle_policy = policies.merge(
            vehicles,
            on="vehicle_id",
            how="left",
            suffixes=("_policy", "_vehicle"),
        )
        st.dataframe(vehicle_policy, use_container_width=True)
    else:
        st.info("Policy-vehicle relationship columns are unavailable.")

    st.subheader("Claims with Policy Details")

    if (
        not filtered_claims.empty
        and not policies.empty
        and "policy_id" in filtered_claims.columns
        and "policy_id" in policies.columns
    ):
        claim_policy = filtered_claims.merge(
            policies,
            on="policy_id",
            how="left",
            suffixes=("_claim", "_policy"),
        )
        st.dataframe(claim_policy, use_container_width=True)
    else:
        st.info("Claim-policy relationship columns are unavailable.")

    st.subheader("Payments with Claim Details")

    if (
        not filtered_payments.empty
        and not filtered_claims.empty
        and "claim_id" in filtered_payments.columns
        and "claim_id" in filtered_claims.columns
    ):
        payment_claim = filtered_payments.merge(
            filtered_claims,
            on="claim_id",
            how="left",
            suffixes=("_payment", "_claim"),
        )
        st.dataframe(payment_claim, use_container_width=True)
    else:
        st.info("Payment-claim relationship columns are unavailable.")


# --------------------------------------------------
# 13. REPORTS AND DOWNLOADS
# --------------------------------------------------
elif page == "Reports & Downloads":

    st.header("Reports & Downloads")

    st.subheader("Download Data")

    datasets = {
        "Customers": customers,
        "Vehicles": vehicles,
        "Policies": filtered_policies,
        "Claims": filtered_claims,
        "Payments": filtered_payments,
    }

    for name, df in datasets.items():
        if not df.empty:
            st.download_button(
                f"Download {name} CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name=f"{name.lower()}.csv",
                mime="text/csv",
                key=f"download_{name.lower()}",
            )
        else:
            st.caption(f"{name}: no data available to download.")

    st.divider()
    st.subheader("Business Report")

    if REPORT_PATH.exists():
        report_text = REPORT_PATH.read_text(encoding="utf-8")
        st.markdown(report_text)

        st.download_button(
            "Download Business Report",
            data=report_text.encode("utf-8"),
            file_name="business_report.md",
            mime="text/markdown",
        )
    else:
        st.info(
            "The business report was not found at "
            "`reports/business_report.md`."
        )


# --------------------------------------------------
# 14. FOOTER
# --------------------------------------------------
st.sidebar.divider()
st.sidebar.caption("Motor Insurance Analytics")
st.sidebar.caption("Built with Python, Pandas, Streamlit, and Plotly")