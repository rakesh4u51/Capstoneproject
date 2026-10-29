"""Vision-based KYC processing."""

import json
import os

from anthropic import Anthropic

from bfsi.skills_loader import build_cached_system


def extract_identity(doc_text: str) -> dict:
    """Extract identity data from a document description."""
    client = Anthropic(
        auth_token=os.environ.get("OPENROUTER_API_KEY", "demo-key"),
        base_url=os.environ.get("ANTHROPIC_BASE_URL", "https://openrouter.ai/api"),
    )
    try:
        response = client.messages.create(
            model=os.environ.get("MODEL_SONNET", "anthropic/claude-sonnet-4.5"),
            max_tokens=200,
            system=build_cached_system(["kyc-extraction"]),
            messages=[{"role": "user", "content": doc_text}],
        )
        text = "".join(block.text for block in response.content if getattr(block, "type", None) == "text")
        start = text.find("{")
        end = text.rfind("}")
        return json.loads(text[start : end + 1]) | {"engine": "claude"}
    except Exception as exc:  # pragma: no cover - fallback only
        return {"full_name": "UNKNOWN", "doc_type": "UNKNOWN", "doc_number": "****", "expiry": "UNKNOWN", "engine": "fallback", "fallback_reason": type(exc).__name__}
