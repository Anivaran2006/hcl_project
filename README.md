# Retail Sales Visualization Project

## Files
- `retail_customer_sales_dataset.csv` — original supplied dataset
- `retail_customer_sales_cleaned.csv` — cleaned working dataset
- `visualizations.py` — reproducible script generating all 11 required charts
- `charts/` — exported PNG charts
- `Retail_Sales_Visualization_Report.pdf` — compiled report with chart captions
- `app.py` — optional interactive Streamlit dashboard
- `requirements.txt` — Python dependencies

## Setup
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Generate charts
Keep the original CSV in the same folder, then run:
```bash
python visualizations.py
```

## Run dashboard
```bash
streamlit run app.py
```

## Data handling notes
The cleaning workflow parses dates, standardizes text casing/whitespace, marks invalid ages, incomes, quantities, unit prices, discounts and ratings as missing, invalidates delivery dates before order dates, and removes exact duplicates/repeated transaction IDs. It does not fabricate missing customer values. Review the cleaning choices with your instructor before submission.
