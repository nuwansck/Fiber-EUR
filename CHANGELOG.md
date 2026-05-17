# Changelog

## Fiber EUR v1.1

### Added

- Risk-based position sizing using `risk_per_trade_usd`.
- `$75` default risk per trade for `$5,000` capital.
- `$225` daily risk cap.
- `risk.py` for unit sizing, risk cap checks, and margin guard.
- `startup_checks.py` for settings and environment validation.
- `reconcile_state.py` to sync local state with OANDA open positions.
- `logging_utils.py` for secret redaction.
- `config_loader.py` as a clean settings loader utility.
- Fail-closed news behavior using `news_fail_closed`.
- Calendar cache controls: `calendar_cache_max_age_hours` and `calendar_retry_after_min`.
- `settings.json.example`.
- `.gitignore`.

### Changed

- Version changed from `Fiber EUR v1.0` to `Fiber EUR v1.1`.
- Trade size is now calculated from money risk instead of blindly using fixed units.
- Startup now validates core settings before trading.
- Telegram trade-open alerts now use the actual calculated trade units.

### Unchanged

- EUR/USD only.
- H4 → H1 → M15 → M5 cascade strategy.
- London and NY sessions.
- 15 pip SL and 25 pip TP.
- Max 4 trades/day.
- Max 1 open trade.
- Conservative trading style.
