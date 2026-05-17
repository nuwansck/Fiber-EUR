"""reconcile_state.py — sync local runtime state with broker positions."""
from __future__ import annotations

from datetime import datetime, timezone
import logging

log = logging.getLogger(__name__)


def reconcile_state_with_broker(trader, state: dict, instrument: str = "EUR_USD") -> dict:
    """Ensure local open_times reflects OANDA open position status."""
    state.setdefault("open_times", {})
    pos = trader.get_position(instrument)
    if pos:
        if instrument not in state["open_times"]:
            trade_id, open_time = trader.get_open_trade_id(instrument)
            state["open_times"][instrument] = open_time or datetime.now(timezone.utc).isoformat()
            log.warning("State reconciled: broker has open %s trade; local state was missing it", instrument)
    else:
        if instrument in state["open_times"]:
            state["open_times"].pop(instrument, None)
            log.warning("State reconciled: local %s open trade removed; broker has none", instrument)
    state["has_open_trade"] = bool(state.get("open_times"))
    return state
