"""Compliance automation pipeline."""

from bfsi.compliance.sanctions_check import sanctions_check
from bfsi.fraud_engine import score_transaction
from bfsi.mcp import registry


def run_compliance(customer_id: str, name: str, amount: float, ip_country: str) -> dict:
    """Run KYC -> AML -> Sanctions -> Approval."""
    stages = []

    customer = registry.call("customer-info", "get_customer", customer_id=customer_id)
    kyc_ok = customer.get("kyc_verified") is True
    stages.append({"stage": "KYC", "ok": kyc_ok})
    if not kyc_ok:
        return {"decision": "BLOCK", "failed_stage": "KYC", "stages": stages}

    fraud = score_transaction(customer_id, amount, ip_country)
    aml_ok = fraud["risk"] != "HIGH"
    stages.append({"stage": "AML", "ok": aml_ok, "risk": fraud["risk"]})
    if not aml_ok:
        return {"decision": "BLOCK", "failed_stage": "AML", "stages": stages, "fraud": fraud}

    sanctions = sanctions_check(name)
    sanctions_ok = not sanctions["hit"] or sanctions["strength"] == "PARTIAL"
    stages.append({"stage": "SANCTIONS", "ok": sanctions_ok, "strength": sanctions["strength"]})
    if not sanctions_ok:
        return {"decision": "BLOCK", "failed_stage": "SANCTIONS", "stages": stages, "sanctions": sanctions}

    stages.append({"stage": "APPROVAL", "ok": True})
    return {"decision": "APPROVE", "stages": stages, "fraud": fraud, "sanctions": sanctions}
