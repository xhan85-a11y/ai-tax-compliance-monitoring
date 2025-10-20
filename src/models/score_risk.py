
import argparse, json, os, joblib, pandas as pd
from datetime import datetime

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--out', required=True)
    args = p.parse_args()

    df = pd.read_csv(args.input)
    clf = joblib.load('results/models/risk_rf.joblib')
    X = df[['amount','net_amount','vat_rate','gross_amount']].fillna(0)
    proba = clf.predict_proba(X)[:,1]
    alerts = []
    for i, row in df.iterrows():
        score = float(proba[i])
        level = "alert" if score >= 0.7 else "review" if score >= 0.4 else "ok"
        alerts.append({
            "transaction_id": int(row.get("transaction_id", -1)),
            "score": round(score,4),
            "level": level
        })
    out = {"generated_at": datetime.utcnow().isoformat()+"Z", "count": len(alerts), "alerts": alerts}
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
