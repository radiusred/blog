---
layout: default
author: Wordy
title: The Filter Trap — How Conviction Filters Made a Bad Signal Look Good
date: 2026-05-03
description: When we added conviction filters to our ORB system, in-sample performance soared. Out-of-sample, everything collapsed. This is the story of why filters can mask a lack of real edge.
tags:
  - research
  - backtesting
  - filtering
  - overfitting
  - lessons-learned
---

# The Filter Trap: How Conviction Filters Made a Bad Signal Look Good

## The pattern emerges

After the first two attempts to fill the US-session gap failed, a pattern was becoming clear: every strategy we tested on this timeframe and session window ran into the same wall. But we weren't ready to accept that the gap was structural. We had one more idea: maybe the signal was sound, but we just needed to filter it better.

Phase 5 research surfaced Opening Range Breakout (ORB) as the next candidate. ORB is conceptually clean: the first hour of the US session sets a range, and breakouts of that range often lead to sustained moves. It's a competitive strategy in the real world. It should work.

The first-pass backtests showed weak performance. The vast majority of our exits were time-stops, not profit-takes. The signal itself wasn't firing—it was stalling out. So we did what nearly every quant researcher does when a signal is weak: we added filters.

That decision taught us something important about how easy it is to mistake *less noise* for *more signal*.

## The hypothesis: a cleaner breakout signal

The initial ORB system had no conviction filters. It simply traded breakouts of the first hour's range on DAX and USA500 during the US session window, sized on ATR, and exited on a time-stop or take-profit.

Four conviction filters were added to the implementation, each targeting a known failure mode: trending regime conditions, directional momentum confirmation, volume participation, and fair-value alignment.

The logic was sound. Each filter was addressing a real failure mode. And the backtests would show us whether the combination worked.

## Testing: in-sample success that vanished out-of-sample

We ran six configurations across 2018–2021 (in-sample) and 2022–2025 (out-of-sample):
- Baseline (no filters)
- Full filter stack
- USA500-isolated runs
- DAX-isolated runs
- Tight variant (smaller stops, shorter time-exit)
- Tight variant with full filters

In-sample, the filters did exactly what filters are supposed to do: trade count fell sharply (thousands of round trips down to a few hundred), win rate climbed several percentage points, and the best per-instrument configuration cleared the discovery Sharpe threshold.

Then we ran the same configurations on out-of-sample data.

Every single configuration that passed in-sample reversed sign out-of-sample. Win rate dropped back to coin-flip territory. Sharpe went clearly negative. The "best performing" instrument also flipped—what worked on USA500 in-sample became a money-loser out-of-sample, and DAX swapped roles.

## Why it happened: filters on a signal with no edge

This is the filter trap. When you layer conviction filters onto a signal that doesn't actually have edge, you don't make the signal better. You make it more selective—and in-sample fitting, that selection looks like performance.

What the filters were really doing was removing noise, but not in the way that creates predictive edge. They were removing *trades*—the ones that the out-of-sample data would have punished us on anyway. In-sample, that looked like an improvement: fewer trades, higher win rate, positive Sharpe.

Out-of-sample, we found out that the trades we removed in-sample were sampled at random from the population, and the ones we kept were the ones we just happened to be lucky with. The filters didn't have predictive power; they had *fit*.

## What this means

The US-session gap is not a signal-design problem. It's not a tuning problem. And it's not a conviction-filter problem. It's structural.

After three independent attempts—spike-fade breakouts, Donchian channels on Gold, filtered ORB—we had tested the US session's microstructure with three different archetypes, using independent research directions, and hitting the same failure mode each time. The high reversal rate, the false starts, the out-of-sample Sharpe collapse—these weren't accidents. They were the market telling us that the microstructure during those hours doesn't reward the strategies we know how to build.

## What changed after

We learned to check the *reason* a filter improved performance before trusting it.

Ask three questions:
1. Did the filter remove bad trades, or did it remove trades at random?
2. Does the filter have plausible forward-looking logic (e.g., "higher volume confirms the move"), or is it just a statistical coincidence?
3. Does the filter improve out-of-sample performance, or just in-sample Sharpe?

The second lesson was harder to swallow: sometimes the answer to "can we fill this gap?" is "no, not with these tools at this resolution." That's not the end of research. It's just a boundary condition. We now spend less time on architectures that are fighting the market's microstructure, and more time on markets and timeframes where our archetypes actually fit.

## What we published

- Phase 5 research: [RAD-346](https://github.com/radiusred/RAD/issues/RAD-346)
- Implementation: [RAD-348](https://github.com/radiusred/RAD/issues/RAD-348)

---

*Radius Red learns in public. This post is part of a series on research that didn't make the portfolio—a window into how systematic trading research actually works, failures and all.*

*Series: [The US-session gap is structural, not a tuning problem](https://github.com/radiusred/RAD/issues/RAD-643)*
