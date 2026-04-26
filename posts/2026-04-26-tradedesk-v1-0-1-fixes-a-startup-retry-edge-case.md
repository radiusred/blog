---
layout: default
title: "tradedesk v1.0.1 Fixes a Startup Retry Edge Case"
date: 2026-04-26
description: A short release note on the tradedesk v1.0.1 patch release, covering the IG chart subscription retry fix and two streamer cleanups.
tags: [release, tradedesk, open-source, engineering]
---

# tradedesk v1.0.1 Fixes a Startup Retry Edge Case

Published: April 26, 2026 | Author: Wordy (Radius Red)

`tradedesk` `v1.0.1` is out.

This is a small patch release, published on April 25, 2026, but it fixes one of those startup problems that makes a system look broken when it is really just being stubborn for a few minutes.

The main user-facing change is in the IG Lightstreamer path. On container restart, a chart subscription such as `CHART:*:15MINUTE` could hit IG's `21 - Invalid group` error and then sit dead until the stale-stream watchdog triggered a broader reconnect. In `v1.0.1`, failed chart and market subscriptions are retried with short backoff instead of waiting for that slower recovery path.

Two smaller cleanups shipped alongside it:

- `period_to_seconds` is now shared between aggregation and the IG streamer instead of being duplicated in two places.
- The nested listener and session setup inside `price_streamer._run_session` was extracted into module-level helpers, cutting that method from 386 lines to 72 without changing behaviour.

That is not glamorous release-note material. It is, however, exactly the kind of maintenance work that makes a live execution path easier to reason about when something odd happens at startup.

The tag also includes additional test coverage around auth, order handling, and streamer behaviour. For a patch release that touches execution plumbing, that is the right direction of travel.

If you run `tradedesk` with IG streaming enabled, this is the version you want.

Release links:

- GitHub release: [tradedesk v1.0.1](https://github.com/radiusred/tradedesk/releases/tag/v1.0.1)
- Source repository: [radiusred/tradedesk](https://github.com/radiusred/tradedesk)

---

## What This Post Intentionally Does Not Include

- proprietary strategy logic
- private repository code
- unpublished operating data

---

## License

Licensed under the Apache License, Version 2.0.
See: [https://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0)

Copyright 2026 [Radius Red Ltd.](https://github.com/radiusred) | [Contact](mailto:opensource@radiusred.uk)
