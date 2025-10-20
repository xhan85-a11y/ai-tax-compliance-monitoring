
import pandas as pd, numpy as np, os
np.random.seed(7)
N = 500
df = pd.DataFrame({
    "transaction_id": np.arange(1, N+1),
    "payer_tax_id": [f"{np.random.randint(100000000,999999999)}" for _ in range(N)],
    "payee_tax_id": [f"{np.random.randint(100000000,999999999)}" for _ in range(N)],
    "amount": np.abs(np.random.normal(300, 150, N)).round(2),
    "payment_date": pd.to_datetime("2024-01-01") + pd.to_timedelta(np.random.randint(0, 250, N), unit="D"),
    "supplier_vat": [f"EU{np.random.randint(100000,999999)}" for _ in range(N)],
    "buyer_vat": [f"EU{np.random.randint(100000,999999)}" if np.random.rand()>0.05 else "" for _ in range(N)],
    "net_amount": np.abs(np.random.normal(250, 120, N)).round(2),
    "vat_rate": np.clip(np.random.normal(20, 5, N), -3, 35).round(2),
    "invoice_date": pd.to_datetime("2024-01-01") + pd.to_timedelta(np.random.randint(0, 250, N), unit="D"),
    "financial_institution_id": [f"FI{np.random.randint(1000,9999)}" for _ in range(N)],
    "account_number": [f"AC{np.random.randint(1000000,9999999)}" for _ in range(N)],
    "balance": np.random.normal(5000, 3000, N).round(2),
    "report_period": np.random.choice(["2024Q1","2024Q2","2024Q3"], size=N)
})
os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/transactions.csv", index=False)
print("Wrote data/raw/transactions.csv")
