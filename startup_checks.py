"""startup_checks.py — Fiber EUR v1.2 startup validation."""
from __future__ import annotations

import logging
import os
from pathlib import Path

log = logging.getLogger(__name__)

REQUIRED_SETTINGS = [
    "bot_name", "config_version", "demo_mode", "risk_per_trade_usd",
    "daily_risk_cap_usd", "max_units", "min_trade_units", "pair_sl_tp",
    "sessions", "signal_threshold", "max_concurrent_trades",
]


def validate_settings(settings: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []
    for key in REQUIRED_SETTINGS:
        if key not in settings:
            errors.append(f"missing setting: {key}")

    pair_cfg = settings.get("pair_sl_tp", {}).get("EUR_USD", {})
    if not pair_cfg:
        errors.append("missing pair_sl_tp.EUR_USD")
    else:
        if float(pair_cfg.get("sl_pips", 0)) <= 0:
            errors.append("sl_pips must be positive")
        if float(pair_cfg.get("tp_pips", 0)) <= 0:
            errors.append("tp_pips must be positive")

    if float(settings.get("risk_per_trade_usd", 0)) <= 0:
        errors.append("risk_per_trade_usd must be positive")
    if float(settings.get("daily_risk_cap_usd", 0)) < float(settings.get("risk_per_trade_usd", 0)):
        errors.append("daily_risk_cap_usd should be >= risk_per_trade_usd")
    if int(settings.get("max_concurrent_trades", 1)) != 1:
        errors.append("Fiber EUR v1.2 is conservative: max_concurrent_trades must be 1")

    sessions = settings.get("sessions", {})
    for label in ("London", "NY"):
        sess = sessions.get(label)
        if not sess:
            errors.append(f"missing session: {label}")
            continue
        if "start" not in sess or "end" not in sess or "max_spread" not in sess:
            errors.append(f"session {label} must include start, end, max_spread")

    return not errors, errors


def validate_environment(require_telegram: bool = False) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not os.environ.get("OANDA_API_KEY"):
        errors.append("OANDA_API_KEY missing")
    if not os.environ.get("OANDA_ACCOUNT_ID"):
        errors.append("OANDA_ACCOUNT_ID missing")
    if require_telegram:
        if not os.environ.get("TELEGRAM_TOKEN"):
            errors.append("TELEGRAM_TOKEN missing")
        if not os.environ.get("TELEGRAM_CHAT_ID"):
            errors.append("TELEGRAM_CHAT_ID missing")
    return not errors, errors


def run_startup_checks(settings: dict, settings_path: str | Path = "settings.json") -> bool:
    ok_settings, setting_errors = validate_settings(settings)
    ok_env, env_errors = validate_environment(require_telegram=False)
    if not Path(settings_path).exists():
        setting_errors.append(f"settings file not found: {settings_path}")
        ok_settings = False

    all_errors = setting_errors + env_errors
    if all_errors:
        log.error("Startup checks failed:")
        for err in all_errors:
            log.error(" - %s", err)
        return False

    log.info("Startup checks passed | %s | risk/trade=%s | daily cap=%s",
             settings.get("bot_name"), settings.get("risk_per_trade_usd"), settings.get("daily_risk_cap_usd"))
    return True
