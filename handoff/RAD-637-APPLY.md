# RAD-637 Apply + Verify

## Apply Patch

```bash
git am handoff/RAD-637-future-post-date-fix.patch
```

## Push

```bash
git push origin HEAD
```

## Verify in CI

1. Open the latest workflow run for `Blog Date Visibility`.
2. Confirm job `jekyll-future-date-guard` succeeds.
3. Confirm step `Assert future-dated fixture is not rendered on public surfaces` passes.

## What the Fix Includes

- Atom feed now uses filtered `site.posts` and excludes `post.date > site.time`.
- Homepage "Latest Posts" now renders dynamically from filtered posts.
- `_config.yml` hardening: `permalink` key fix and `show_drafts: false`.
- Author workflow docs for drafts and publishing (`README.md`).
- CI guard workflow that fails if a future-dated fixture leaks into `index.html` or `atom.xml`.
