# Changelog

## Fiber EUR v1.5

### Bug fixes
- **CRITICAL — `now` undefined in `detect_sl_tp_hits`** (`bot.py`): The trade history
  write block used `now.strftime(...)` but `now` is not defined in `detect_sl_tp_hits`'s
  scope. The `NameError` was silently caught, meaning trade history silently failed to
  write on every closed trade since v1.0. Fixed by defining `_hist_now = datetime.now(sg_tz)`
  locally at the start of the history block.

### Version housekeeping
- All docstrings, inline comments, and user-visible strings updated to v1.5 throughout
  every file: `bot.py`, `main.py`, `signals.py`, `calendar_filter.py`, `config.py`,
  `config_loader.py`, `database.py`, `oanda_trader.py`, `reporting.py`, `risk.py`,
  `startup_checks.py`, `state_utils.py`, `telegram_alert.py`, `telegram_templates.py`,
  `README.md`, `settings.json`, `settings.json.example`, `version.py`.
- `_BANNER` in `telegram_templates.py` now reads `🇪🇺 Fiber EUR v1.5 | EUR/USD`
  (was `v1.3.2` — shown on every Telegram message).
- CSV report captions in `reporting.py` updated to `v1.5`.
- `startup_checks.py` error message updated to `v1.5`.
- Misleading `SGD` label removed from `bot.py` log line and module-level comment
  (account currency is USD; no FX conversion occurs).

---

## Fiber EUR v1.4

### Bug fixes
- **CRITICAL — V2 counter-trend NameError** (`signals.py`): `_m30_body` was only assigned
  inside `if direction == "BUY":`, causing a `NameError` on every SELL trade that reached
  V2. Fixed by hoisting above the loop.
- **CRITICAL — V2 counter-trend logic** (`signals.py`): Both candle checks ran regardless
  of direction. Fixed with explicit direction guards so each direction counts only opposing
  candle type.
- **`load_settings()` global mutation** (`bot.py`): `_DEFAULT_SETTINGS.update(...)` mutated
  the module-level dict permanently. Fixed to return a fresh merged copy each call.
- **`usd_to_sgd()` misleading docstring** (`bot.py`): Account is USD. Docstring corrected.
- **Wrong settings key for `trading_day_start_hour`** (`main.py`): Was reading
  `db_cleanup_hour_sgt`. Fixed to use dedicated `trading_day_start_hour_sgt` key.
- **`fresh_day_state()` redundant `load_settings()` call** (`main.py`): Fixed to accept
  optional `settings` parameter.

### Version housekeeping
- `version.py`, `bot.py`, `main.py`, `signals.py` docstrings → v1.4.
- `settings.json` `bot_name` → `"Fiber EUR v1.4"`, `config_version` → `"1.4"`.
- New key: `trading_day_start_hour_sgt: 0`.

---

## Fiber EUR v1.3.2

### Hotfix + weekend guard
- Corrected startup weekday logging guard in `main.py`.
- Added `trade_weekdays_only: true` and `trading_weekdays_sgt: [0,1,2,3,4]`.
- Disabled Sunday/Saturday scan cycles and session-open alerts.
- Fixed duplicate `SGT SGT` in session-open Telegram messages.

---

## Fiber EUR v1.3

### Added
- Risk-based position sizing (`risk_per_trade_usd`).
- Daily risk cap (`daily_risk_cap_usd`).
- `risk.py`, `startup_checks.py`, `reconcile_state.py`, `logging_utils.py`,
  `config_loader.py`.
- Fail-closed news filter behavior.
- Calendar cache controls.

### Changed
- Trade size calculated from money risk, not fixed units.
- Startup validates core settings before trading.
- London and US sessions only (Early Asia, Tokyo, US Cont. disabled).
