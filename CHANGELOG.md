## Fiber EUR v1.3.1

### Weekend guard fix
- Added `trade_weekdays_only: true` and `trading_weekdays_sgt: [0,1,2,3,4]`.
- Disabled Sunday/Saturday scan cycles before OANDA login and before session-open Telegram alerts.
- Updated Telegram startup card to show `Trading days: Mon–Fri only`.
- Fixed duplicate `SGT SGT` in session-open Telegram messages.


## London + US Session Update

- Disabled Early Asia, Tokyo, and US Cont. sessions for EUR/USD.
- Kept only the recommended high-liquidity SGT windows: London 16:00–20:59 and US 21:00–23:59.
- Updated settings, startup Telegram card/session template, bot defaults, and main startup documentation.
- Kept max spread at 1.3 pip for both active sessions.

# Changelog

## Fiber EUR v1.3

### v1.3 session update
- Updated runtime version references to `Fiber EUR v1.3`.
- Replaced the previous two-session setup with Early Asia, Tokyo, London, US, and US Cont. time blocks in SGT.
- Set all session max-spread limits to 1.3 pips.
- Made startup card and session-open alerts read sessions dynamically from `settings.json`.
- Made daily state initialization create per-session counters dynamically.

## Fiber EUR v1.3


### v1.3 verification/fixes

- Fixed Telegram startup card top line from stale `Fiber EUR v1.0` to `Fiber EUR v1.3`.
- Fixed all active runtime version references to `Fiber EUR v1.3`.
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

- Version changed from `Fiber EUR v1.0` to `Fiber EUR v1.3`.
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
