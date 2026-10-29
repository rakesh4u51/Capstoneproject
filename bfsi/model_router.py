"""Model routing and audit logging."""

import json
import os
from pathlib import Path

_LOG_PATH = Path("audit_log/model_routing.jsonl")

_TIERS = {
    "classify": ("MODEL_HAIKU", "anthropic/claude-3.5-haiku", "high-volume classification"),
    "reason": ("MODEL_SONNET", "anthropic/claude-sonnet-4.5", "default reasoning"),
    "decide": ("MODEL_OPUS", "anthropic/claude-opus-4.1", "high-stakes decision"),
}


def route(task: str, request_id: str) -> str:
    """Choose the most appropriate model for the work and log the rationale."""
    env_key, default, rationale = _TIERS.get(task, _TIERS["reason"])
    model = os.environ.get(env_key, default)
    _LOG_PATH.parent.mkdir(exist_ok=True)
    with _LOG_PATH.open("a", encoding="utf-8") as handle:
        print(json.dumps({"request_id": request_id, "task": task, "model": model, "rationale": rationale}), file=handle)
    return model
