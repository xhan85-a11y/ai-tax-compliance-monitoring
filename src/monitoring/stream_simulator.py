
import argparse, time, json, os, joblib, pandas as pd
from datetime import datetime

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--rate', type=int, default=10, help='events per minute')
    p.add_argument('--source', default='data/processed/transactions_clean.csv')
    p.add_argument('--outdir', default='results/alerts')
    args = p.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    df = pd.read_csv(args.source)
    clf = joblib.load('results/models/risk_rf.joblib')
    X = df[['amount','net_amount','vat_rate','gross_amount']].fillna(0)

    sleep_s = max(0.05, 60.0/args.rate)
    for i, row in df.iterrows():
        prob = float(clf.predict_proba(X.iloc[i:i+1])[:,1][0])
        level = "alert" if prob >= 0.7 else "review" if prob >= 0.4 else "ok"
        alert = {
            "ts": datetime.utcnow().isoformat()+"Z",
            "transaction_id": int(row.get("transaction_id", -1)),
            "prob": round(prob,4),
            "level": level
        }
        path = f"{args.outdir}/event_{i:05d}.json"
        with open(path, "w") as f:
            json.dump(alert, f)
        print(f"[{level.upper()}] -> {path}")
        time.sleep(sleep_s)

if __name__ == "__main__":
    main()
