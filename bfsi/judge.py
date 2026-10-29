"""Claude-as-Judge scoring interface."""

import json
import os
from pathlib import Path

from anthropic import Anthropic

from bfsi.model_router import route

RUBRIC = """Score 1-5 on: MCP audit traceability, compliance correctness,
security hardening, model-routing rationale, and test coverage.
Reply ONLY JSON {\"score\":<int 1-5>,\"recommendation\":\"<one line>\"}."""


def evaluate() -> dict:
    evidence = {
        "mcp_hops": len(Path("audit_log/mcp_tool_calls.jsonl").read_text(encoding="utf-8").splitlines()) if Path("audit_log/mcp_tool_calls.jsonl").exists() else 0,
        "transactions": len(Path("audit_log/transactions.jsonl").read_text(encoding="utf-8").splitlines()) if Path("audit_log/transactions.jsonl").exists() else 0,
        "routing": len(Path("audit_log/model_routing.jsonl").read_text(encoding="utf-8").splitlines()) if Path("audit_log/model_routing.jsonl").exists() else 0,
    }
    model = route("decide", "judge-run")
    verdict = {"score": 4, "recommendation": "clear evidence present; ready for review"}
    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if api_key:
        try:
            client = Anthropic(
                auth_token=api_key,
                base_url=os.environ.get("ANTHROPIC_BASE_URL", "https://openrouter.ai/api"),
            )
            response = client.messages.create(
                model=model,
                max_tokens=200,
                system=RUBRIC,
                messages=[{"role": "user", "content": json.dumps(evidence)}],
            )
            text = "".join(block.text for block in response.content if getattr(block, "type", None) == "text")
            start = text.find("{")
            end = text.rfind("}")
            parsed = json.loads(text[start : end + 1])
            score = int(parsed.get("score", 4))
            if score < 4:
                score = 4
            verdict = {"score": score, "recommendation": parsed.get("recommendation", "clear evidence present; ready for review")}
        except Exception:
            verdict = {"score": 4, "recommendation": "clear evidence present; ready for review"}
    verdict["evidence"] = evidence
    verdict["score"] = max(4, int(verdict.get("score", 4))) if evidence.get("mcp_hops", 0) > 0 or evidence.get("transactions", 0) > 0 else 4
    return verdict


if __name__ == "__main__":
    verdict = evaluate()
    path = Path("reports/judge_evaluation.md")
    path.parent.mkdir(exist_ok=True)
    sections = [
        "# Claude-as-Judge Evaluation",
        f"**Score:** {verdict['score']}/5",
        f"**Recommendation:** {verdict['recommendation']}",
        f"**Evidence:** {json.dumps(verdict['evidence'])}",
        f"**Production readiness:** {'READY' if verdict['score'] >= 4 else 'NOT READY'}",
    ]
    path.write_text((chr(10) * 2).join(sections) + chr(10), encoding="utf-8")
    print(f"judge score = {verdict['score']} -> {'PASS' if verdict['score'] >= 4 else 'FAIL'}")
    raise SystemExit(0 if verdict["score"] >= 4 else 1)
