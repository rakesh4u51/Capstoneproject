"""customer-info MCP server."""

try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError:  # mcp v2+ compatibility
    from mcp.server.mcpserver import MCPServer as FastMCP

mcp = FastMCP("customer-info")

_CUSTOMERS = {
    "C5001": {"name": "Asha Rao", "kyc_verified": True, "tier": "retail", "home_country": "IN", "risk": "low"},
    "C5002": {"name": "Liam Chen", "kyc_verified": True, "tier": "premier", "home_country": "SG", "risk": "low"},
}
_HISTORY = {
    "C5001": [{"amount": 250.0, "country": "IN"}, {"amount": 900.0, "country": "IN"}],
    "C5002": [{"amount": 12000.0, "country": "SG"}],
}


@mcp.tool()
def get_customer(customer_id: str) -> dict:
    """Return customer master record."""
    customer = _CUSTOMERS.get(customer_id)
    if not customer:
        return {"error": "not_found"}
    return {**customer, "customer_id": customer_id}


@mcp.tool()
def check_customer_history(customer_id: str) -> dict:
    """Return prior transaction history for baselining."""
    history = _HISTORY.get(customer_id, [])
    avg_amount = round(sum(item["amount"] for item in history) / len(history), 2) if history else 0.0
    return {"customer_id": customer_id, "count": len(history), "avg_amount": avg_amount}


@mcp.tool()
def verify_ip_location(customer_id: str, ip_country: str) -> dict:
    """Flag country mismatch against the customer home country."""
    home_country = _CUSTOMERS.get(customer_id, {}).get("home_country")
    mismatch = home_country is not None and ip_country != home_country
    return {"customer_id": customer_id, "home_country": home_country, "ip_country": ip_country, "geo_mismatch": mismatch}


if __name__ == "__main__":
    mcp.run()
