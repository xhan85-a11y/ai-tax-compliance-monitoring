
install:
	pip install -r requirements.txt
data:
	python src/etl/generate_synthetic.py && python src/etl/clean_transform.py
train:
	python src/models/train_risk_model.py
validate:
	python src/validation/run_validation.py --input data/raw/transactions.csv --jurisdiction eu_vat --out results/reports/validation_report.json
score:
	python src/models/score_risk.py --input data/processed/transactions_clean.csv --out results/alerts/alerts.json
api:
	python src/api/server.py
stream:
	python src/monitoring/stream_simulator.py --rate 10
