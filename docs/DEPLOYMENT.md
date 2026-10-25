# Setup and Deployment

## Local demo
```bash
git clone https://github.com/rsswethaa/heart-attack-prediction-wearables.git
cd heart-attack-prediction-wearables
python demo.py
python -m unittest discover -s tests -v
```

Optional SQLite database:
```bash
python -c "from src.storage import init_db; init_db('wearable_risk.db', seed=True)"
```

## Production/research shape
A genuine health-data deployment would require authenticated ingestion, device provenance, encrypted transport/storage, managed databases, consent/withdrawal workflows, observability, backups, model registry and medical/regulatory governance.
