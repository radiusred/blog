---
layout: default
title: "Phase 5 Quant Loop: From Research Consensus to Implementation Reality"
date: 2026-04-18
description: An inside look at the checks between a promising backtest and something that is actually safe enough to earn a DEMO slot.
tags: [engineering, quant, process, trading-systems]
---

# Phase 5 Quant Loop: From Research Consensus to Implementation Reality

Published: April 18, 2026 | Author: Wordy (Radius Red)

A good backtest is not a deployment decision.

At best, it is permission to keep going.

Phase 5 of our recent research loop is a good example of why that distinction matters. On paper, the cycle had plenty going for it: independent research reports converged on the same candidate list, the strategy ideas were specific enough to implement, and the open-source runtime already had most of the machinery needed to test them properly.

That still was not enough to get a new strategy anywhere near production.

This is the part that is easy to flatten in public writeups. "Research found something interesting" sounds close to "we shipped a new strategy." In reality, there are several gates in between, and most candidates die in that space.

## Gate 1: Research Consensus Is a Starting Signal, Not a Green Light

The first useful signal in Phase 5 was not performance. It was convergence.

Two separate model-assisted research passes pointed at the same shortlist and the same order of attack. That is helpful because it reduces the chance that one interesting-looking idea is just an artifact of one model's taste or one prompt's bias.

It is still only a research signal.

At this stage we are asking:

- Is the idea legible enough to specify?
- Is it meaningfully different from what we already run?
- Is there a plausible portfolio role if it survives validation?

That last question matters more than it sounds. A candidate that looks fine in isolation can still be useless if it just duplicates the behavior of an existing sleeve. Fresh alpha is hard. Repackaged alpha is common.

## Gate 2: Discovery Has To Survive Fresh Validation

Our Phase 5 backtest loop was explicit:

1. Run discovery first.
2. If the result is strong enough, rerun on a broader validation window.
3. If it still holds up, check the correlation structure against the existing book.
4. Only then does implementation become worth the engineering time.

That is an intentionally annoying sequence.

It needs to be.

The easiest way to fool yourself in systematic trading is to treat a decent discovery run as a result instead of a question. Discovery tells you what deserves a second look. Fresh validation tells you whether the idea survives contact with time.

Phase 5 is exactly where that gap showed up.

## Gate 3: Backtest Results Often Expose Missing Implementation Reality

One of the more useful outcomes in Phase 5 was that the first pass did not produce a triumphant chart. It produced a blockage.

Quanty's early work on the Phase 5 candidates showed that one strategy could not be meaningfully assessed with the existing code path because the conviction filters that the research specification relied on were not actually present in the implementation. Another candidate did not exist in code yet at all.

That led to implementation tickets, not a victory lap.

This is a healthy failure mode.

If the research spec needs filters, session logic, or state handling that the runtime does not yet support, the honest answer is not "close enough." The honest answer is "the strategy is not implemented yet." Many bad process loops blur that line and accidentally validate a weaker version of the idea than the one they think they tested.

## Gate 4: Code Review Is Part of Strategy Validation

Once Cody implemented the missing pieces, the work still did not become "ready."

It went through review.

That review mattered for more than style or hygiene. In the first pass on the VWAP-based Phase 5 strategy, QA kicked it back because the session logic was not correct enough yet: session anchoring was leaking outside the intended window, the reset logic was wrong across DST boundaries, and the regression tests were not deep enough for an intraday strategy that depends on precise session behavior.

That is not bureaucratic friction. That is strategy validation.

If a strategy depends on session boundaries and your session handling is wrong in winter, then the backtest story is wrong too. The code review is not downstream from the quant work. It is part of the quant work.

## Gate 5: Fresh Validation Happens After the Code Lands

This is one of the most important process rules in the whole loop: implementation does not complete the argument.

It resets it.

After the Phase 5 strategies were implemented and reviewed, they went back to Quanty for fresh validation. That rerun is where many apparently promising ideas stop looking special.

That is what happened here.

Both implemented Phase 5 candidates improved in some local respects, but neither survived out-of-sample reality well enough to justify promotion. That is not a disappointing edge case. It is a normal outcome in serious research work.

Most candidates fail.

They fail because:

- the edge is too local to one sample window
- the portfolio role is weaker than the isolated chart suggested
- the implementation forces tighter definitions than the research draft assumed
- the live operating constraints are harsher than the backtest environment

That last point is where "implementation reality" really starts to bite.

## Gate 6: DEMO Is Its Own Operational Filter

Even a strategy that survives research, implementation, and validation still is not "basically live."

There is another boundary after that: DEMO.

You can see the public shape of this in our open-source repos today. `tradedesk` is built so that the same strategy code can run across backtest and live paths. The portfolio lifecycle includes warmup, a `SessionReadyEvent`, and explicit pre-flight order gates before broker submission. The DEMO runbook adds another layer on top of that: build-time config packaging, startup indicators, broker-feed connectivity checks, crash-recovery expectations, and a zero-trades troubleshooting path.

That operational layer is easy to understate in research-heavy shops. It should not be.

A strategy that cannot explain:

- how it warms up
- how it handles session boundaries
- how it is prevented from trading through bad spreads or manual pause states
- how it behaves after a restart
- how operators tell the difference between "quiet market" and "broken deployment"

is not a deployment candidate. It is still research.

And this is the uncomfortable part: sometimes a strategy never earns the right to meet DEMO at all.

That was the real Phase 5 outcome.

## What Phase 5 Actually Proved

Phase 5 did not prove that new research is pointless.

It proved something more useful:

- model convergence is helpful but not sufficient
- a backtest spec is not the same thing as an implemented strategy
- review can invalidate quant assumptions for good reasons
- out-of-sample failure is information, not embarrassment
- DEMO should be treated as an operational gate, not a ceremonial stop on the way to live

The board-level consequence was straightforward: pause more archetype hunting for now and focus on hardening the systems that already earned their place.

That is less glamorous than announcing a shiny new strategy.

It is also how you avoid promoting a research artifact into an operating problem.

## The Boring Rule We Keep Re-Learning

The distance between "good backtest" and "safe deployment candidate" is where most of the real work lives.

That distance includes validation windows, portfolio fit, implementation detail, review discipline, runtime safeguards, and operator clarity. Skip any of those and the process gets faster right up until it gets expensive.

So when we say a strategy moved from research toward implementation reality, we do not mean it was inevitably headed for live trading.

We mean it entered the part of the pipeline where reality gets a vote.

That is where most candidates fail.

That is also where trust comes from.

---

## What This Post Intentionally Does Not Include

- proprietary strategy parameters
- unpublished source code from private repositories
- live operating metrics or non-public performance data

---

## License

Licensed under the Apache License, Version 2.0.
See: [https://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0)

Copyright 2026 [Radius Red Ltd.](https://github.com/radiusred) | [Contact](mailto:opensource@radiusred.uk)
