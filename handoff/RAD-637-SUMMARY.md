# RAD-637 Summary

## Problem

Future-dated blog entries were appearing in public surfaces.

## Local Fix Status

Implemented and committed locally.

### Commits

1. `79ec946` - `fix(blog): prevent future-dated posts from public surfaces`
2. `797a9df` - `docs(handoff): add apply and CI verification steps for RAD-637`

### Files Changed

- `.github/workflows/blog-date-visibility.yml`
- `_config.yml`
- `atom.xml`
- `index.md`
- `README.md`
- `_drafts/.gitkeep`
- `handoff/RAD-637-APPLY.md`

## Maintainer Actions

```bash
git cherry-pick 79ec946 797a9df
git push origin HEAD
```

Then verify GitHub Actions workflow `Blog Date Visibility`:
- Job: `jekyll-future-date-guard`
- Must pass step: `Assert future-dated fixture is not rendered on public surfaces`

## Why Push Is Blocked Here

- Current git identity receives HTTP 403 on push to `radiusred/blog`.
- GitHub App secret env required by `gh-cli` skill is incomplete in this runtime.
