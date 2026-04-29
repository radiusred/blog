# Radius Red Blog

This repository is the canonical source for the Radius Red public blog.

Publishing endpoints:

- Blog: `https://radiusred.github.io/blog/`
- Feed: `https://radiusred.github.io/blog/atom.xml`

Repository roles:

- `radiusred/blog`: blog posts, blog assets, and Jekyll blog configuration
- `radiusred/.github`: org profile/docs site and routing that can link/redirect to the blog

When adding or updating blog articles, do it in this repository.

## Publishing Rules

- Published posts belong in `posts/` and must include a valid front matter `date`.
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
