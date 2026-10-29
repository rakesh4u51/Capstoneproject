"""Synthetic batch fraud scoring."""

import json
from pathlib import Path

from bfsi.fraud_engine import score_transaction
from bfsi.model_router import route

_SYNTHETIC = [
    {"id": "B1", "customer_id": "C5001", "amount": 300.0, "ip_country": "IN"},
    {"id": "B2", "customer_id": "C5001", "amount": 9000.0, "ip_country": "RU"},
    {"id": "B3", "customer_id": "C5002", "amount": 15000.0, "ip_country": "SG"},
    {"id": "B4", "customer_id": "C5002", "amount": 60000.0, "ip_country": "NG"},
]


def run_batch():
    """Score synthetic batch transactions and persist results."""
    results = []
    for item in _SYNTHETIC:
        route("classify", item["id"])
        score = score_transaction(item["customer_id"], item["amount"], item["ip_country"])
        results.append({"id": item["id"], "risk": score["risk"], "engine": score["engine"]})
    Path("audit_log/batch_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results
