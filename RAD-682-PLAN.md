# RAD-682: Blog Cleanup Plan

**Status:** Ready for approval  
**Date:** 2026-04-30  
**Issue:** Remove old blog from radiusred/.github and consolidate to radiusred/blog

## Current State Analysis

### Old Deployment (radiusred/.github)
- **URL:** https://radiusred.github.io/.github/
- **Framework:** Material for MkDocs (theme: slate, primary: red, accent: red)
- **Content:** Org documentation site with redirect to /blog/ in index.html
- **Deployment:** GitHub Actions workflow (`deploy-blog.yml`) builds and deploys to GitHub Pages
- **Features:** Search, code copy buttons, instant navigation, mobile-responsive

### Current Deployment (radiusred/blog)
- **URL:** https://radiusred.github.io/blog/
- **Framework:** Jekyll with custom CSS
- **Styling:** Dark theme (#222 background, #991919 burgundy main, #ddd text, #a33 links)
- **Content:** 10 published posts as of 2026-04-30
- **Configuration:** Minimal Jekyll setup with kramdown markdown

### Styling Comparison

| Aspect | Old MkDocs | Current Jekyll |
|--------|-----------|-----------------|
| Color scheme | Dark (slate) | Dark (#222 background) |
| Primary accent | Red | Burgundy (#991919, #a33) |
| Typography | Material Design system | System fonts (-apple-system, BlinkMacSystemFont, etc.) |
| Search | Built-in search plugin | Not implemented |
| Code features | Copy button, syntax highlight | Basic syntax highlight |
| Navigation | Instant navigation, tracking | Simple internal links |

**Styling verdict:** The current Jekyll blog already has a similar dark, red-accented aesthetic. The main features from the old MkDocs site (search, code copy, instant nav) would need to be added to Jekyll if desired, but are not strictly necessary for blog functionality.

## Broken Links Audit

**Location:** Bluesky posts mentioning https://radiusred.github.io/.github/
**Status:** Old site is still live with redirect to /blog/, so links still work technically but point to wrong canonical URL.
**Action needed:** Any posts that linked directly to the old site should be audited.

## Action Plan

### Phase 1: Audit & Documentation (This PR)
- [x] Inspect radiusred/.github repo structure and styling
- [x] Document differences between old and current blogs
- [x] Identify any unique content in old deployment
- [ ] Create this plan document

### Phase 2: Disable Old Deployment (PR to radiusred/.github)
1. **Remove GitHub Actions deployment:**
   - Delete or disable `.github/workflows/deploy-blog.yml`
   - Rationale: Prevents accidental rebuilds of MkDocs site

2. **Update documentation redirect:**
   - Update `docs/index.md` to clarify that blog moved to radiusred/blog
   - Remove outdated references to `https://radiusred.github.io/.github/`
   - Keep org profile docs in place (CONTRIBUTING.md, profile/README.md)

3. **Test:**
   - Verify old site no longer auto-deploys
   - Confirm `/blog/` redirect still works for existing links

### Phase 3: Link Audit (Manual Review)
1. Review Bluesky posts for broken/outdated links (requires AT Protocol API auth)
2. Identify any posts linking to https://radiusred.github.io/.github/
3. Create social media post announcing blog consolidation if needed

### Phase 4: Cleanup (Optional, Future)
- Once old site is confirmed decommissioned and no traffic, consider removing entire MkDocs setup from .github repo
- Archive or delete `mkdocs.yml`, `docs/`, `requirements.txt`, and build artifacts

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Broken links in existing Bluesky posts | Low | Old domain still resolves to /blog/ via index.html redirect |
| Loss of old site styling/features | Low | Current blog has equivalent dark theme; missing features are nice-to-have |
| Accidental rebuild during transition | Medium | Disable workflow before testing |
| References to old URL in docs | Low | Update docs/index.md to clarify new canonical location |

## Success Criteria

- [ ] `.github/workflows/deploy-blog.yml` is disabled/removed
- [ ] `docs/index.md` updated to point to radiusred/blog as canonical blog source
- [ ] Old site at https://radiusred.github.io/.github/ no longer auto-rebuilds
- [ ] Links still work via redirect (graceful degradation)
- [ ] No broken links in active Bluesky posts

## Next Steps

1. **Get approval** for Phase 2 (disable old deployment)
2. **Create PR to radiusred/.github** implementing Phase 2 changes
3. **Manual audit** of Bluesky posts (Phase 3) - requires authentication
4. **Verify** old site no longer rebuilds after workflow removal
