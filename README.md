# Radius Red Blog

This repository is the canonical source for the Radius Red public blog.

Publishing endpoints:

- Blog: `https://radiusred.github.io/blog/`
- Feed: `https://radiusred.github.io/blog/atom.xml`

Repository roles:

- `radiusred/blog`: blog posts, blog assets, and Jekyll blog configuration
- `radiusred/.github`: org profile/docs site and routing that can link/redirect to the blog

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

- Published posts belong in `_posts/` and must include a valid front matter `date`.
- Do not use a future `date` as a draft mechanism.
- For unpublished work, use `_drafts/` with undated filenames (for example `my-post.md`).
- Alternative holdback: set `published: false` in front matter until ready.

## Build Visibility Controls

- `_config.yml` sets `future: false` so future-dated content is excluded.
- `_config.yml` sets `show_drafts: false` so drafts are excluded by default.
- Homepage and Atom feed both filter posts to `post.date <= site.time`.

## Local Preview

- Normal preview (published content only): `jekyll serve`
- Include drafts while editing: `jekyll serve --drafts`
- Include future-dated posts for testing only: `jekyll serve --future`
