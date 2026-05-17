"""risk.py — Fiber EUR v1.2 risk and margin utilities.

Keeps the original conservative EUR/USD strategy unchanged, but replaces blind
fixed-size trading with money-risk sizing and daily risk controls.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

log = logging.getLogger(__name__)


@dataclass
class RiskPlan:
    requested_units: int
    final_units: int
    risk_amount: float
    estimated_required_margin: float | None = None
    margin_available: float | None = None
    adjusted: bool = False
    reason: str = ""


def calculate_units_from_risk(
    risk_amount: float,
    sl_pips: float,
    pip_value_per_10k: float = 1.0,
    min_units: int = 1000,
    max_units: int = 50000,
) -> int:
    """Return units sized so a SL roughly equals risk_amount.

    For EUR/USD, 10,000 units is approximately $1 per pip when account currency
    is USD. If your OANDA account is not USD, adjust settings['pip_value_per_10k'].
    """
    if risk_amount <= 0 or sl_pips <= 0 or pip_value_per_10k <= 0:
        raise ValueError("risk_amount, sl_pips, and pip_value_per_10k must be positive")
    units = int((risk_amount / (sl_pips * pip_value_per_10k)) * 10000)
    units = max(min_units, min(units, max_units))
    # Round down to nearest 100 units to avoid odd sizes.
    units = (units // 100) * 100
    return max(min_units, units)


def estimate_required_margin(units: int, price: float, margin_rate: float = 0.0333) -> float:
    """Approximate required margin in account currency.

    OANDA provides exact margin after order processing; this pre-check is a
    safety guard. EUR/USD notional is approximated as units * price.
    """
    if units <= 0 or price <= 0:
        return 0.0
    return abs(units) * price * margin_rate


def build_risk_plan(settings: dict, sl_pips: float, price: float, account_summary: dict | None = None) -> RiskPlan:
    risk_amount = float(settings.get("risk_per_trade_usd", settings.get("risk_per_trade", 75)))
    min_units = int(settings.get("min_trade_units", 1000))
    max_units = int(settings.get("max_units", settings.get("trade_units", 50000)))
    pip_value = float(settings.get("pip_value_per_10k", settings.get("sgd_per_pip_per_10k", 1.0)))

    requested = calculate_units_from_risk(risk_amount, sl_pips, pip_value, min_units, max_units)

    if not account_summary:
        return RiskPlan(requested_units=requested, final_units=requested, risk_amount=risk_amount)

    margin_available = _to_float(account_summary.get("marginAvailable"), None)
    margin_rate = _to_float(account_summary.get("marginRate"), 0.0333)
    safety_factor = float(settings.get("margin_safety_factor", 0.6))
    auto_scale = bool(settings.get("auto_scale_on_margin_reject", True))

    required = estimate_required_margin(requested, price, margin_rate)
    if margin_available is None:
        return RiskPlan(requested, requested, risk_amount, required, None, False, "margin unavailable")

    allowed_margin = margin_available * safety_factor
    if required <= allowed_margin:
        return RiskPlan(requested, requested, risk_amount, required, margin_available, False, "margin ok")

    if not auto_scale:
        return RiskPlan(requested, 0, risk_amount, required, margin_available, False, "insufficient margin")

    # Scale units down to fit allowed margin, then round down to nearest 100.
    if price <= 0 or margin_rate <= 0:
        return RiskPlan(requested, 0, risk_amount, required, margin_available, False, "cannot calculate margin")

    adjusted = int((allowed_margin / (price * margin_rate)) // 100 * 100)
    adjusted = max(0, min(requested, adjusted))
    if adjusted < min_units:
        return RiskPlan(requested, 0, risk_amount, required, margin_available, True, "adjusted below min units")

    adjusted_required = estimate_required_margin(adjusted, price, margin_rate)
    return RiskPlan(requested, adjusted, risk_amount, adjusted_required, margin_available, True, "scaled for margin safety")


def daily_risk_remaining(state: dict, settings: dict) -> float:
    cap = float(settings.get("daily_risk_cap_usd", 0))
    used = float(state.get("daily_risk_used_usd", 0.0))
    if cap <= 0:
        return float("inf")
    return max(0.0, cap - used)


def can_take_risk(state: dict, settings: dict, risk_amount: float) -> tuple[bool, str]:
    cap = float(settings.get("daily_risk_cap_usd", 0))
    used = float(state.get("daily_risk_used_usd", 0.0))
    if cap <= 0:
        return True, "daily risk cap disabled"
    if used + risk_amount > cap + 1e-9:
        return False, f"daily risk cap reached: used={used:.2f}, next={risk_amount:.2f}, cap={cap:.2f}"
    return True, f"daily risk ok: used={used:.2f}, next={risk_amount:.2f}, cap={cap:.2f}"


def reserve_daily_risk(state: dict, risk_amount: float) -> None:
    state["daily_risk_used_usd"] = round(float(state.get("daily_risk_used_usd", 0.0)) + float(risk_amount), 2)


def _to_float(value, default):
    try:
        return float(value)
    except Exception:
        return default
