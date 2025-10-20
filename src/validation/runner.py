
import argparse, yaml, json, pandas as pd
from datetime import datetime

def check_types(row, types):
    issues = []
    for col, tp in types.items():
        val = row.get(col, None)
        if tp == "float":
            try:
                float(val)
            except Exception:
                issues.append(f"type:{col}")
        elif tp == "date":
            try:
                pd.to_datetime(val)
            except Exception:
                issues.append(f"type:{col}")
        elif tp == "str":
            if not isinstance(val, str):
                issues.append(f"type:{col}")
    return issues

def run_validation(df, schema):
    required = schema["schema"]["required"]
    types = schema["schema"]["types"]
    rules = schema.get("rules", [])
    findings = []
    for _, row in df.iterrows():
        rec = row.to_dict()
        rec_find = []
        # Required
        for r in required:
            if pd.isna(rec.get(r, None)) or rec.get(r, "") == "":
                rec_find.append({"id":"REQUIRED_"+r.upper(), "severity":"high", "message":f"Missing required field {r}"})
        # Types
        for issue in check_types(rec, types):
            col = issue.split(":")[1]
            rec_find.append({"id":"TYPE_"+col.upper(), "severity":"medium", "message":f"Type check failed on {col}"})
        # Rules
        env = rec.copy()
        for rule in rules:
            cond = rule.get("condition","")
            try:
                if eval(cond, {}, env):
                    rec_find.append({"id":rule["id"], "severity":rule["severity"], "message":rule["message"]})
            except Exception:
                continue
        if rec_find:
            findings.append({"transaction_id": int(rec.get("transaction_id", -1)), "findings": rec_find})
    return findings

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--jurisdiction", required=True, choices=["us_1099","eu_vat","oecd_crs"])
    p.add_argument("--out", required=True)
    args = p.parse_args()

    schema_path = f"data/reference/jurisdictions/{args.jurisdiction}_schema.yml"
    schema = yaml.safe_load(open(schema_path))
    df = pd.read_csv(args.input)
    findings = run_validation(df, schema)

    report = {"generated_at": datetime.utcnow().isoformat()+"Z", "jurisdiction": args.jurisdiction, "count": len(findings), "findings": findings}
    with open(args.out, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
