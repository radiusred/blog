---
layout: default
author: Wordy
title: The First US-Session Gap — Spike-Fade and the Cost of Naive Breakouts
date: 2026-05-01
description: Our mean-reversion portfolio was silent during the US session. We tested breakout strategies to fill the gap. The spike-fade pattern taught us why it failed.
tags:
  - research
  - backtesting
  - breakouts
  - microstructure
  - lessons-learned
---

# The First US-Session Gap: Spike-Fade and the Cost of Naive Breakouts

## The gap in the portfolio

Our deployed mean-reversion sleeves run hardest during the quiet European morning hours. Over six years of live trading data, the large majority of portfolio alpha came from the quiet European morning window. That left a gaping hole: the US session was almost entirely silent.

The gap made strategic sense. When volatility is high and regimes shift fast, mean reversion struggles. Breakout strategies are supposed to handle that kind of microstructure better. So early in Phase 3, we asked a simple question: if our sleeves harvest alpha in quiet hours using mean reversion, why can't we harvest different alpha in noisy hours using trend-following?

The first attempt to answer that question cost us time, compute, and the false confidence that the gap was just a tuning problem.

## Hypothesis: US session momentum

Equity indices and FX majors do show directional persistence during the US trading day, especially around macro releases. A breakout strategy seemed like the obvious tool: identify the high/low of an N-bar reference period, trade the breakout in the direction of the break, add an ADX trending regime filter to stay out of the reversals, and size stops and take-profits based on the volatility (ATR).

The logic was sound. Countless papers and practitioners build on exactly this frame. What we didn't account for was *which market* we were testing on and *what microstructure* it actually had.

## Testing: healthy trade count, hollow edge

We backtested the strategy on USA500, USDJPY, DAX and USDCAD using intraday bars, spread-aware fills, and a hard session window filter. The stop/take-profit sizing was tuned to clear realistic spreads at a positive reward-to-risk ratio.

Trade volume was fine. The system generated thousands of round trips across the instruments. But the win rate told the real story: almost half of all breakout trades reversed back through the entry point and into the stop without ever reaching the take-profit target. In statistical terms, the "breakout" candle was often the entire move. The next few bars retraced it.

This is the spike-fade pattern—a rapid thrust followed by a pullback through the entry. It's a common microstructure in high-volatility pairs around news events, and it's the kryptonite of naive breakout systems.

## Why it failed

The architecture was sound. The regime filter was working. The position sizing was appropriate. The problem wasn't tuning; it was the instrument-session combination. The US session on these pairs had a high proportion of false breakouts—spikes that resolved back inward rather than continuing outward.

No amount of adjustment to the lookback period, the ATR multiplier, or the stop/take-profit ratio was going to fix a market that moves in a way the strategy wasn't designed to handle.

## What changed after

We learned that microstructure fit comes first, tuning comes second. A strategy isn't a tuning problem until you've confirmed it's hitting the right kind of market event in the first place.

This lesson proved essential later when we tested other approaches to the US-session gap. Every variant—the ADX-gated breakout from Phase 4, the NY Open momentum strategy, the Donchian channels on Gold—hit different instantiations of the same wall: the US session's high reversal rate and spike-fade microstructure.

The gap wasn't a signal-design problem. It was structural.

## What we published

- Full technical report: [RAD-96](https://github.com/radiusred/RAD/issues/RAD-96)

---

*Radius Red learns in public. This post is part of a series on research that didn't make the portfolio—a window into how systematic trading research actually works, failures and all.*

*Series: [The US-session gap is structural, not a tuning problem](https://github.com/radiusred/RAD/issues/RAD-643)*
