"""In-process MCP registry with audit tracing."""

import json
from pathlib import Path

from bfsi.mcp import banking_api_server as banking_api_server_module
from bfsi.mcp import customer_info_server as customer_info_server_module

_AUDIT_PATH = Path("audit_log/mcp_tool_calls.jsonl")
_SEQ = {"n": 0}

_TOOLS = {
    ("customer-info", "get_customer"): customer_info_server_module.get_customer,
    ("customer-info", "check_customer_history"): customer_info_server_module.check_customer_history,
    ("customer-info", "verify_ip_location"): customer_info_server_module.verify_ip_location,
    ("banking-api", "get_balance"): banking_api_server_module.get_balance,
    ("banking-api", "transfer_funds"): banking_api_server_module.transfer_funds,
    ("banking-api", "apply_loan"): banking_api_server_module.apply_loan,
}


def _mask(args):
    out = dict(args)
    for key, value in out.items():
        if "card" in key.lower() and isinstance(value, str) and len(value) > 4:
            out[key] = "****" + value[-4:]
    return out


def _audit(server, tool, args, result):
    _AUDIT_PATH.parent.mkdir(exist_ok=True)
    _SEQ["n"] += 1
    record = {"seq": _SEQ["n"], "server": server, "tool": tool, "args": _mask(args), "ok": "error" not in (result or {})}
    with _AUDIT_PATH.open("a", encoding="utf-8") as handle:
        print(json.dumps(record), file=handle)


def call(server: str, tool: str, **args):
    """Call an MCP tool and record the hop to the audit log."""
    func = _TOOLS.get((server, tool))
    if func is None:
        raise KeyError(f"unknown MCP tool {server}.{tool}")
    result = func(**args)
    _audit(server, tool, args, result)
    return result
