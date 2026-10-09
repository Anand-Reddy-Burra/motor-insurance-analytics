
# Motor Insurance Analytics

## Project Overview

Motor Insurance Analytics is a Python-based data analytics project
that analyzes insurance policies, customers, vehicles, claims, and
payments. It includes data validation, data cleaning, business
metrics, visualizations, and an interactive Streamlit dashboard.

## Features

- Load insurance data from CSV files
- Validate required columns and data quality
- Clean and export datasets
- Analyze premiums, claims, and payments
- Generate business insights and charts
- View results in a Streamlit dashboard
- Run automated tests using pytest
- Record pipeline activity in log files

## Project Structure

```text
motor_insurance_analytics/
├── data/
│   ├── raw/
│   └── cleaned/
├── notebooks/
├── src/
├── app/
├── reports/
├── tests/
├── logs/
├── run_pipeline.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- Pytest

## Setup Instructions

### 1. Clone or open the project

Open the project directory in VS Code.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the environment on macOS

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Prepare the data

Place the five CSV files in `data/raw/`:

- customers.csv
- policies.csv
- vehicles.csv
- claims.csv
- payments.csv

### 6. Run the analytics pipeline

```bash
python run_pipeline.py
```

The pipeline generates cleaned data, analysis results, charts,
and a business insights report when all stages complete successfully.

### 7. Launch the dashboard

```bash
streamlit run app/streamlit_app.py
```

### 8. Run automated tests

```bash
python -m pytest tests -v
```

## Outputs

- Cleaned CSV files in `data/cleaned/`
- Charts in `reports/charts/`
- Business insights in `reports/business_report.md`
- Execution logs in `logs/pipeline.log`

## Disclaimer

This project is intended for educational and analytical purposes.
All conclusions depend on the quality and completeness of the input data.
