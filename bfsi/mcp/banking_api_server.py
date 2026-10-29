"""banking-api MCP server."""

try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError:  # mcp v2+ compatibility
    from mcp.server.mcpserver import MCPServer as FastMCP

mcp = FastMCP("banking-api")

_ACCOUNTS = {
    "AC5001": {"customer_id": "C5001", "balance": 5000.0},
    "AC5002": {"customer_id": "C5002", "balance": 42000.0},
}


@mcp.tool()
def get_balance(account_id: str) -> dict:
    """Return account balance."""
    account = _ACCOUNTS.get(account_id)
    if not account:
        return {"error": "not_found"}
    return {"account_id": account_id, "balance": account["balance"]}


@mcp.tool()
def transfer_funds(from_account: str, to_account: str, amount: float) -> dict:
    """Move money between two accounts."""
    source = _ACCOUNTS.get(from_account)
    target = _ACCOUNTS.get(to_account)
    if not source or not target:
        return {"ok": False, "error": "account_not_found"}
    if source["balance"] < amount:
        return {"ok": False, "error": "insufficient_funds"}
    source["balance"] -= amount
    target["balance"] += amount
    return {"ok": True, "from": from_account, "to": to_account, "amount": amount, "from_balance": round(source["balance"], 2)}


@mcp.tool()
def apply_loan(customer_id: str, amount: float, term_months: int) -> dict:
    """Return loan decision."""
    approved = amount <= 25000
    return {"customer_id": customer_id, "amount": amount, "term_months": term_months, "decision": "APPROVED" if approved else "REFERRED"}


if __name__ == "__main__":
    mcp.run()
