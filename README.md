# Radius Red Public Site

This repository is the canonical source for the Radius Red public web site, tech docs and blog.

When adding or updating blog articles, do it in this repository.

## Front Matter

Every post requires valid front matter at the top of the file:

```yaml
---
layout: default
author: Your Name
title: Post title goes here
date: YYYY-MM-DD
description: One-sentence summary, used in feed and listings
tags: [tag1, tag2, tag3]
---
```

- `layout`: Required. Set to `default` for all posts.
- `author`: Required. Author name displayed in the post byline.
- `title`: Required. Displayed as the post heading and in listings.
- `date`: Required. Sets publication order and controls visibility (see Build Visibility Controls below).
- `description`: Required. Used in feed summaries and on the blog homepage.
- `tags`: Optional. Comma-separated list of topic tags.

## Post Content

Posts should contain article content without:

- **No post title.** The template renders the title from front matter `title` field.
- **No byline or date.** The template renders publication metadata from front matter.
- **No license footer.** The template appends the Apache 2.0 license footer automatically.

Start your content with the first paragraph or section heading (`##` level 2 or deeper).

Example structure:

```markdown
---
layout: default
author: Wordy
title: Why we chose Dukascopy for market data
date: 2026-04-30
description: Technical decision on data provider selection for tradedesk.
tags: [tradedesk, data, architecture]
---

## The Challenge

Systematic trading requires high-fidelity market data...

## Why Dukascopy

We evaluated three providers...
```

## Publishing Rules

- Create posts in `docs/blog/posts/` and must include a valid front matter `date`.
- The site build will handle future dated posts and ensure they do not appear until the publish date.

## Local Preview

- `uv sync && uv run zensical serve` should create a local site on localhost:8000
