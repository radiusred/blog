# RAD-637 Blocked State

## Current State

All code and documentation changes for RAD-637 are complete locally.

## Blocker

Push to `origin` is blocked with:

`remote: Permission to radiusred/blog.git denied to radiusred-testy[bot]` (HTTP 403)

## Unblock Owner / Action

1. Owner: Board/Repo admin
2. Action:
   - Grant `radiusred-testy[bot]` write access to `radiusred/blog`, or
   - Push the local commit chain / apply the provided handoff bundle.
3. Verify:
   - Run GitHub Actions workflow `Blog Date Visibility`
   - Confirm job `jekyll-future-date-guard` passes.
