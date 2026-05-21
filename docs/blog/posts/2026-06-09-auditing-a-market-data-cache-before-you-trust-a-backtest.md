---
layout: default
author: Wordy
title: "Auditing a Market Data Cache Before You Trust a Backtest"
date: 2026-06-09
description: "Backtests assume the historical data is clean. It usually isn't. Here is the data-quality audit we run on our Dukascopy cache — gaps, DST seams, spread anomalies, stale prints, and cross-provider drift — before any result is allowed to matter."
tags: [engineering, data-quality, backtesting, open-source]
---

# Auditing a Market Data Cache Before You Trust a Backtest

## The unglamorous part of systematic trading

Most backtests fail in interesting ways. A strategy looks profitable, then turns out to have been trading a slice of data where the underlying price feed was wrong. A surprise gap during a DST transition gets papered over by the resampler. A run of stale prints inflates a "trend." A vendor quietly shifts a price scale and the equity curve sails on, indifferent to the fact that 2018–2019 is no longer comparable to 2024–2026.

We have made all of those mistakes in our own research at one point or another. The cheapest defence we have found is to assume the data is dirty until proven otherwise, and to run a fixed audit before any historical dataset is allowed to drive a decision.

This article walks through the audit we run against our local Dukascopy candle cache, the same one our open-source [`tradedesk-dukascopy`](https://github.com/radiusred/tradedesk-dukascopy) package produces. The audit scripts live in that repo; they are read-only, deterministic, and intentionally boring. None of this is about strategy alpha. It is about making sure a backtest is at least testing what we think it is testing.

## Why the cache is the right object to audit

`tradedesk-dukascopy` is built around a simple shape: download Dukascopy ticks once, normalise them into 1-minute bid/ask candles, persist them under a cache directory like `<cache>/<SYMBOL>/<YYYY>/<MM>/<DD>_{bid,ask}.csv.zst`, and then never touch the network during a backtest. Everything downstream — resamplers, strategies, walk-forward harnesses — reads from that cache.

That design has two consequences. First, the cache becomes the only thing a backtest needs to be honest about. Second, a single quiet corruption in the cache can poison every result computed against it from that point forward. Auditing the cache is therefore higher leverage than auditing any single backtest.

The audit ships as two scripts in the public repo:

- `scripts/dukascopy_audit.py` — a fast, local, read-only audit of the existing cache
- `scripts/dukascopy_cross_provider.py` — a cross-check of the local daily series against independent reference data

Both are meant for maintainers and researchers, not for the normal export path. They emit JSON so the output is easy to diff between snapshots and easy to gate CI or pre-research checklists on.

## What the local audit looks for

`dukascopy_audit.py` reads the bid/ask candle cache for a list of instruments over a year window and emits a per-instrument report covering four categories.

### 1. Session gaps and the longest intraday gap

A clean 1-minute candle feed should have predictable gaps: weekends, exchange holidays, the daily Dukascopy maintenance window, and (for indices) the session breaks. Everything else is suspicious.

The audit counts intraday gaps over 15 minutes, reports the longest intraday gap with its start timestamp, and excludes obvious weekend gaps so the signal stays useful. A symbol that suddenly shows a 90-minute hole in the middle of a London session is something a researcher needs to see before they run a momentum sweep on it.

### 2. DST-transition bar counts

Twice a year a 1-minute bar series picks up an unusual day: one short, one long, depending on whether the local exchange follows London, New York, or something else. Most backtesters silently swallow this; many resamplers do not.

The audit walks through the last-Sunday-of-March and last-Sunday-of-October London DST boundaries and compares the bar count on the transition day (and the day after, where drift typically shows up) against an expected baseline. The output is intentionally a soft signal — DST anomalies are not always bugs, but they are always worth eyeballing before treating that week as flat data.

### 3. Spread sanity

For each bar with both bid and ask we compute a spread, then summarise the distribution: median, 5th percentile, 95th percentile, 99th percentile, count of impossible (zero-or-negative) spreads, and count of "extreme wide" bars where the spread is more than ten times the 95th percentile.

This is the check that has caught us the most surprises. A handful of impossible spreads usually means a one-sided tick run, easy to handle. A spike in extreme-wide bars during a specific date range usually means we are looking at an instrument that was thinly quoted on Dukascopy during that period, and any backtest run over that window will overstate fill quality unless our cost model is brutal.

### 4. Stale price runs

Some instruments, particularly indices and metals proxies, occasionally print the same level for many consecutive minutes during quiet hours. The audit flags runs of stale prices so that we know whether a "low-volatility" period in our data was real or a vendor quirk.

Each of these four checks is one short, dataclass-based function in the repo. None of them try to be clever. The point is that the answers exist as numbers in a JSON file, and that we look at them before we look at any equity curve.

## Cross-checking against an independent provider

A local audit can only tell you whether the cache is internally consistent. It cannot tell you whether the cache is right. For that, the second script — `dukascopy_cross_provider.py` — compares the local Dukascopy daily close series against independent references:

- ECB / Frankfurter reference rates for FX pairs
- Yahoo Finance daily closes for indices, metals, and commodity proxies

It walks the date window day by day, joins on calendar day, computes a percentage delta, and reports counts of days where the local series disagrees materially with the reference. Persistent drift in one direction is the symptom that matters; isolated single-day spikes are usually just two providers disagreeing on which print is "the" close for a thinly-traded session.

This is the script that catches the scariest class of problem: a vendor quietly changing how it represents a price. We have seen that exactly once, and the cross-provider check is now the reason we expect to catch it the next time within a single audit cycle rather than a quarter into a backtest series.

## Where these scripts fit in the workflow

`tradedesk-dukascopy` is explicit that it is a data preparation tool, not a runtime component. The intended loop is:

1. Download and export historical data once.
2. Commit or archive the output CSV plus metadata.
3. Run fast, deterministic backtests against local files.

The audit sits between steps two and three. Concretely, in our research process the gate looks like this:

- A new instrument lands in the cache.
- Before the first hypothesis is run against it, we execute the local audit over the full available window for that instrument.
- We run the cross-provider check on the same window.
- The combined JSON output is treated as part of the data provenance for any research note that uses that instrument.

The audit costs minutes. The alternative — discovering halfway through a parameter sweep that the price scale flipped on a single instrument three years ago — costs days of rework, and worse, costs trust in every result that touched the bad data.

## What the audit deliberately does not do

A few things the audit explicitly does not try to solve, because we have learned that being honest about them is more useful than pretending:

- It does not produce a single pass/fail verdict. Data quality is a distribution, not a boolean. Researchers read the JSON.
- It does not fix the cache. The script ships read-only on purpose; repairing the cache is a separate, deliberate action.
- It does not replace cost modelling. A clean spread distribution is necessary but not sufficient; a strategy that round-trips constantly will still die on realistic spread arithmetic.
- It does not certify a backtest. It only certifies that the dataset is not obviously broken.

The framing we use internally: the audit is not the test, it is the precondition for any test being meaningful.

## Borrowing this for your own pipeline

If you are running your own backtesting stack against vendor candle data, the cheap version of this discipline is:

- Pin every dataset to a cache and never download mid-backtest.
- Pick four or five mechanical sanity checks (gaps, DST seams, spread sanity, stale runs, cross-provider drift) and run them per-instrument, per-window.
- Emit JSON, not prose. Diff successive audit snapshots. Promote a regression in any of these counters to a research blocker, not a research footnote.
- Make the audit cheap enough that nobody is tempted to skip it.

The exact scripts live in the open-source repo and are short enough to read in a sitting. The bigger point is the habit: a backtest result is only as honest as the data it touched, and the only way to know whether the data was honest is to look.

---

**Sources and code**: All audit code referenced here is in the public [`tradedesk-dukascopy`](https://github.com/radiusred/tradedesk-dukascopy) repository under `scripts/dukascopy_audit.py` and `scripts/dukascopy_cross_provider.py`, with maintainer-facing usage documented in the project [`README`](https://github.com/radiusred/tradedesk-dukascopy/blob/main/README.md). No private research output, strategy parameters, or live deployment details are referenced in this article.
