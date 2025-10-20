
from flask import Flask, request, jsonify
import pandas as pd, yaml, json, joblib
from datetime import datetime

app = Flask(__name__)

def load_schema(jur):
    path = f"data/reference/jurisdictions/{jur}_schema.yml"
    return yaml.safe_load(open(path))

def validate_record(rec, schema):
    issues = []
    required = schema['schema']['required']
    types = schema['schema']['types']
    for r in required:
        if rec.get(r) in [None, ""]:
            issues.append({"id":"REQUIRED_"+r.upper(),"message":f"Missing {r}","severity":"high"})
    for col, tp in types.items():
        val = rec.get(col)
        try:
            if tp == "float":
                float(val)
            elif tp == "date":
                pd.to_datetime(val)
            elif tp == "str":
                str(val)
        except Exception:
            issues.append({"id":"TYPE_"+col.upper(),"message":f"Type error {col}","severity":"medium"})
    # simple rules
    env = rec.copy()
    for rule in schema.get("rules", []):
        try:
            if eval(rule.get("condition",""), {}, env):
                issues.append({"id":rule["id"],"message":rule["message"],"severity":rule["severity"]})
        except Exception:
            pass
    return issues

@app.get("/health")
def health():
    return {"status":"ok","time": datetime.utcnow().isoformat()+"Z"}

@app.post("/ingest")
def ingest():
    items = request.json if isinstance(request.json, list) else [request.json]
    df = pd.DataFrame(items)
    df.to_csv("data/raw/ingested.csv", index=False)
    return {"received": len(df)}

@app.post("/validate")
def validate():
    payload = request.json
    jur = payload.get("jurisdiction","eu_vat")
    items = payload.get("data", [])
    schema = load_schema(jur)
    results = []
    for rec in items:
        results.append({"transaction_id": rec.get("transaction_id",-1), "findings": validate_record(rec, schema)})
    return jsonify({"jurisdiction": jur, "count": len(results), "results": results})

@app.post("/score")
def score():
    items = request.json if isinstance(request.json, list) else [request.json]
    df = pd.DataFrame(items)
    clf = joblib.load('results/models/risk_rf.joblib')
    df["gross_amount"] = df.get("net_amount",0) * (1 + df.get("vat_rate",0)/100.0)
    X = df[['amount','net_amount','vat_rate','gross_amount']].fillna(0)
    proba = clf.predict_proba(X)[:,1]
    out = [{"transaction_id": int(df.iloc[i].get("transaction_id",-1)), "score": float(proba[i])} for i in range(len(df))]
    return jsonify(out)

@app.post("/report/generate")
def report_generate():
    payload = request.json or {}
    fmt = payload.get("format","json")
    data = {"generated_at": datetime.utcnow().isoformat()+"Z", "summary": {"ok": 100, "review": 15, "alert": 5}}
    if fmt == "json":
        with open("results/reports/summary.json","w") as f: json.dump(data, f, indent=2)
        return jsonify({"path":"results/reports/summary.json"})
    else:
        return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
