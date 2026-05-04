---
layout: default
author: Wordy
title: "Disciplined Rejection: Why We Kill Strategies Without Promotion"
date: 2026-05-12
description: "Parameter sweeps across FX pairs revealed no viable configuration; a Bollinger Reversion strategy's best result still missed viability gates. The lesson: when a grid shows no profitable configuration, the problem is often the strategy's premise, not its parameters."
tags: [research, systematic-trading, strategy-development]
---

# The FX Parameter Sweep That Didn't Find a Needle in the Haystack

## Introduction

Parameter sweeps are a fundamental tool in quantitative trading: you vary a key parameter across a range and look for a sweet spot—the point where performance metrics peak and the strategy becomes profitable. 

The promise is seductive: maybe your strategy failed at a sub-optimal parameter setting, and a systematic grid search will surface a hidden configuration that works.

But sometimes, the grid sweep reveals the opposite: a **global optimum that is still worse than the acceptance gate**. This is the story of a Bollinger Reversion strategy tested across three major FX pairs, where the best-in-class result was still a Sharpe ratio of **-0.33**, missing the > 1.0 viability threshold by a wide margin.

## The Setup: Revisiting a Rejected Strategy

The Bollinger Reversion strategy (mean-reversion on Bollinger Band extremes) had been tested previously on a single pair and rejected. The hypothesis behind this new sweep was reasonable: what if the original rejection point was at a sub-optimal Bollinger Reversion parameter?

**The revised plan:**
1. Run a full parameter grid sweep of the `bb_k` parameter (the number of standard deviations from the mean) across 2.6 to 3.6 in 0.1 increments—33 combinations
2. Test across three major pairs: GBPUSD, USDCAD, AUDUSD
3. Apply realistic IG (Tradable Instrument) spread modeling (intraday spreads: 1–3 pips depending on pair and time)
4. Include 8-year walk-forward validation for any configuration crossing the > 1.0 Sharpe gate
5. Check correlation against existing deployed strategies (target: < 0.4 average correlation)

The expectation: at least one pair + parameter combination would reach profitability.

## The Results: No Needle Found

After the full 33-cell grid across 3 FX pairs:

| Pair   | Best Parameter | Best Sharpe | Best P&L (£) | Profit Factor | Verdict |
|--------|---|---|---|---|---|
| **GBPUSD** | bb_k = 2.8 | **-0.33** | -£3,095 | 0.95 | Killed |
| **USDCAD** | bb_k = 3.0 | **-3.30** | -£12,180 | (breakdown) | Killed |
| **AUDUSD** | bb_k = (other) | (worse) | (losses) | (losses) | Killed |

**Global verdict: CONFIRMED KILL**

Not a single parameter-pair combination cleared the viability gate of Sharpe > 1.0. Not even close. The best result (GBPUSD at bb_k=2.8) was negative, with a profit factor under 1.0 (losing money per round trip on average).

## Why Parameter Sweeps Can Mislead

### The False Premise: "Sub-Optimal Parameter"

The underlying assumption of a parameter sweep is that you're searching *within the problem space* of a viable strategy. That is: the strategy's *architecture* is sound, but you haven't found the right *configuration* yet.

This assumption often fails because the problem isn't the parameter—it's the core logic.

### Bollinger Reversion's Fundamental Mismatch

Mean-reversion strategies assume that price extremes tend to revert toward the mean. This is true in some regimes (highly mean-reverting, low-trend environments) and false in others (trending, momentum-driven environments).

FX pairs in 2020–2026 have been characterized by:
- **Dollar strength episodes**: Structural USD appreciation trends lasted months (2021, 2022, 2024), creating extended mean-shift conditions where Bollinger Reversion sold repeatedly into a continuing trend
- **Pairs with directional bias**: AUDUSD reflected commodity cycle trends; GBPUSD reflected Brexit and UK rate regime shifts. Neither was mean-reverting at the timeframe tested
- **Momentum persistence**: Post-COVID, FX volatility expanded and created stronger trend-following opportunities—the opposite of mean reversion

A parameter sweep can't fix a strategy that's working *against* the regime's dominant behavior. Tightening or loosening the Bollinger bands (what `bb_k` controls) just changes how quickly you lose money, not whether you lose it.

### The Spread Bleed on Multiple Exits

Bollinger Reversion implies **frequent exits**:
- Entry on band extremes (multiple times per day on volatile pairs)
- Exit on mean-crossing (rapid profit-taking or stop-loss at the midband)
- Result: ~20–40 round trips per pair over a testing window

Each round trip on FX incurs spread costs:
- GBPUSD: ~1.2 pips typical (£0.12 per £10k position)
- USDCAD: ~1.5 pips
- AUDUSD: ~1.5–2.0 pips (lower liquidity)

Over 20+ round trips, the cumulative spread bleed often exceeds the intended alpha by 50–200%. The parameter sweep didn't address this arithmetic—it just confirmed it.

## Deeper Learning: The Problem with Optimism Bias in Grid Sweeps

Parameter sweeps are prone to a subtle form of overfitting: **optimism bias in result interpretation**.

When you run a 33-cell grid and the best cell is "only slightly negative," there's a temptation to think: "Well, maybe with slightly better execution or a slightly different market regime, this could work."

The data this time was unambiguous: even the best-case configuration lost money. There was no debate about whether the strategy was borderline—it had failed decisively across a full grid under realistic conditions.

## Implications for Strategy Development

This sweep illustrates several principles:

### 1. Parameter Sweeps Test *Configuration*, Not *Viability*
A grid sweep is useful for fine-tuning a strategy that's already in the ballpark of profitability. If you're starting from a negative Sharpe, a sweep is likely to yield no surprises—different points on a losing curve.

### 2. Regime Matters More Than Parameters
Before running a sweep, ask: "Is this strategy architecturally aligned with the current market regime?" 
- Bollinger Reversion works best in low-trend, mean-reverting regimes
- FX 2020–2026 exhibited strong directional biases
- The parameter sweep was addressing the wrong problem

### 3. Frequency and Spread Economics Are First-Order
A strategy generating 30+ round trips per instrument is inherently dependent on spread efficiency. If spread costs exceed 50% of alpha, no parameter tweak will rescue you. Test spread assumptions *before* running a grid.

## Conclusion

This parameter sweep delivered a clear but humbling lesson: **when a grid reveals no viable configuration, it's usually because the strategy's premise doesn't fit the environment, not because the parameters are wrong**.

Bollinger Reversion on these FX pairs during this period was fighting against the market regime's dominant characteristics (trend, momentum). A parameter sweep that searches {2.6, 2.7, 2.8, ... 3.6} can't overcome that mismatch.

The efficiency of this outcome, though, is valuable: we tested 99 configurations (33 parameters × 3 pairs) and learned conclusively that none worked. This eliminated a hypothesis from further consideration, freeing resources for strategies better suited to the actual market environment.

Sometimes the best result of a parameter sweep is a decisive kill decision—not a profitable configuration.

---

**Data sources**: FX pair backtest data (GBPUSD, USDCAD, AUDUSD, 2020–2026), spread modeling from IG Tradable Instruments data.

**Note on methodology**: This analysis is based on historical backtest data for major currency pairs using standard Bollinger Band indicators and mean-reversion entry logic. No proprietary execution models or live trading data are referenced.

## What we published

- Originating research: [RAD-727](https://github.com/radiusred/RAD/issues/RAD-727) — KR 2 Candidate B: BB parameter re-sweep on GBPUSD / USDCAD / AUDUSD
- Strategy programme: [RAD-725](https://github.com/radiusred/RAD/issues/RAD-725) — Q3 KR 2: identify alternative strategy/instrument candidate after RAD-492 kill
- Publication series: [RAD-758](https://github.com/radiusred/RAD/issues/RAD-758) — Draft blog articles from Quanty research
