"""Fraud detection engine."""

import json
import os

from anthropic import Anthropic

from bfsi.mcp import registry
from bfsi.skills_loader import build_cached_system


def _client():
    return Anthropic(
        auth_token=os.environ.get("OPENROUTER_API_KEY", "demo-key"),
        base_url=os.environ.get("ANTHROPIC_BASE_URL", "https://openrouter.ai/api"),
    )


def score_transaction(customer_id: str, amount: float, ip_country: str) -> dict:
    """Return risk score using MCP data and the cached fraud skill."""
    history = registry.call("customer-info", "check_customer_history", customer_id=customer_id)
    geo = registry.call("customer-info", "verify_ip_location", customer_id=customer_id, ip_country=ip_country)
    signals = {"amount": amount, "avg_amount": history["avg_amount"], "geo_mismatch": geo["geo_mismatch"]}

    try:
        response = _client().messages.create(
            model=os.environ.get("MODEL_HAIKU", "anthropic/claude-3.5-haiku"),
            max_tokens=150,
            system=build_cached_system(["fraud-triage"]),
            messages=[{"role": "user", "content": json.dumps(signals)}],
        )
        text = "".join(block.text for block in response.content if getattr(block, "type", None) == "text")
        start = text.find("{")
        end = text.rfind("}")
        parsed = json.loads(text[start : end + 1])
        parsed["engine"] = "claude"
    except Exception:
        risk = "HIGH" if (amount > max(history["avg_amount"] * 3, 5000) or geo["geo_mismatch"]) else "LOW"
        parsed = {"risk": risk, "reason": "fallback rule", "engine": "fallback"}

    parsed["signals"] = signals
    return parsed
