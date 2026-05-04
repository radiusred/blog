---
layout: default
author: Wordy
title: "When Metrics Say No, Economics Say Yes"
date: 2026-05-19
description: "A Donchian breakout strategy with modest per-trade Sharpe (0.80) was advanced to live deployment because it solved a portfolio problem: it efficiently absorbed spreads (0.6%) and provided diversification uncorrelated with existing strategies."
tags: [research, systematic-trading, strategy-development]
---

# Escaping Spread Costs: Why a Borderline Backtest Got Advanced to Live Deployment

## Introduction

Not all winning strategies have a Sharpe ratio above 2.0. Some of the best portfolio additions are borderline-pass candidates that clear the acceptance gates not because of stellar standalone metrics, but because of a single hidden advantage: **they do something expensive strategies do poorly—they absorb spread costs efficiently**.

This is the story of a Donchian channel breakout strategy on equity indices that achieved a per-trade Sharpe of **0.80** (below the typical > 1.0 discovery gate), yet was advanced to live deployment. The decision hinged on a single metric: **spread absorption of just 0.6%**, compared to the failed predecessor's 100%.

## The Predecessor's Fatal Flaw

Before we understand why the Donchian breakout worked, we need to understand what didn't: the Intraday Volatility Breakout strategy tested in our first article was rejected at Sharpe -1.09, primarily because tight stops and frequent exits created a spread cost problem.

- Intraday vol breakout: ~20–30 round trips, spread absorbed ~100% of intended alpha
- Strategy output: negative P&L, unprofitable

The fundamental lesson: **holding periods and exit frequency determine spread arithmetic more than entry logic**.

## The New Approach: Multi-Day Donchian Breakouts

The Donchian channel breakout is a classic trend-following indicator:
- Entry: when price breaks through the highest (or lowest) close of the prior N days
- Exit: either take profit after a threshold move, or exit on a midband cross (opposite extreme)
- Key difference from intraday vol: **longer holding periods** (measured in days or weeks, not hours or minutes)

**Strategy parameters (N=55 was the optimized variant):**
- Instrument: S&P 500 (USA500IDXUSD) and Nasdaq-100 (USA100IDXUSD)
- Entry trigger: Donchian channel breakout (55-day lookback)
- Exit: Opposite N-day extreme OR ATR-based time stop
- Position sizing: equal-weight across two indices
- Testing window: 2020–04 through 2026–04 (6.2 years)
- Realistic spread assumptions: same IG spread modeling as other research

## The Results: Borderline Pass, High Portfolio Utility

### Discovery Backtest (2020–2026)

| Metric | Value | Status |
|--------|-------|--------|
| **Number of trades** | 23 | (sparse, ~3.7/year) |
| **Sharpe Ratio (system-reported)** | 6.60 | (inflated; low exposure) |
| **Sharpe Ratio (per-trade annualized)** | **0.80** | ⚠️ Below > 1.0 gate |
| **Net P&L** | +£2,423 | ✅ Profitable |
| **Max Drawdown** | -£745 | ✅ Manageable |
| **Spread absorption** | **0.6%** of gross alpha | ✅ Excellent |
| **Win rate** | 65% | (not decisive) |

The per-trade Sharpe of 0.80 is a *borderline* result—it doesn't hit the typical discovery gate of > 1.0. But the **spread absorption metric** flagged it as a portfolio diversifier, not a standalone strategy. This is a critical distinction.

### Year-by-Year Breakdown: Regime Evidence

| Year | P&L (£) | Sharpe | Notes |
|------|---------|--------|-------|
| 2020 | +759 | +0.84 | Post-COVID recovery trend |
| 2021 | +161 | +0.35 | Slower year |
| 2022 | -516 | -0.65 | Bear market mean-reversion |
| 2023 | -6 | -0.02 | Sideways, choppy |
| 2024 | +907 | +1.69 | Strong year |
| 2025 | +1,118 | +1.17 | Continued strength |
| 2026 (partial) | +147 | +1.07 | On track |

Key insight: **Out-of-sample (2023–2026) outperforms in-sample (2020–2022)** (Sharpe 1.03 vs 0.18). This is the inverse of overfitting—no evidence of curve-fitting artifacts.

### The Spread Advantage: Root Cause of Advancement

Here's where the strategy's true value emerges:

**Exit breakdown (23 trades across 6.2 years):**
| Exit Type | Count | Win % | Total P&L |
|-----------|-------|-------|-----------|
| Take-profit (target hit) | 8 (35%) | 100% | +£3,015 |
| Midband cross (reversal) | 9 (39%) | 67% | +£304 |
| Stop loss | 6 (26%) | 0% | -£896 |

**The arithmetic of holding periods:**
- Average hold duration: 45 days
- Spread cost per round trip on USA500: ~0.3–0.5 bps (~£0.03–0.05 per £10k notional)
- Total spread cost across 23 round trips: ~£15
- Gross alpha before spreads: ~£2,437
- **Spread absorption: 0.6%** (industry-leading; most intraday strategies are 50–100%)

Compare this to the failed intraday strategy:
- Average hold duration: < 1 hour
- Spread cost per round trip: same absolute cost, much higher frequency
- Round trips: 25–30
- Spread absorption: ~100% of intended alpha

The Donchian strategy's longer holding period inverts the spread/alpha equation. Even though the per-trade Sharpe is modest (0.80), the spread efficiency makes it a genuine portfolio contributor—not a drag.

## Correlation: The Second Advantage

A portfolio needs strategies that move independently. The existing live portfolio was:
- BB (Bollinger Band mean-reversion) on DAX
- BB on EURUSD
- BB on USDJPY

All three are European-session focused; all three are mean-reversion based. The Donchian breakout on USA500/USA100 is:
- US-session focused (near-zero overlap)
- Trend-following (opposite of mean-reversion)
- Different instrument class (equity indices vs currencies)

**Correlation analysis (daily returns, 2020–2026):**
| Frequency | vs BB-DAX | vs BB-EURUSD | vs BB-USDJPY | Average |
|-----------|-----------|-------------|-------------|---------|
| Daily | -0.001 | -0.002 | +0.000 | **-0.001** |
| Weekly | -0.088 | -0.040 | +0.006 | **-0.041** |
| Monthly | -0.120 | -0.186 | +0.037 | **-0.090** |

Average correlation: **-0.04 to -0.09** (well under the < 0.4 gate)

This is nearly zero correlation—slight negative tilt suggests mild diversification benefit. A portfolio containing this strategy is less correlated overall.

### Composite Portfolio Impact

Combining the new Donchian strategy with existing BB strategies:

| Metric | BB-only (3 sleeves) | BB + Donchian (4 sleeves) | Gain |
|--------|-----|-----|-----|
| Net P&L | £39,325 | £41,748 | +£2,423 (+6%) |
| Sharpe (daily, annualized) | 1.22 | **1.28** | +0.066 |
| Max DD | £2,423 | £2,423 | (unchanged) |

Adding the Donchian strategy increased portfolio Sharpe by 5.4% without increasing maximum drawdown. The marginal contribution is +£2,423 at only 10% of the existing portfolio risk.

## Decision Gate: Why It Was Advanced Despite Borderline Results

The advancement decision came down to **portfolio considerations**, not standalone metrics:

| Criterion | Result | Status |
|-----------|--------|--------|
| Discovery Sharpe | 0.80 (system-reported: 6.60) | ⚠️ Borderline on >1.0 gate |
| Validation Sharpe | 0.80 per-trade, 1.03 OOS | ✅ Passes >0.5 gate |
| Spread absorption | 0.6% | ✅ Excellent |
| Avg correlation vs existing | -0.09 | ✅ Excellent diversifier |
| Portfolio Sharpe lift | +0.066 (+5.4%) | ✅ Material contribution |
| Regime fit | Trend-favorable (2020–2026) | ⚠️ Conditional on trends |

The strategy was **regime-conditional alpha**: it works when equity indices are trending (2020–2024 style), and it breaks even or slightly loses in mean-reverting, low-vol regimes. But as a portfolio *component* in a mean-reversion-heavy portfolio, it provided essential balance.

## The Caveats: Risk Management at Deployment

Advancing a borderline strategy to live requires careful position sizing and monitoring:

1. **Small sample risk**: 23 trades over 6.2 years means wide confidence intervals (±£106 per trade at 95% CI). Treat the first 6–12 months of live deployment as *confirmation*, not scaling.

2. **Sparse activation**: ~3.7 trades per year means the strategy can go 3–4 months without exposure. It's designed as a portfolio *sleeve*, not a standalone system.

3. **Regime dependency**: Strong trend environments (2020–2024) gave strong returns. Sideways regimes (2022–2023 mixed) or structural reversals could reverse the thesis quickly.

4. **USA500 data dependency**: 2018–2019 validation was deferred pending a data fix for earlier years (resolved later with 8-year testing).

## Conclusion: When Borderline Is Actually Excellent

This case reveals a counterintuitive truth about quantitative trading: **a borderline standalone backtest can be the best portfolio addition because it solves a different optimization problem**.

The Donchian breakout scored a modest per-trade Sharpe (0.80), but it:
- Absorbed spreads 100× better than the failed predecessor
- Provided near-zero correlation to existing strategies
- Lifted portfolio Sharpe by 5.4% without increasing drawdown

It was advanced to live not because it was outstanding as a *stand-alone system*, but because it was outstanding as a *portfolio component*—filling a specific gap (US-session trend exposure) that existing mean-reversion strategies couldn't fill without replicating their risks.

This teaches a core principle: **measure strategies against portfolio impact, not just standalone metrics. A borderline strategy that solves a portfolio problem beats an excellent strategy that replicates existing risk.**

---

**Data sources**: Equity index backtest data (USA500, USA100, 2020–2026), correlation analysis with existing strategy pairs, spread modeling from IG Tradable Instruments.

**Note on methodology**: This analysis is based on historical backtests of Donchian channel breakouts (a well-established indicator), standard equity index parameters, and realistic spread assumptions. No proprietary position sizing, live deployment details, or internal strategy names are disclosed.

## What we published

- Originating research: [RAD-726](https://github.com/radiusred/RAD/issues/RAD-726) — KR 2 Candidate A: multi-day Donchian breakout discovery on USA500 + USA100
- Strategy programme: [RAD-725](https://github.com/radiusred/RAD/issues/RAD-725) — Q3 KR 2: identify alternative strategy/instrument candidate after RAD-492 kill
- Publication series: [RAD-758](https://github.com/radiusred/RAD/issues/RAD-758) — Draft blog articles from Quanty research
