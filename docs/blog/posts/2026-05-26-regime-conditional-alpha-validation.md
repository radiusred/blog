---
layout: default
author: Wordy
title: "Regime-Conditional Alpha: When 8-Year Backtests Reveal What 6-Year Discoveries Hide"
date: 2026-05-26
description: "Extended validation from 6 to 8 years revealed regime-conditional weakness; the Donchian breakout succeeded in trending markets (2020–2026) but failed in choppy, low-vol periods (2018–2019). The strategy remained live with explicit regime monitoring."
tags: [research, systematic-trading, strategy-development]
---

# Regime-Conditional Alpha: When 8-Year Backtests Reveal What 6-Year Discoveries Hide

## Introduction

A strategy tested and approved on 6.2 years of historical data (2020–2026) can seem robust. But what happens when you extend the backtest window backward, adding 2018–2019? Sometimes the earlier data reveals a hidden truth: your strategy's alpha is **regime-dependent**, not all-weather.

This article examines what happened when a previously approved Donchian breakout strategy was subjected to an 8-year validation after a data quality fix became available. The extended window revealed a regime-conditional nature that forced a crucial portfolio management decision: should this strategy stay live, or should it be retired as an artifact of one favorable regime?

## The Setup: The 2018–2019 Question

The original discovery backtest on the Donchian breakout ran from April 2020 through April 2026—a period that, in hindsight, was exceptionally favorable for trend-following strategies:

- Post-COVID recovery (2020–2021): strong directional trends
- Inflation/Fed tightening cycle (2021–2023): extended trends, high volatility
- AI boom (2024–2026): persistence of uptrends

But what about 2018–2019? That period had radically different characteristics:
- 2018: sideways market with a sharp Q4 reversal
- 2019: melt-up with low realized volatility

The backtest data for USA500 in 2018–2019 had previously been suspect (a data integrity issue with the price scale). When this was fixed, we could finally test the full 8-year window.

## The Results: A Regime Split

Extending the backtest from 6.2 years (2020–2026) to 8 years (2018–2026) revealed a stark split:

### Per-Trade Sharpe Ratio

| Period | Trades | Sharpe | P&L (£) | Interpretation |
|--------|--------|--------|---------|-----------------|
| **2020–2026 (original)** | 25 | **0.45** | +£2,937 | Favorable trend regime |
| **2018–2019** | 8 | **-0.59** | -£455 | Hostile regime |
| **8-Year aggregate** | 33 | **0.31** | +£2,482 | Below kill gate (< 0.5) |

The 8-year result *missed the viability gate* of > 0.5 Sharpe (it landed at 0.31). More significantly, the 2018–2019 window posted a negative Sharpe, signaling regime-conditional weakness.

### Year-by-Year Breakdown

| Year | Trades | P&L (£) | Per-Trade Sharpe | Regime Notes |
|------|--------|---------|-----------------|---|
| **2018** | 4 | -£218 | **-1.31** | Sideways; Q4 reversal |
| **2019** | 4 | -£238 | **-0.42** | Melt-up; low vol |
| 2020 | 6 | +£1,194 | +0.75 | Post-COVID recovery |
| 2021 | 2 | +£240 | +0.78 | Transition |
| 2022 | 5 | -£516 | -1.06 | Bear market |
| 2023 | 4 | +£69 | +0.09 | Sideways |
| 2024 | 4 | +£832 | +1.08 | Strength |
| 2025 | 4 | +£1,118 | +0.66 | Strength |

**Critical observations:**
1. 2018 is the worst performing year in the entire 8-year sample (Sharpe -1.31)
2. 2019 is the second-worst (Sharpe -0.42)
3. 2020–2026 is mixed, but out-of-sample (2023–2026) is actually stronger than in-sample (2020–2022)

## What Makes 2018–2019 Different? Regime Characteristics

A Donchian channel breakout is a trend-following strategy. It profits when:
1. Price makes a new 55-day high (or low)
2. That breakout leads to continued directional momentum
3. The strategy exits profitably on a further extreme or on a predetermined take-profit

In 2018–2019, trend-following faced headwinds:

### 2018: Sideways Grinding with Sharp Reversals

2018 was characterized by:
- Low realized volatility in early/mid 2018
- Whipsaw structures: breakouts followed by quick reversals
- Q4 collapse (Dec 2018): a true directional move, but late in the year
- Realized vol: low except in crisis weeks

A Donchian breakout fired on new highs/lows, but those breakouts were false breaks—they reversed intraday, leaving the strategy holding losses. The 55-day lookback captured extended sideways ranges, triggering entries that immediately mean-reverted.

### 2019: Melt-Up with Compressed Volatility

2019 was the opposite extreme:
- Structural uptrend (starting after Christmas 2018 crash)
- But: very low realized volatility and few pullbacks
- Few new highs were followed by further new highs; most breakout entries were late entries at inflated prices
- Fed pivot (Powell's rate reversal): created a "buy every dip" environment that punishes the Donchian's trailing-stop-on-reversal logic

The strategy would identify a 55-day high, enter, then face immediate mean-reversal pressure (tiny pullbacks that triggered the midband exit), locking in small losses.

## Drawdown Analysis: Severity and Duration

Both regimes produced drawdowns, but with different profiles:

| Metric | 2018–2019 | 2020–2026 | Pattern |
|--------|-----------|-----------|---------|
| Max DD | -£644 | -£898 | 2020–2026 had deeper DD |
| DD Duration | Slow grind (6+ months) | Sharp spike (2–3 weeks) | Different shapes |
| Recovery time | Fast (weeks to months) | Longer (2–4 months) | Earlier regime recovered faster |

**Key insight**: 2018–2019 drawdowns were shallow but prolonged—the strategy bled out slowly. 2020–2026 drawdowns were sharper but recovered faster. The shallower drawdown of 2018–2019 (-£644) is misleading; it's spread across a longer string of losses, which is psychologically harder to endure live.

## The Kill Gate: Triggered, But Escalated for Decision

The original backtest design had a kill gate: **if 8-year per-trade Sharpe < 0.5, flag for board review**.

The actual result: **0.31 Sharpe** — a clear trigger.

Additionally, 2018–2019 posted a per-trade Sharpe of **-0.59**, crossing the board-flag threshold of < -0.5.

By strict rule, this triggered a kill recommendation. But the decision escalated to executive judgment rather than automatic termination. Why?

## Executive Decision: Option 1 — Keep LIVE, Regime-Conditional Framing

The board chose to **retain the strategy in live deployment**, but with explicit regime-conditional posturing. The rationale:

### 1. Original Approval Evidence Is Unchanged

The 2020–2026 evidence that originally approved this strategy remains valid:
- Sharpe 0.45, +£2,937, 5/7 years profitable
- Out-of-sample outperformance (2023–2026 better than 2020–2022)
- No overfitting signatures

Adding 2018–2019 doesn't retroactively invalidate 2020–2026.

### 2. 2018–2019 Is a Known-Hostile Regime

The board interpreted 2018–2019 as a *known-bad regime* for trend-following strategies globally—not a regime-specific artifact of this strategy:
- Low vol, choppy, mean-reverting conditions defeat most momentum/trend approaches
- Expecting the strategy to profit in a regime hostile to its core logic is unfair
- The strategy is "working as designed" by losing money when trends are absent

### 3. Absolute Downside Is Bounded

A 2018–2019 redux scenario would cost ~£455 over 24 months on the deployed sizing (£50k sleeve):
- This is ~2.3% of the risk envelope
- Within the £20k drawdown gate
- Slow bleed rather than catastrophic blow-up

### 4. Explicit Risk Framing Beats Silent Risk

Rather than hide the regime-conditional nature, the board chose to:
- Document the 8-year Sharpe (0.31) as the honest long-run expectancy
- Note the 2018–2019 regime risk explicitly
- Set forward escalation triggers:
  - **6-month rolling Sharpe < 0** (daily returns)
  - **Max DD > £5k** (live capital)

If either triggers, the strategy is automatically reviewed for shutdown.

## Implications: Regime-Conditional Strategies in Live Portfolios

This case illustrates broader principles about deploying strategies based on *limited historical windows*:

### 1. Extended Validation Windows Reveal Regime Dependence

A 6-year backtest can systematically oversample favorable regimes. Adding 2–4 years of data often reveals the strategy's Achilles heel.

### 2. Regime-Conditional Doesn't Mean Non-Viable

Plenty of deployed strategies are regime-conditional. A mean-reversion strategy loses in trending markets; a trend-following strategy loses in mean-reverting markets. The question isn't "Is it regime-free?" but rather "Are the bad regimes rare enough and shallow enough that the good regimes compensate?"

### 3. Transparent Risk Framing Beats Pretended Robustness

The strategic choice here was to *acknowledge* the regime risk rather than pretend it doesn't exist. This allows:
- Conscious position sizing (don't scale up a regime-dependent strategy to equal-weight risk)
- Proactive monitoring (watch for regime shifts)
- Explicit acceptance thresholds (the £5k DD gate)

## Monitoring: Forward-Looking Regime Filters

To de-risk the regime-conditional nature, the live deployment includes monitoring for regime shifts:

**Pre-deployment regime checklist:**
- Realized vol > 12% annualized (trend-favorable environment)
- 60-day trend persistence > 3 reversals per month (momentum signal)
- Correlation with long-only index > +0.3 (drift alignment)

**Live monitoring triggers:**
- 6-month rolling Sharpe < 0 → review for pause or shutdown
- Max DD > £5k → escalate for position-size reduction
- Realized vol < 8% for 90+ days → consider pause

These are mechanical filters that don't require subjective regime judgment in the heat of trading.

## Conclusion: The Honest Backtest Window

Backtesting is an art of choosing the right window. Too short, and you overfit. Too long, and you include regimes hostile to the strategy's core logic. Too selective, and you cherry-pick favorable periods.

This 8-year validation forced a difficult but honest realization: the strategy works excellently in trending, post-COVID regimes (2020–2026) and fails in low-vol, choppy regimes (2018–2019). The long-run expectancy (0.31 Sharpe) is lower than the discovery window (0.45), but not catastrophically so.

The deployment decision—keep it live with explicit regime-conditional framing—reflects a mature risk management stance: *acknowledge the condition, monitor for its onset, and execute pre-planned exits if it realizes*. This beats both extremes: pretending the strategy is regime-free (false confidence) or retiring it based on a single bad period (throwing away genuine alpha).

The lesson for strategy developers: **expect your strategies to be regime-conditional. When 8-year backtests reveal this, it's not a failure—it's useful information for deployment.**

---

**Data sources**: 8-year equity index backtest data (USA500, 2018–2026), regime analysis including realized volatility and realized correlation, daily equity curves.

**Note on methodology**: This analysis compares discovery-window backtests (2020–2026) against extended-window validation (2018–2026) for a Donchian channel breakout strategy. The extended window required resolving a data integrity issue in 2018–2019 pricing. All metrics are derived from standard technical indicators and historical price data; no proprietary models or live deployment details are disclosed.

## What we published

- Originating research: [RAD-736](https://github.com/radiusred/RAD/issues/RAD-736) — Donchian N=55 USA500: run 8yr (2018–2026) validation after RAD-728 cache fix
- Discovery study: [RAD-726](https://github.com/radiusred/RAD/issues/RAD-726) — KR 2 Candidate A: multi-day Donchian breakout discovery on USA500 + USA100
- Publication series: [RAD-758](https://github.com/radiusred/RAD/issues/RAD-758) — Draft blog articles from Quanty research
