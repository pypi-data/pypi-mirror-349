from typing import TypedDict


class CheckResultDict(TypedDict):
    """
    TypedDict; result of a check

    Args:
        status: check status e.g. 'vulnerable', 'fixed', 'broken-functionality'
    """

    status: str


CheckResult = str | CheckResultDict
"""
Either a string for the `status` or a `CheckResultDict`
"""

CheckResultOrNone = CheckResult | None
"""
Deprecated. Prefer `CheckResult | None`.
"""
