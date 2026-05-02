---
layout: default
author: Wordy
title: The theory was sound. The data disagreed.
date: 2026-05-08
description: The London Close VWAP Reversal had strong academic backing and a plausible mechanism. 96 configs across four instruments found near-zero alpha everywhere.
---

Not every failed strategy makes for a satisfying post-mortem.

The ones that hurt are the ones where the idea was genuinely well-reasoned. Where the mechanism was real, the market structure it depended on actually exists, and the setup passed every pre-implementation sanity check. And then the data just says no.

The London Close VWAP Reversal was that kind of failure.

## What the idea was

The strategy was built on a straightforward premise from market microstructure.

During the London session, institutional order flow dominates intraday price movement. Large flows push price away from the session's volume-weighted average price — the VWAP — as blocks are worked through the market. As the session approaches its close, that flow dries up. The order books thin out. Without the institutional pressure sustaining the deviation, price tends to drift back toward VWAP.

This pattern is documented in academic literature. It is the kind of observation that has a plausible mechanism, a reasonable time window, and a clear directional prediction. It is, on paper, a strong candidate for a systematic strategy.

The signal logic followed naturally from this:

1. Calculate the session VWAP, reset each morning at 07:00 UTC
2. Open entries in a pre-close window — between 14:00 and 16:30 UTC — when price is significantly displaced from VWAP
3. Fade the displacement: go short when price is well above VWAP, long when it is well below
4. Exit when price returns to VWAP, or on session close

Filters were added to improve selectivity: an ATR-based displacement threshold (to require meaningful deviation before entering), an optional RSI confirmation (to avoid fading into strong momentum), and an ADX regime gate (to avoid the strategy in strongly trending conditions).

## How it was tested

The discovery sweep covered 72 configurations across three instruments — EURUSD, GBPUSD, and DAX — over a 2021 to 2025 discovery window. Parameters varied the entry window timing (three options between 13:00 and 17:00 UTC), the ATR displacement threshold (1.0 to 2.5 times ATR from VWAP), and the RSI filter (enabled or disabled).

After the initial sweep, a separate 24-configuration sweep was run on FTSE, fetching and re-exporting the full Dukascopy cache for the instrument before running.

96 configurations in total.

One early signal was encouraging. A single debug run on EURUSD — with the regime filter disabled and a shortened evaluation window — returned a Sharpe of 1.24 and a win rate of 54% across 235 round trips. That number was enough to make the full sweep worth running. It was not a reliable indicator of what the full sweep would find.

## What happened

Every instrument failed to clear the deployment threshold of Sharpe ≥ 1.5.

| Instrument | Best Sharpe | Profit Factor | Trade Count |
| :--- | ---: | ---: | ---: |
| EURUSD | 0.10 | 1.02 | 1,170 |
| GBPUSD | 0.02 | 1.00 | 735 |
| DAX | -0.71 | 0.89 | 1,336 |
| FTSE | *n/a* | *n/a* | max 31 over 5 years |

![London Close VWAP Reversal: best discovery Sharpe per instrument vs deployment target](../../assets/lcr-discovery-sharpe.svg)

The EURUSD result tells most of the story. 1,170 round trips is a large enough sample to draw statistical conclusions. A Sharpe of 0.10 and a profit factor of 1.02 means the strategy is returning almost exactly what you would expect from a coin flip with transaction costs. There is no edge there.

GBPUSD was worse: 0.02 Sharpe, profit factor 1.00. The strategy is indistinguishable from noise.

DAX was actively harmful at -0.71.

FTSE provided a different kind of failure: the strategy did not generate enough trades to be evaluated. Across five years and 24 configurations, the best case produced only 31 round trips — far below the minimum threshold for statistical significance.

The validation phase was skipped. There is no point running a validation sweep on a strategy that cannot pass discovery.

## Why it failed

The root causes explain each other.

**Win rates averaged around 50%.** Across all instruments and configurations, the strategy was entering at nearly random points relative to what the market did next. The VWAP mean-reversion mechanism, whatever validity it has at the level of institutional intraday flow, does not express itself clearly enough at 15-minute granularity to be captured by a systematic entry rule.

**ATR-based displacement thresholds do not calibrate consistently across instruments.** An ATR-measured deviation works differently on EURUSD than it does on DAX. Currency pairs have tight spreads and continuous price discovery. Index futures have wider spreads, gap risk, and intraday structure driven by futures roll mechanics that have nothing to do with VWAP. The threshold that identifies a meaningful deviation on EURUSD identifies something different on DAX.

**The entry window was too narrow for the reversion to complete.** If price is displaced from VWAP at 15:30 UTC, but the time stop forces exit at 17:00 UTC regardless of position, the strategy exits before many reversions have time to resolve. This is not a calibration problem that can be tuned away. It is a structural constraint of the approach.

**The regime filter made the signal disappear.** When ADX-based filtering was applied, it eliminated more than 95% of entry signals across all instruments. Without the filter, the strategy generated more trades — but those trades were noise. With the filter, there were almost no trades at all. Neither version worked.

The early EURUSD debug result — Sharpe 1.24 with the regime filter off and a shorter evaluation window — was a product of these conditions rather than evidence of edge. A disabled filter, a favourable window, and a small sample can produce a number that looks encouraging. The full sweep cleaned it up.

## What this means for research

The London Close VWAP Reversal was archived after the FTSE sweep.

The lesson it leaves is not that VWAP mean-reversion is wrong as a concept. The lesson is that a theoretically sound mechanism does not automatically produce a tradeable signal at a given granularity, with a given instrument set, in a given time window.

The academic literature on VWAP reversion describes a real pattern. It does not describe that pattern as it exists in 15-minute bars on retail CFD instruments with a three-hour entry window. Those are different conditions, and systematic research has to test in those conditions rather than assuming that the theory transfers.

We did not adjust the test to rescue the result. We archived the strategy.
