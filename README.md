# Fiber EUR v1.1

Fiber EUR v1.1 keeps the original EUR v1.0 conservative 4-layer cascade strategy:

- H4 macro trend
- H1 trend stack
- M15 impulse confirmation
- M5 pullback entry
- EUR/USD only
- London and New York sessions only
- One open trade maximum

## What changed from v1.0

v1.1 does **not** change the core strategy. It improves safety and production readiness:

| Area | v1.1 Improvement |
|---|---|
| Risk per trade | Added `$75` money-risk sizing |
| Daily risk cap | Added `$225` daily exposure cap |
| Position size | Dynamically calculated from SL and risk |
| Margin safety | Added pre-trade margin guard and optional auto-scale |
| News filter | Added fail-closed behavior when calendar is unavailable |
| Startup checks | Added settings and environment validation |
| State recovery | Added broker/local state reconciliation |
| Logging | Added secret redaction helper |
| Config | Added config version and safer risk settings |

## Risk settings

Default v1.1 risk settings:

```json
{
  "capital_usd": 5000,
  "risk_per_trade_usd": 75,
  "daily_risk_cap_usd": 225,
  "pip_value_per_10k": 1.0,
  "min_trade_units": 1000,
  "max_units": 50000,
  "margin_safety_factor": 0.6,
  "auto_scale_on_margin_reject": true
}
```

With the default SL of 15 pips and EUR/USD pip value of about `$1` per pip per 10k units:

```text
$75 / (15 pips × $1 per pip per 10k) × 10,000 = 50,000 units
```

If your OANDA account currency is not USD, update `pip_value_per_10k` accordingly.

## Important

Start in demo mode first. Verify that the calculated units, margin guard, SL/TP, Telegram alerts, and reports are correct before using any live account.
