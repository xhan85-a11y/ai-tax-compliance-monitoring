
import pandas as pd, os

def clean(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    # Canonical columns
    out["amount"] = pd.to_numeric(out.get("amount", 0), errors="coerce").fillna(0.0)
    out["net_amount"] = pd.to_numeric(out.get("net_amount", 0), errors="coerce").fillna(0.0)
    out["vat_rate"] = pd.to_numeric(out.get("vat_rate", 0), errors="coerce").fillna(0.0)
    # Dates
    for col in ["payment_date","invoice_date"]:
        if col in out.columns:
            out[col] = pd.to_datetime(out[col], errors="coerce")
    # Derivatives
    out["gross_amount"] = out["net_amount"] * (1 + out["vat_rate"]/100.0)
    out["has_vat"] = (out.get("buyer_vat","") != "")
    return out

def main():
    df = pd.read_csv("data/raw/transactions.csv")
    out = clean(df)
    os.makedirs("data/processed", exist_ok=True)
    out.to_csv("data/processed/transactions_clean.csv", index=False)
    print("Wrote data/processed/transactions_clean.csv")

if __name__ == "__main__":
    main()
