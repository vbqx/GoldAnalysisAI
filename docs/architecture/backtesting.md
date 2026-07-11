# Backtesting Design

This document separates the current replay infrastructure from the target LLM full-pipeline replay. The distinction matters:

- The current implementation is a point-in-time replay harness plus a rule baseline.
- The target implementation is a full historical replay of how the project would have run at that time: LLM analysis, LLM debate, LLM trading decision, risk review, manager decision, then execution simulation.

Rule backtest results must not be presented as the final performance of the LLM decision system.

## Backtest Layers

### Layer 1: Replay Infrastructure

Keep this layer. It is required by every serious backtest mode, including LLM replay.

Responsibilities:

- Slice historical 5m OHLCV at each replay timestamp.
- Rebuild 15m, 1h, 4h, and 1d bars from the visible history.
- Recompute indicators and ICT/PA structure only from data available at that timestamp.
- Align historical macro inputs such as DXY without using future bars.
- Simulate entry, stop, TP, timeout, fees, slippage, and same-bar ambiguity.
- Produce R-multiple statistics, drawdown, setup grouping, and direction grouping.

### Layer 2: Rule Baseline Backtest

Keep this layer as a baseline. It answers:

```text
How do the deterministic rule candidates and rule decision chain behave without LLM judgment?
```

This layer currently uses:

- `compute_trading_signals`
- structure-only debate
- optional historical DXY weighting
- rule trader
- rule risk team
- rule manager
- execution simulator

Interpretation boundary:

```text
Rule baseline results are useful for debugging setup quality, but they are not the performance of the full LLM system.
```

For example, weak performance in `fvg_retest_short` means the rule-generated FVG short candidate is suspicious. It does not prove the LLM system would have selected the same trade.

### Layer 3: LLM Full Pipeline Replay

This is the target requested capability.

At each replay timestamp, the system should run the same logical pipeline the live app runs, but with point-in-time inputs:

```text
Historical MarketContext
-> LLM Analyst Team
-> LLM Bull/Bear Research
-> LLM Debate
-> LLM Level Proposal
-> LLM Trader / Risk / Manager decision
-> Execution simulation on future 5m bars
```

This layer answers:

```text
If the project had been run at this historical moment, what would the LLM analysis and final trading decision have been, and what happened afterward?
```

### Layer 4: A/B Attribution

Once Layer 3 exists, compare modes rather than reading one result in isolation:

```text
Rule baseline
Rule + historical DXY
LLM analysis only
LLM full pipeline
LLM full pipeline + historical DXY
```

This is how we determine whether LLM judgment actually improves selection, risk, or drawdown.

## Institutional Validation Layers

1. Continuous replay
   - Runs through a fixed historical interval.
   - Best for reading regime-level behavior, drawdown shape, and setup decay.

2. Random window replay
   - Samples many historical windows with a deterministic seed.
   - Reports distribution-aware metrics such as median result, bad-window behavior, and p10 window R.
   - This is important for XAUUSD because intraday sessionality and macro-cycle clustering can make one clean interval misleading.

3. Walk-forward validation
   - Planned next layer: tune or select parameters on a training window, then evaluate only on the next unseen window.
   - This is the main overfitting guardrail once the system has tunable strategy parameters.

4. Regime split
   - Planned next layer: compare high-volatility, low-volatility, trend, range, and event-adjacent periods.
   - Event tagging should include CPI, NFP, FOMC, and major central-bank windows.

## Current MVP Scope

- Uses 5m OHLCV as the base replay stream.
- Rebuilds 15m, 1h, 4h, and 1d bars from the historical 5m slice.
- Recomputes indicators and structure only from data visible at the replay timestamp.
- Optionally fetches DXY daily history once and aligns each replay point to the last DXY bar at or before that timestamp.
- Reuses the current rule baseline stack:
  - `compute_trading_signals`
  - structure-only debate, optionally macro-weighted by historical DXY
  - trader
  - risk team
  - manager
- Simulates entry, stop, TP, and timeout on future 5m bars.
- Uses R-multiple accounting, not raw point profit alone.
- Applies conservative same-bar logic: if stop and TP are both reachable in one OHLC bar, stop wins.

## Historical DXY Overlay

When `BacktestConfig.use_macro=True`, the replay engine:

1. Fetches `TVC:DXY` daily bars once.
2. At each replay timestamp, uses only `DXY.index <= timestamp`.
3. Computes 1d, 5d, and 20d DXY changes.
4. Converts DXY strength into a gold macro bias:
   - DXY rising: bearish gold bias.
   - DXY falling: bullish gold bias.
   - Small mixed moves: neutral.
5. Applies `macro_weight` as a soft score/debate adjustment.

DXY is deliberately a weighting input, not a hard trading switch, because gold and USD can both rise during stress regimes.

## Target LLM Full Pipeline Replay

### Point-In-Time Input Contract

Each LLM replay point must receive only information available at or before the replay timestamp.

Allowed:

- OHLCV bars ending at or before timestamp `t`.
- Derived indicators computed from those bars.
- DXY/US10Y bars with index `<= t`.
- Historical news/calendar/social records only if their timestamp is `<= t`.
- Explicit unavailable markers when historical external data is missing.

Disallowed:

- Current DXY/US10Y as a substitute for historical macro.
- Current news/calendar/social feeds in a historical replay.
- Future OHLCV, future swing points, future FVG fills, or future TP/SL outcomes inside LLM prompts.
- Any prompt text that says or implies what happened after timestamp `t`.

### LLM Stage Contract

The LLM replay should be auditable stage by stage.

Required stages:

1. Analyst Team
   - Technical analyst.
   - Fundamentals analyst.
   - News analyst.
   - Sentiment analyst.

2. Research
   - Bullish researcher.
   - Bearish researcher.

3. Debate
   - Produces consensus bias and consensus strength.

4. Level Proposal
   - Produces candidate levels, or rejects levels if geometry is poor.

5. Trading Decision
   - Selects execute / reduce / wait.
   - Selects concrete candidate signal indices or LLM-proposed levels.
   - Must explain why rejected candidates were rejected.

6. Risk / Manager Decision
   - Approves, reduces, or cancels execution.
   - Must be more conservative when external data is missing or event risk is unknown.

### Recommended First Implementation

Do not run unlimited LLM calls across every 5m bar. Start with a controlled replay sample:

```python
BacktestConfig(
    decision_mode="llm_pipeline",
    llm_sample_limit=10,
    step_bars=48,
    use_macro=True,
    llm_cache=True,
)
```

Recommended behavior:

- Evaluate only every `step_bars`.
- Stop after `llm_sample_limit` LLM replay points.
- Cache every LLM request and response by deterministic input hash.
- Store the full prompt payload, parsed output, model name, latency, and parse errors.
- Fall back to `wait` if a required LLM stage fails validation.

### LLM Cache

LLM replay must be reproducible enough for debugging. Store cache files under a dedicated directory such as:

```text
tests/reports/backtest_llm_cache/
```

Cache key should include:

- timestamp
- model
- stage
- normalized input payload hash
- prompt/schema version

Cached content should include:

- input payload
- messages
- raw response
- parsed response
- error, if any
- latency

### Output Schema

Each LLM replay decision should produce a record similar to:

```json
{
  "timestamp": "2026-06-12T08:00:00Z",
  "price": 3421.5,
  "mode": "llm_pipeline",
  "external_availability": {
    "dxy": "historical",
    "us10y": "missing",
    "news": "missing",
    "calendar": "missing"
  },
  "analyst_team": {},
  "bullish": {},
  "bearish": {},
  "debate": {},
  "level_proposals": [],
  "decision": {
    "action": "execute",
    "primary_direction": "short",
    "selected_signal_indices": [0],
    "confidence": 0.62,
    "summary": "..."
  },
  "execution": {
    "entry_time": "...",
    "exit_reason": "stop",
    "r_multiple": -1.0
  }
}
```

### Safety Defaults

- If LLM cannot produce valid JSON: `wait`.
- If historical external data is missing: mark missing explicitly and reduce confidence.
- If LLM selects a signal with invalid geometry: reject it.
- If LLM proposes levels, deterministic validators must still check entry/SL/TP geometry.
- If LLM and deterministic risk conflict, take the more conservative result.

## Metrics

- `trigger_rate`: triggered trades / generated signals.
- `tp1_success_rate`: TP hit trades / triggered trades.
- `win_rate`: profitable closed trades / closed trades.
- `total_r`: total R across closed trades.
- `avg_r`: average R per closed trade.
- `profit_factor`: gross winning R / absolute gross losing R.
- `expectancy_r`: win_rate * avg_win_R - loss_rate * avg_loss_R.
- `max_drawdown_r`: max drawdown in cumulative R.

## Data Requirements

CSV input should contain either a datetime column (`datetime`, `time`, or `timestamp`) or a datetime index, plus OHLC columns:

```text
Datetime,Open,High,Low,Close,Volume
```

Lowercase names are accepted. `Volume` is optional and defaults to zero.

## Limitations

- Current implemented backtest is Layer 1 + Layer 2, not Layer 3.
- LLM stages are intentionally excluded from the current rule baseline.
- Historical DXY is point-in-time replayed; historical US10Y/news/calendar overlays are still planned.
- Full LLM pipeline replay is planned and must use explicit point-in-time input contracts.
- Intra-candle path is unknown for OHLC bars, so the MVP uses conservative stop-first assumptions.
- Spread, commission, and slippage are modeled as configurable point costs, not broker-specific execution.
