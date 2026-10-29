"""Guardrailed customer service chatbot."""

import os
import re

from anthropic import Anthropic

from bfsi.mcp import registry
from bfsi.skills_loader import build_cached_system

_BANNED = re.compile(r"(ignore\s+previous|system\s+prompt|full\s+card\s+number)", re.IGNORECASE)


def sanitize(text: str) -> str:
    """Strip control characters and obvious prompt injection attempts."""
    cleaned = "".join(character for character in text if character.isprintable())
    return _BANNED.sub("[removed]", cleaned)[:2000]


def fraud_tools(customer_id: str, ip_country: str) -> dict:
    """Fetch fraud metadata via audited MCP tools."""
    return {
        "history": registry.call("customer-info", "check_customer_history", customer_id=customer_id),
        "geo": registry.call("customer-info", "verify_ip_location", customer_id=customer_id, ip_country=ip_country),
    }


def reply(customer_id: str, message: str, ip_country: str = "IN", stream: bool = True) -> str:
    """Produce a sanitized answer using the customer-support skill."""
    cleaned = sanitize(message)
    signals = fraud_tools(customer_id, ip_country)
    client = Anthropic(
        auth_token=os.environ.get("OPENROUTER_API_KEY", "demo-key"),
        base_url=os.environ.get("ANTHROPIC_BASE_URL", "https://openrouter.ai/api"),
    )
    user_message = f"Customer {customer_id} asks: {cleaned}\nFraud signals: {signals}"
    kwargs = {
        "model": os.environ.get("MODEL_SONNET", "anthropic/claude-sonnet-4.5"),
        "max_tokens": 300,
        "system": build_cached_system(["customer-support"]),
        "messages": [{"role": "user", "content": user_message}],
    }
    content = []
    if stream:
        with client.messages.stream(**kwargs) as stream_message:
            for chunk in stream_message.text_stream:
                content.append(chunk)
    else:
        response = client.messages.create(**kwargs)
        content.append("".join(block.text for block in response.content if getattr(block, "type", None) == "text"))
    return "".join(content)
