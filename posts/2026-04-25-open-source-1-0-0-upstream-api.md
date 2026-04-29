---
title: What an open-source 1.0.0 looks like when an upstream API moves
date: 2026-04-25
description: Why tradedesk 1.0.0 shipped now, what changed in IG streaming support, and how a release workflow bug became part of the work.
tags: [tradedesk, releases, api, github-actions]
---

# What an open-source 1.0.0 looks like when an upstream API moves

Version numbers often get written about as if they are purely symbolic.

They are not.

Sometimes a `1.0.0` lands because a project feels emotionally mature. Sometimes it lands because a public API contract just became real enough that hand-waving is no longer acceptable. Our `tradedesk 1.0.0` release was much closer to the second category.

The immediate trigger was not branding. It was a broker deadline.

IG is retiring its legacy `MARKET` streaming subscription on **May 1, 2026**, which meant our open-source streaming layer had to stop treating that contract as a stable foundation. In practice, that meant moving `tradedesk` over to the newer `PRICE` subscription model before the cutoff and making the change visible in code, examples, and release automation while there was still time for users to adapt.

That sort of change sounds small when reduced to a changelog line. It was not dramatic, but it was real.

The contract changed in a few important ways. Stream item names are no longer just `MARKET:{epic}`. They now require account context and follow `PRICE:{account_id}:{epic}`. The top-of-book fields we consume also changed names, and the Lightstreamer subscription needs the correct `Pricing` data adapter. If you are maintaining code against the old contract, this is exactly the kind of break that can sit quietly until a date-based upstream shutdown turns it into an outage.

So the first job of `tradedesk 1.0.0` was simple: make the contract explicit.

We updated the streaming code to consume the new `PRICE` item naming and field set. We updated the public `BaseStrategy` example as part of the same cluster so the documentation would not lag the code by a release. That part matters more than it sounds. A surprising amount of integration pain comes from projects that technically shipped a change but left the public examples behind, forcing users to discover the new contract by reading implementation code or failing tests.

We did not want that.

The second job was to let QA do its job in public.

On the first pass, QA did what a good review gate should do: it caught a tiny follow-up problem that was not central to the migration, but still belonged in the release story. In this case it was a single `ruff E501` line-length regression. That is not a glamorous defect. It is also exactly the kind of thing teams are tempted to wave through when the "important" work already feels done.

We fixed it immediately and reran the review path.

That detail is worth mentioning because release discipline is usually visible in the small things before it is visible in the big ones. If a project is casual about the small correctness and hygiene checks when a deadline is looming, it usually becomes casual about larger ones too.

From there, the release grew into something more useful than a broker-compatibility patch.

Before cutting `1.0.0`, we did a pre-release quality sweep across the `tradedesk` codebase and fixed a few issues that were worth cleaning up precisely because the release boundary was becoming more important. One path used `assert isinstance()`, which is fine until Python optimization removes asserts entirely. One event type was using a bare dataclass instead of the project's `@event` convention, which is the kind of inconsistency that keeps small API surfaces from feeling truly stable. A misplaced test file was also moved so the test layout matched the source layout more cleanly.

None of those changes are dramatic by themselves.

Together, they are the kind of work that makes a `.0` release more defensible.

Then the release pipeline itself became part of the story.

When we tried to run the shared release workflow, it failed for a reason that had nothing to do with the package code. Our public repositories were pointing at a reusable GitHub Actions workflow stored in a private repository. GitHub does not allow public repositories to consume private reusable workflows that way, so the failure was structural, not accidental.

That bug had stayed hidden because several recent releases had been cut manually rather than through the broken shared workflow path. In other words: the pipeline problem was real for a while, but the system had not been forced to prove it recently enough for anyone to notice.

This is exactly why release work is useful editorial material.

It rarely tells a story only about the code you meant to ship. It also tells a story about the assumptions baked into your tooling. In our case, fixing the `tradedesk` release meant moving the shared reusable workflow and version-calculation action back into public `radiusred/.github`, updating the public repos that consumed it, and removing the redundant private copy.

That is not side-quest work. That is release work.

By the end of the cycle, `tradedesk 1.0.0` meant four things at once:

1. The IG `PRICE` subscription migration was complete before the upstream cutoff.
2. The public examples reflected the new constructor contract.
3. The package got a last pre-`1.0.0` cleanup pass instead of a ceremonial version bump.
4. The release automation ended up in the right public place for public repositories to rely on it.

That is a much better reason to cut `1.0.0` than sentiment.

For users, the practical takeaway is straightforward: if your code still assumes the old `MARKET` streaming contract, you should treat this as a real upgrade, not a decorative version change. The new subscription shape requires account-aware item names, uses the updated field names, and depends on the right adapter configuration. That is exactly the sort of boundary where explicit examples and fast release notes are more valuable than long marketing copy.

For us, the more general lesson is that open-source maturity is often visible in how a project reacts to external pressure.

An upstream API moved.

We had to adapt the package contract.

QA caught a small mistake on the way through.

The release process revealed a workflow-topology bug.

We fixed that too and shipped the release.

That is not a grand launch narrative, but it is an honest one. And for engineering tools, honest release stories are usually the most useful kind.

`tradedesk 1.0.0` is now on PyPI.

Sometimes `1.0.0` means "we're finished."

More often, it means "the interfaces matter enough now that we are willing to tighten every bolt in public."

---

## License

Licensed under the Apache License, Version 2.0.
See: https://www.apache.org/licenses/LICENSE-2.0

Copyright 2026 [Radius Red Ltd.](https://github.com/radiusred) | [Contact](mailto:opensource@radiusred.uk)

*Radius Red Ltd.*
