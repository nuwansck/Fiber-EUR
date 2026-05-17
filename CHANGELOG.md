# Changelog

## Fiber EUR v1.2


### v1.2 verification/fixes

- Fixed Telegram startup card top line from stale `Fiber EUR v1.0` to `Fiber EUR v1.2`.
- Fixed all active runtime version references to `Fiber EUR v1.2`.
- Startup Telegram now shows `$75/trade`, `$225/day` cap, calculated risk percentage, and auto-size max units.
- Added startup log warning when broker balance differs from configured `capital_usd`.
- Corrected session display to match the code's exclusive session end logic.

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

- Version changed from `Fiber EUR v1.0` to `Fiber EUR v1.2`.
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
