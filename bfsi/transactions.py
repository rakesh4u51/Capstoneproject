"""Production transaction processing."""

import json
from pathlib import Path

from bfsi.compliance.pipeline import run_compliance
from bfsi.mcp import registry
from bfsi.model_router import route

_TXN_LOG = Path("audit_log/transactions.jsonl")


def process(request_id: str, customer_id: str, name: str, from_account: str, to_account: str, amount: float, ip_country: str = "IN") -> dict:
    """Process a transaction and log the audit trail."""
    route("reason", request_id)
    compliance = run_compliance(customer_id, name, amount, ip_country)

    if compliance["decision"] != "APPROVE":
        result = {"request_id": request_id, "status": "REJECTED", "reason": compliance.get("failed_stage"), "compliance": compliance}
    else:
        route("decide", request_id)
        transfer = registry.call("banking-api", "transfer_funds", from_account=from_account, to_account=to_account, amount=amount)
        result = {"request_id": request_id, "status": "SETTLED" if transfer.get("ok") else "FAILED", "transfer": transfer, "compliance": compliance}

    _TXN_LOG.parent.mkdir(exist_ok=True)
    with _TXN_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(result) + "\n")
    return result
