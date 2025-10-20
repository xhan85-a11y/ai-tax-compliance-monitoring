
# AI-Driven Compliance Monitoring Systems for Global Tax Reporting and Auditing

A production-style, research-friendly prototype for **cross-jurisdiction tax compliance monitoring**.
It ingests transactions, validates them against **country-specific schemas and rules**, scores **compliance risk**
with ML, and exposes a **Flask API** for validation, reporting, and monitoring. Includes a **streaming simulator**,
audit logs, and export utilities for e-filing payload stubs.

## Highlights
- **Multi-jurisdiction schemas** (US 1099-like, EU VAT-like, OECD CRS-like stubs).
- **Validation engine**: schema checks + rule evaluations.
- **ETL**: normalization and enrichment; reproducible pipelines.
- **Risk scoring**: supervised model + heuristics; outputs alert JSON.
- **API**: /ingest, /validate, /score, /report/generate, /health.
- **Streaming**: simulate real-time ingestion and alerting.
- **Docs & tests**: architecture, methodology, experiments; unit tests.

## Quickstart
```bash
pip install -r requirements.txt

# Generate synthetic data
python src/etl/generate_synthetic.py

# Train the risk model
python src/models/train_risk_model.py

# Validate & score a batch
python src/validation/run_validation.py --input data/raw/transactions.csv --jurisdiction eu_vat --out results/reports/validation_report.json
python src/models/score_risk.py --input data/processed/transactions_clean.csv --out results/alerts/alerts.json

# Run API
python src/api/server.py

# Stream simulator (events/min)
python src/monitoring/stream_simulator.py --rate 10
```

## Repository Layout
```
src/
  etl/           # ingest/clean/enrich
  validation/    # schemas + rules + runner
  models/        # training and risk scoring
  api/           # Flask server
  monitoring/    # stream simulator & metrics
data/
  raw/           # synthetic inputs
  processed/     # cleaned outputs
  reference/jurisdictions/ # schemas & rules
results/
  models/ alerts/ reports/ logs/ exports/
```

## Research Angles
- Cross-jurisdiction rule harmonization and **explainability** of violations.
- Threshold tuning for **precision vs. recall** in compliance alerts.
- Handling partial data & **schema drift**.

## License
MIT
