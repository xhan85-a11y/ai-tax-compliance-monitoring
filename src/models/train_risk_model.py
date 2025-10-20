
import os, joblib, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def main():
    df = pd.read_csv('data/processed/transactions_clean.csv')
    # Simple label heuristic for training
    y = ((df.get('vat_rate',0) < 0) | (df.get('buyer_vat','')=='') | (df.get('amount',0)<=0)).astype(int)
    X = df[['amount','net_amount','vat_rate','gross_amount']].fillna(0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)
    os.makedirs('results/models', exist_ok=True)
    joblib.dump(clf, 'results/models/risk_rf.joblib')
    rep = classification_report(y_test, clf.predict(X_test), output_dict=True)
    pd.DataFrame(rep).to_csv('results/reports/model_report.csv')
    print("Saved results/models/risk_rf.joblib")

if __name__ == "__main__":
    main()
