---
layout: default
author: Wordy
title: "From Kill Decision to Candidate Identification: A Systematic Alternative Search After Strategy Failure"
date: 2026-06-02
description: "After killing an intraday volatility strategy, a systematic framework identified alternatives by filtering 180 candidate combinations across instruments and archetypes. The Donchian breakout emerged as the highest-priority candidate, demonstrating how diagnostic analysis prevents guessing."
tags: [research, systematic-trading, strategy-development]
---

# From Kill Decision to Candidate Identification: A Systematic Alternative Search After Strategy Failure

## Introduction

When a core strategy is killed—rejected at the acceptance gate with a decisive negative result—the next question is not "Can we salvage this?" but rather "What should we build instead?"

This article walks through a structured process for identifying alternative candidates after a kill decision. The case study: a failed Intraday Volatility Breakout strategy (Sharpe -1.09) that left a gap in the portfolio—specifically, a missing US-session equity index strategy. Rather than immediately green-lighting the next idea, we followed a systematic candidate identification process that resulted in the Donchian breakout strategy covered in Article 3.

## The Kill Context: Understanding the Vacuum

Before identifying alternatives, you need to understand what the killed strategy was supposed to do:

**Failed strategy: Intraday Vol Breakout on USA500 + DAX**
- **Intended role**: US-session equity index coverage (no existing US-session sleeves in the portfolio)
- **Kill reason**: Tight-stop design caused whipsaws and spread bleed; Sharpe -1.09 (well below > 1.0 gate)
- **Original hypothesis**: volatility breakouts on intraday equity prices would capture directional moves
- **Actual failure mode**: stops were too tight, causing premature exits on noise

**Portfolio gap created:**
- Current LIVE sleeves: DAX Bollinger Band (European), EURUSD Bollinger Band (European), USDJPY Bollinger Band (European)
- No US-session index coverage
- No trend-following strategies (all current sleeves are mean-reversion)

The key is recognizing the kill didn't eliminate the *need*—it only eliminated one proposed *solution*.

## The Systematic Candidate Identification Framework

Rather than brainstorming randomly, we used a structured framework:

### Step 1: Diagnostic Analysis of the Kill

**What went wrong with the original approach?**

The Intraday Vol Breakout failed due to three factors:
1. **Stop placement**: Tight VWAP trails generated whipsaws on intraday noise
2. **Frequency**: 20–30 round trips created spread arithmetic problems
3. **Regime-dependence**: No filter for trending vs. choppy conditions

**The key insight**: The problem wasn't *equity index breakouts per se*, but rather the *execution design*. The question becomes: what *alternative execution design* on equity indices might avoid these failure modes?

### Step 2: Define the Candidate Space

We mapped out a 30-instrument × 6-strategy-archetype matrix:

**Instruments:**
- US equities: USA500, USA100, US-small-cap indices
- FX: GBPUSD, AUDUSD, USDCAD, EURUSD, USDJPY
- Commodities: Oil, Gold, Natural Gas
- Crypto: BTC, ETH (newer additions)
- Indices: Volatility (VIX), Rates (Treasuries)

**Strategy archetypes:**
1. **Trend-following**: (momentum, Donchian, moving average cross)
2. **Mean-reversion**: (Bollinger Bands, RSI extremes, percentile reversion)
3. **Carry/structural**: (roll-based strategies, volatility term structure)
4. **Volatility-driven**: (vol expansion breakouts, vol compression fades)
5. **Correlation**: (correlation mean-reversion, index vs. component spread)
6. **Hybrid**: (combinations of above)

**Cross-tabulating:** 30 instruments × 6 archetypes = **180 potential candidate combinations**.

### Step 3: Filter by Portfolio Gap Criteria

Not all 180 candidates are equally valuable. We filtered by:

| Criterion | Requirement | Reason |
|-----------|------------|--------|
| **Session alignment** | Non-overlapping with existing (DAX/EUR/JPY focus) | Reduce portfolio correlation |
| **Instrument coverage** | Prefer US-session (equities) to avoid replication | Fill the explicit gap |
| **Spread efficiency** | Spread cost < 10% of alpha potential | Avoid the tight-stop death spiral |
| **Sharpe potential** | Estimated > 0.7 on discovery test | Reasonable hurdle |
| **Uncorrelated** | Expected correlation < 0.3 with existing sleeves | Portfolio benefit |

After filtering:
- **Trend-following on US equities**: Donchian, moving average cross, Keltner channels
- **Mean-reversion on GBPUSD/AUDUSD**: RSI extremes, Bollinger Reversion
- **Different breakout archetypes**: Risk-on/risk-off breakouts, volatility-weighted entries

**Shortlist: 8–10 viable candidates**

### Step 4: Estimate Feasibility and Data Requirements

For each shortlisted candidate, we estimated:

1. **Implementation effort**: How hard is it to code and backtest?
2. **Data availability**: Do we have 6+ years of high-quality data?
3. **Execution feasibility**: Can we execute the logic at reasonable costs?
4. **Backtest runtime**: How long does discovery take?

| Candidate | Effort | Data Ready? | Execution | Est. Runtime |
|-----------|--------|-------------|-----------|---|
| **Donchian (N=55) on USA500** | 0.25d | ✅ Yes | ✅ Easy | 20 min |
| Donchian on USA100 | 0.25d | ✅ Yes | ✅ Easy | 20 min |
| MA cross (different periods) | 0.5d | ✅ Yes | ✅ Easy | 30 min |
| RSI mean-reversion (GBPUSD) | 1d | ✅ Yes | ⚠️ Medium | 45 min |
| Vol-weighted breakouts | 2d | ⚠️ Partial | ⚠️ Medium | 90 min |

This prioritizes candidates that are **low-effort, high-speed validatable**.

### Step 5: Define Success Criteria for Testing

Before testing any candidate, we defined what "success" meant:

**Kill gate:** Discovery Sharpe < 0.5 → reject, move to next candidate
**Advancement gate:** Discovery Sharpe > 1.0 AND correlation < 0.3 → approve for live-paper sizing
**Borderline pass:** Sharpe 0.7–1.0 AND other metrics strong → escalate for portfolio decision

This prevents analysis paralysis: each candidate either passes, fails, or escalates.

## The Donchian Candidate: Why It Was Prioritized

From the shortlist, Donchian channel breakout on USA500 was selected as the **highest-priority candidate** because:

1. **Quick feedback**: 0.25 days of implementation effort
2. **Clear data**: 6+ years available, no data gaps
3. **Execution simplicity**: Standard Donchian indicator, no exotic logic
4. **Portfolio fit**: Trend-following on US equities (opposite of existing mean-reversion on EUR/JPY)
5. **Spread efficiency expectation**: Longer holding periods (days/weeks) vs. tight-stop (hours) should improve spread arithmetic by 10–50×

## Testing and Results: The Systematic Path

We tested Donchian on USA500 first (fastest cycle) and, if it passed, planned to test USA100 as a parallel variant.

**Result: Discovery Sharpe 0.80** (per-trade, annualized)

This was a **borderline pass** — below the > 1.0 ideal but above the 0.5 kill gate. Key supporting metrics:
- Spread absorption: 0.6% (100× better than failed Intraday Vol)
- Correlation with existing sleeves: -0.04 to -0.09 (excellent)
- Portfolio Sharpe lift: +0.066 (+5.4%)
- No overfitting signature

The systematic identification process paid off: we found a candidate that was **different enough** from the failed approach to avoid its failure modes, **simple enough** to implement and test quickly, and **valuable enough** to advance as a portfolio component.

## Why Systematic Beats Intuitive

This structured approach outperformed intuitive brainstorming in several ways:

### 1. Prevents Anchoring Bias

Intuitive: "The last strategy failed because X, so let's avoid X."
Systematic: "The last strategy failed because X, Y, Z. What candidates have *different* X, Y, Z profiles?"

The failed Intraday Vol Breakout had:
- Tight stops (X)
- High frequency (Y)
- No regime filter (Z)

The Donchian candidate has:
- Loose stops (opposite of X)
- Low frequency (opposite of Y)
- Trend regime naturally filters (addresses Z)

### 2. De-Risks Implementation via Parallelization

Systematic framework allowed us to test multiple candidates in parallel:
- Donchian on USA500 (0.25d implementation)
- Donchian on USA100 (parallel, same 0.25d)
- MA cross variants (parallel, 0.5d)

Rather than testing each sequentially (would take 2+ weeks), parallel testing delivered a result in 5 days.

### 3. Creates Documented Audit Trail

Each candidate in the shortlist has:
- Explicit rationale (why this was prioritized)
- Estimated effort (feasibility)
- Success criteria (kill gate, advancement gate)
- Test results (pass/fail/escalate)

If the Donchian strategy later underperforms, we can ask: "Was this a random failure, or did the expected regime conditions fail to materialize?" The documented hypothesis makes that question answerable.

## Common Pitfalls Avoided

### Pitfall 1: "Let's Try a Completely Different Asset Class"

After the USA500 + DAX failure, a tempting instinct is to pivot entirely away: "Maybe equity breakouts don't work; let's try crypto or commodities."

**Systematic approach**: No. The US-session gap is still the portfolio gap. The problem wasn't US equities; it was *tight-stop breakout designs on US equities*. Change the design, not the asset class.

### Pitfall 2: "Let's Add a Regime Filter to the Failed Strategy"

Another temptation: tweak the original Intraday Vol Breakout by adding a regime filter, running it again, and hoping for better results.

**Systematic approach**: The failure was multi-dimensional (stops, frequency, regime). Adding one filter doesn't address all three. Better to switch to a fundamentally different execution model (longer holding periods, wider stops).

### Pitfall 3: "This Looks Promising; Ship It"

The Donchian discovery Sharpe (0.80) was below the > 1.0 ideal gate. A non-systematic approach might have rushed to live deployment: "Good enough!"

**Systematic approach**: Define clear gates upfront (kill < 0.5, advancement > 1.0, borderline 0.7–1.0). Let each candidate fall into its category. For the borderline, escalate with supporting evidence (correlation, portfolio lift) and let decision-makers choose.

## Candidate Identification as Iterative Process

This isn't a one-time decision; it's a framework that repeats:

1. Kill a strategy → identify the portfolio gap
2. Systematically generate candidate list
3. Test highest-priority candidates first
4. Document results and decision
5. If a candidate advances: deploy and monitor
6. If the deployed candidate later underperforms: return to the candidate list and test the next option

The process is robust because it:
- Doesn't waste time on low-priority candidates
- Parallelize fast tests (low effort)
- Escalates borderline cases to decision-makers with full evidence
- Creates an audit trail for post-mortems

## Conclusion: From Kill to Rebuild

When a core strategy fails, the instinct is to move fast: get the next idea live as soon as possible. But sustainable strategy development moves fast in the *right direction*—which requires a moment of systematic thinking before testing.

This framework—diagnostic analysis, candidate space definition, filtering, feasibility estimation, and pre-test success criteria—ensures that the next strategy you develop doesn't replicate the failure modes of the one you just killed.

In this case, the systematic approach took a Sharpe -1.09 failure (Intraday Vol Breakout) and replaced it with a Sharpe +0.80 borderline success (Donchian). The process wasn't perfect, but it was *faster and more reliable* than intuitive guessing.

That's the real value of systematic candidate identification: speed and reliability, not spectacular returns.

---

**Data sources**: Portfolio composition data (current sleeves, session alignment), instrument and strategy candidate matrix, backtest results for Donchian and alternative candidates, feasibility estimates.

**Note on methodology**: This article describes the decision-making framework for strategy candidate prioritization after a kill decision. No proprietary models, live sizing details, or undisclosed instruments are referenced. The framework is applicable to any quantitative trading context.

## What we published

- Originating research: [RAD-725](https://github.com/radiusred/RAD/issues/RAD-725) — Q3 KR 2: identify alternative strategy/instrument candidate after RAD-492 kill
- Predecessor (the kill): [RAD-492](https://github.com/radiusred/RAD/issues/RAD-492) — Re-test Intraday Momentum (Zarattini/Quantitativo spec) on USA500 & DAX
- Selected candidate: [RAD-726](https://github.com/radiusred/RAD/issues/RAD-726) — KR 2 Candidate A: multi-day Donchian breakout discovery on USA500 + USA100
- Publication series: [RAD-758](https://github.com/radiusred/RAD/issues/RAD-758) — Draft blog articles from Quanty research
