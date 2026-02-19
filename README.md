# Accounting Insights Assistant

A practical command-line accounting tool that goes beyond simple totals and highlights signals teams actually act on:

- **Label performance** (count, average, and total)
- **Monthly net cashflow trend** with running balance
- **Expense anomaly detection** for unusually large outliers
- **Recurring expense detection** for vendor/subscription oversight
- **Actionable recommendations** generated from your transaction signals

---

## 1) Install Python (one-time setup)

1. Download Python 3.10+ from [python.org/downloads](https://www.python.org/downloads/)
2. On Windows, check **Add Python to PATH** during install.

Confirm installation:

```bash
python --version
```

If needed:

```bash
python3 --version
```

---

## 2) Open terminal in this project folder

The folder should contain:

- `app.py`
- `sample_transactions.csv`

---

## 3) Run the insights report

```bash
python app.py sample_transactions.csv
```

or:

```bash
python3 app.py sample_transactions.csv
```

---

## 4) Optional label drill-down

```bash
python app.py sample_transactions.csv --label payroll
```

---

## 5) CSV format requirements

Your CSV must contain these exact columns:

- `date` (format: `YYYY-MM-DD`)
- `description`
- `amount` (positive for income, negative for expenses)
- `label`

---

## Example output sections

- `Label Performance`
- `Monthly Net Cashflow`
- `Potential Expense Anomalies`
- `Recurring Expense Signals`
- `Actionable Recommendations`

These sections are designed to support monthly close, cost controls, and management reporting.
