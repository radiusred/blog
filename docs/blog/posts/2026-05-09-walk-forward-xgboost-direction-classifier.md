---
layout: default
author: Wordy
title: "Walk-Forward XGBoost for FX Direction: Building the Leakage Gate That Caught Us"
date: 2026-05-09
description: "We shipped a complete walk-forward ML direction classifier to tradedesk. The model found real directional skill on EURUSD. The spreads ate it. Here is what we built, how the embargo/purge gate works, and why a framework-only result is worth publishing."
tags: [machine-learning, systematic-trading, open-source, tradedesk, python]
---

# Walk-Forward XGBoost for FX Direction: Building the Leakage Gate That Caught Us

Phase 6 of the tradedesk build added a complete walk-forward ML direction classifier framework to the [open-source repository](https://github.com/radiusred/tradedesk). The framework covers feature engineering, label generation, walk-forward cross-validation with embargo and purge, XGBoost training and calibration, and markdown reporting.

This post explains what we built, why the leakage prevention machinery matters more than the model itself, and what the Phase 6 results actually showed. The punchline: the model found real directional skill, and the edge was consumed by spread costs at 15-minute resolution on EURUSD. That is a success, not a failure.

## What We Built

The framework lives in `tradedesk/ml/` and has five logical layers:

**Feature engineering** (`features.py`): A `FeatureBuilder` class that transforms raw 1-minute bid/ask OHLCV bars into a 40-plus column feature matrix. The default stack includes 14 technical indicators (ADX, ATR, Bollinger Bands, CCI, EMA, Keltner Channel, MACD, MFI, OBV, RSI, SMA, Stochastic, VWAP, Williams %R), lagged log returns over five windows (1, 5, 15, 60, 240 bars), rolling realised vol, skew and kurtosis over three windows (15, 60, 240 bars), time-of-day cyclical features, and microstructure ratios from the bid/ask spread. Every column at bar `t` depends strictly on data at or before `t`. The no-look-ahead guarantee is enforced structurally, not by convention.

**Label generation** (`labels.py`): Two families. The simpler one — `forward_return_labels` — generates binary {-1, 0, 1} directional labels from the sign of `close[t+h] / close[t] - 1` over a configurable horizon `h`. The spread-aware path uses ask-to-bid round-trip returns: long label = `bid_close[t+h] / ask_close[t] - 1`, short label = `bid_close[t] / ask_close[t+h] - 1`. Labels only flip when both legs clear the neutral band. The second family, `triple_barrier_labels`, follows López de Prado's construction with configurable ATR-based upper/lower targets and a vertical barrier.

**Walk-forward CV** (`cv.py`): A `WalkForwardSplitter` that enforces embargo and purge at every fold boundary. This is the load-bearing piece — the rest of the framework would be dangerous without it.

**Model** (`model.py`, `tuning.py`): A `DirectionClassifier` wrapping XGBoost with calibration and regularisation tuning. Defaults are tuned for high-noise-to-signal FX data: shallow trees (`max_depth=4`), aggressive subsampling (`subsample=0.8`, `colsample_bytree=0.8`), and a small regularisation sweep (24 grid points across `max_depth`, `min_child_weight`, `gamma`, `reg_lambda`).

**Reporting** (`reporting.py`, `walk_forward_runner.py`): A `walk_forward_collect` function that mirrors the CV loop but retains fitted models and out-of-sample probabilities, plus a markdown report with per-fold metrics, aggregate summary, feature importance, equity curve, and a leakage sanity panel.

The `MLDirectionStrategy` class wires the framework to live streaming: it maintains a rolling history buffer, calls `FeatureBuilder.transform` on each close, and dispatches a signal when `predict_proba` crosses the configured threshold. It works with any model that implements `predict_proba`, so nothing is XGBoost-specific in the live path.

## Why Embargo and Purge Matter

Time-series cross-validation is not the same as iid cross-validation. In iid settings, shuffled k-fold is fine. In financial data, shuffled k-fold is a disaster.

The problem is label leakage. When your label at bar `t` is the sign of `close[t+h] / close[t] - 1`, that label depends on price data from bars `t+1` through `t+h`. If any training row overlaps the test window's label horizon, the model can learn to predict from data it would not have had in live trading. The resulting accuracy looks good. The live Sharpe does not.

The standard fix is a gap between the last training row and the first test row. That gap has two components:

**Purge** removes `h` training rows at the tail whose label window would overlap the test window. If horizon `h = 15`, the last 15 training rows are dropped before the test fold begins, because their labels include price data from inside the test window.

**Embargo** adds an additional buffer beyond the purge. Even after purging label-overlapping rows, feature serial autocorrelation can carry information from training data into the test period beyond the label horizon. The embargo absorbs that leakage. If the framework is configured with `purge=h, embargo=h`, the total gap between last training bar and first test bar is `2h` samples.

In `WalkForwardConfig`:

```python
@dataclass(frozen=True)
class WalkForwardConfig:
    train_window: int      # samples per training fold
    test_window: int       # samples per test fold
    step: int | None = None
    embargo: int = 0       # buffer beyond purge
    purge: int = 0         # rows dropped from train tail
    expanding: bool = False
```

The combined gap is `embargo + purge`. The splitter enforces this at every fold boundary with no exceptions.

The tests verify both sides of this contract:

1. A canary feature that *encodes the label* must produce >95% accuracy — this proves the harness detects leaks when they exist.
2. A pure-noise feature must produce ~50% accuracy — this proves the splitter does not invent edges from nowhere.

If either check fails, the leakage gate itself is broken, which is more dangerous than any individual model result. These tests run in CI as a separate top-level step, blocking merges to main if the contract breaks.

Here is the relevant section of `walk_forward_evaluate` signature in `cv.py`:

```python
def walk_forward_evaluate(
    X: pd.DataFrame,
    y: pd.Series,
    splitter: WalkForwardSplitter,
    model_factory: Callable[[], Any],
    *,
    forward_returns: pd.Series | None = None,
    threshold: float = 0.5,
    periods_per_year: int = 252 * 24 * 60,
) -> pd.DataFrame:
    ...
```

The function returns a tidy DataFrame with one row per fold: `fold`, `n_train`, `n_test`, `log_loss`, `accuracy`, `auc`, `hit_rate`, `sharpe`, `max_drawdown`, `trade_count`. The Sharpe here is annualised from per-bar forward returns; on 1-minute bars the annualisation constant is `252 * 24 * 60 = 362880`.

## Quickstart

The example in `docs/examples/phase6_walk_forward_eurusd.py` runs the full pipeline against a Dukascopy cache. The programmatic path is:

```python
from tradedesk.ml import (
    FeatureBuilder, FeatureConfig,
    LabelConfig, forward_return_labels,
    WalkForwardConfig, WalkForwardSplitter, walk_forward_evaluate,
)
from tradedesk.ml.model import DirectionClassifier, DirectionClassifierConfig

# 1. Build features from 1-minute bid/ask OHLCV bars
builder = FeatureBuilder(config=FeatureConfig())
X = builder.transform(bars)  # bars: UTC DatetimeIndex, OHLCV + bid_close + ask_close

# 2. Forward-return labels (binary: 1 = up, 0 = down)
y_raw = forward_return_labels(bars, LabelConfig(horizon=15)).reindex(X.index)
valid = y_raw.notna()
X, y = X.loc[valid], (y_raw.loc[valid] > 0).astype(int)

# 3. Walk-forward CV with embargo + purge
splitter = WalkForwardSplitter(
    WalkForwardConfig(
        train_window=200_000,  # ~139 days of 1-minute bars
        test_window=50_000,    # ~35 days
        embargo=15,
        purge=15,
    )
)

def make_clf() -> DirectionClassifier:
    return DirectionClassifier(DirectionClassifierConfig(n_estimators=200))

metrics = walk_forward_evaluate(X, y, splitter, make_clf)
print(metrics[["fold", "accuracy", "auc", "sharpe", "trade_count"]])

# 4. Persist a trained model
model = DirectionClassifier(DirectionClassifierConfig()).fit(X, y)
model.save("artefacts/direction_eurusd_15m.joblib")
```

To load it into the live strategy:

```python
from tradedesk.ml.model import DirectionClassifier
from tradedesk.strategy.ml_direction_strategy import MLDirectionStrategy

model = DirectionClassifier.load("artefacts/direction_eurusd_15m.joblib")
strategy = MLDirectionStrategy(
    instrument="EURUSD",
    period="1m",
    feature_builder=FeatureBuilder(FeatureConfig()),
    model=model,
)
```

The strategy warms up silently until the feature buffer exceeds `FeatureBuilder.warmup()` bars (roughly 240 minutes for the default config), then dispatches `Signal.ENTRY_LONG`, `Signal.ENTRY_SHORT`, or `Signal.NEUTRAL` on each close.

The command-line runner accepts arguments directly:

```bash
python docs/examples/phase6_walk_forward_eurusd.py \
    --cache /path/to/dukascopy \
    --date-from 2018-01-01 --date-to 2026-01-01 \
    --horizons 15 60 \
    --threshold 0.55 \
    --train-window-bars 500000 \
    --test-window-bars 125000 \
    --spread-aware
```

The `--spread-aware` flag switches to ask-to-bid round-trip labels, which is the realistic path for EURUSD.

## What Phase 6 Found

We ran the framework on eight years of EURUSD 1-minute data at two horizons: 15 bars (15 minutes) and 60 bars (1 hour). The walk-forward setup used approximately one year of training data per fold and three months of out-of-sample test data, with `purge = embargo = horizon`.

The directional AUC across folds was consistently above 0.50. The model had real directional skill. The accuracy at threshold = 0.55 was low, but the signal was there — statistically distinguishable from noise.

The spread-aware Sharpe was not. At 15-minute resolution, EURUSD bid/ask spread costs consumed the directional edge entirely. The round-trip cost of entering and exiting a position at 15 minutes is not large in absolute terms, but the expected move over 15 minutes on a major FX pair is not large either. The model was right about direction more than half the time; it just was not right *by enough* to clear the spread.

At 60-minute resolution the picture improved. A longer horizon gave the directional signal more room to earn back the entry cost. But the deflated Sharpe test — which adjusts for the number of folds and the variance of fold Sharpes — remained the gate. The aggregate result at 60 minutes was framework-level: not wrong enough to indicate random noise, not strong enough to justify deployment.

That is the right outcome.

## Why "Framework Only" Is a Good Result

The point of a deflated Sharpe gate is exactly this: to separate genuine edge from the noise floor introduced by running many folds, many features, and a regularisation sweep. The more combinations you try, the more likely you are to find something that looks good by chance. The deflated Sharpe corrects for that multiple-testing cost.

A framework-only result means:

- The model has measurable directional skill above chance (AUC > 0.50 across folds)
- The walk-forward design prevented look-ahead — the leakage canary confirmed this
- The regularisation sweep did not find a combination that passes the spread-adjusted gate at 15m
- At 60m, the gate is closer but not crossed

Shipping the result without the gate would be worse. We would have a number that looks like Sharpe 0.4 and sounds encouraging until live trading strips the transaction costs back out.

The framework did what it was supposed to do: it measured honestly.

The natural next step is wider instrument and horizon coverage. A 15-minute EURUSD edge consumed by spread is not the same as a 60-minute GBPJPY edge, or a 15-minute edge on a less-quoted instrument where the ratio of expected move to spread is more favourable. The pipeline is in place. Running it against a different instrument is a configuration change, not new engineering.

## What Is Now in tradedesk

The following is now in the public [tradedesk repository](https://github.com/radiusred/tradedesk) and importable from `tradedesk.ml`:

| Module | What it provides |
|--------|-----------------|
| `tradedesk.ml.features` | `FeatureBuilder`, `FeatureConfig`, 14-indicator stack |
| `tradedesk.ml.labels` | `forward_return_labels`, `triple_barrier_labels`, `LabelConfig` |
| `tradedesk.ml.cv` | `WalkForwardSplitter`, `WalkForwardConfig`, `walk_forward_evaluate` |
| `tradedesk.ml.model` | `DirectionClassifier`, `DirectionClassifierConfig` |
| `tradedesk.ml.tuning` | `walk_forward_sweep`, `PlattCalibrator`, `IsotonicCalibrator` |
| `tradedesk.ml.reporting` | `walk_forward_collect`, `render_markdown_report` |
| `tradedesk.strategy.ml_direction_strategy` | `MLDirectionStrategy` |

The leakage canary test runs in CI and blocks merges. The quickstart example is in `docs/examples/phase6_walk_forward_eurusd.py`. The framework works with any `predict_proba`-compatible model, so XGBoost is a default, not a constraint.

---

*Radius Red builds systematic trading infrastructure in the open. The tradedesk repository is on [GitHub](https://github.com/radiusred/tradedesk).*
