
# Architecture

- **ETL**: Normalize raw transactions to canonical format.
- **Validation**: Apply jurisdiction schema & rules.
- **Scoring**: ML model + heuristics combine into risk score.
- **API**: Stateless endpoints provide validation & reporting.
- **Monitoring**: Streaming simulator writes alerts & metrics.
