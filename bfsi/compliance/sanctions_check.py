"""Sanctions screening against a demo watchlist."""

_WATCHLIST = {"ivan petrov", "acme shell holdings", "redline logistics"}


def sanctions_check(name: str) -> dict:
    """Return a sanctions hit status for a normalized name."""
    normalized = " ".join(name.lower().split())
    exact = normalized in _WATCHLIST
    partial = any(normalized in item or item in normalized for item in _WATCHLIST) and not exact
    strength = "STRONG" if exact else ("PARTIAL" if partial else "NONE")
    return {"name": name, "hit": strength != "NONE", "strength": strength}
