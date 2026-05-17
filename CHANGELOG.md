# Changelog

## Fiber EUR v1.4

### Bug fixes
- **CRITICAL — V2 counter-trend NameError** (`signals.py`): `_m30_body` was only assigned inside `if direction == "BUY":`, causing a `NameError` on every SELL trade that reached the V2 veto. All SELL signals silently crashed the scan cycle. Fixed by hoisting `_m30_body = float(cfg.get(...))` to before the loop so it is always defined for both directions.
- **CRITICAL — V2 counter-trend logic** (`signals.py`): Both the bearish-candle check and the bullish-candle check ran for every iteration regardless of direction. For BUY, bullish (with-trend) candles were incorrectly counted as counter-trend. For SELL, bearish (with-trend) candles were incorrectly counted. Fixed with explicit `if direction == "BUY": ... else: ...` guards so each direction counts only the opposing candle type.
- **`load_settings()` global mutation** (`bot.py`): `_DEFAULT_SETTINGS.update(json.load(f))` permanently mutated the module-level default dict; keys removed from `settings.json` would silently retain their old value for the process lifetime. Fixed to return a fresh merged copy on every call — `_DEFAULT_SETTINGS` is no longer mutated.
- **`usd_to_sgd()` misleading docstring** (`bot.py`): Comment said "Account is natively SGD" but account currency is USD. Function is a USD rounding helper. Docstring corrected; function name retained for call-site compatibility.
- **Wrong settings key for `trading_day_start_hour`** (`main.py`): `msg_startup()` was passed `settings.get("db_cleanup_hour_sgt")` for the `trading_day_start_hour` parameter. Coincidentally produced the correct value (0) but from the wrong key. Fixed to use new dedicated key `trading_day_start_hour_sgt`.
- **`fresh_day_state()` redundant `load_settings()` call** (`main.py`): Function reloaded settings from disk internally even when the caller already had a loaded copy. Fixed to accept an optional `settings` parameter and use it when provided.

### Version housekeeping
- `version.py` → `Fiber EUR v1.4`
- `bot.py` docstring → v1.4
- `main.py` docstring → v1.4
- `signals.py` docstring → v1.4
- `settings.json` `bot_name` → `"Fiber EUR v1.4"`
- `settings.json` `config_version` → `"1.4"`
- `settings.json` new key: `trading_day_start_hour_sgt: 0`
- `settings.json.example` kept in sync

---

## Fiber EUR v1.3.2

### Hotfix
- Corrected startup weekday logging guard in `main.py` to use loaded `_s` settings before the later `settings = load_settings()` assignment.
- Keeps London + US sessions only.
- Keeps Mon-Fri only weekday guard for scans/session alerts.
- Keeps max spread at 1.3 pip.

### Weekend guard fix
- Added `trade_weekdays_only: true` and `trading_weekdays_sgt: [0,1,2,3,4]`.
- Disabled Sunday/Saturday scan cycles before OANDA login and before session-open Telegram alerts.
- Updated Telegram startup card to show `Trading days: Mon–Fri only`.
- Fixed duplicate `SGT SGT` in session-open Telegram messages.

---

## Fiber EUR v1.3

### Session update
- Disabled Early Asia, Tokyo, and US Cont. sessions for EUR/USD.
- Kept only the recommended high-liquidity SGT windows: London 16:00–20:59 and US 21:00–23:59.
- Updated settings, startup Telegram card/session template, bot defaults, and main startup documentation.
- Kept max spread at 1.3 pip for both active sessions.

### v1.3 verification/fixes
- Fixed Telegram startup card top line from stale `Fiber EUR v1.0` to `Fiber EUR v1.3`.
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
