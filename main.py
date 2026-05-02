import re
import shutil
from datetime import date, datetime
from pathlib import Path

DOCS_BLOG = Path("docs/posts")
DRAFTS_BLOG = Path("_drafts")
CONFIG = Path("zensical.toml")
ARCHIVE_PAGE = Path("docs/archive.md")
NAV_LIMIT = 10


def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown file."""
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter_text = match.group(1)
    body = content[match.end() :]

    data = {}
    for line in frontmatter_text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip("\"'")

    return data, body


def _post_date(post_file):
    """Return the post's frontmatter date as a date, or None if missing/invalid."""
    fm, _ = parse_frontmatter(post_file.read_text())
    raw = fm.get("date")
    if not raw:
        return None
    try:
        return date.fromisoformat(raw)
    except ValueError:
        return None


def reconcile_drafts():
    """Move future-dated posts out of docs/blog/, promote due drafts back in."""
    DRAFTS_BLOG.mkdir(parents=True, exist_ok=True)
    today = date.today()

    demoted = []
    for post in DOCS_BLOG.glob("*.md"):
        d = _post_date(post)
        if d and d > today:
            shutil.move(str(post), str(DRAFTS_BLOG / post.name))
            demoted.append(post.name)

    promoted = []
    for draft in DRAFTS_BLOG.glob("*.md"):
        d = _post_date(draft)
        if d and d <= today:
            shutil.move(str(draft), str(DOCS_BLOG / draft.name))
            promoted.append(draft.name)

    if demoted:
        print(f"Hidden as drafts ({len(demoted)}): {', '.join(sorted(demoted))}")
    if promoted:
        print(f"Promoted to published ({len(promoted)}): {', '.join(sorted(promoted))}")


def _published_posts():
    """Return [(date, title, filename)] for all published posts, newest first."""
    posts = []
    for post in DOCS_BLOG.glob("*.md"):
        fm, _ = parse_frontmatter(post.read_text())
        d = _post_date(post)
        title = fm.get("title")
        if d and title:
            posts.append((d, title, post.name))
    posts.sort(key=lambda p: p[0], reverse=True)
    return posts


def regenerate_nav():
    """Rewrite the nav block in zensical.toml: top NAV_LIMIT posts plus an archive link."""
    posts = _published_posts()
    visible = posts[:NAV_LIMIT]

    new_block = ['nav = [', '  { "Radius Red Blog" = "index.md" },']
    for _, title, fname in visible:
        safe_title = title.replace('"', '\\"')
        new_block.append(f'  {{ "{safe_title}" = "posts/{fname}" }},')
    new_block.append('  { "All posts..." = "archive.md" },')
    new_block.append("]")

    text = CONFIG.read_text()
    lines = text.split("\n")
    start = end = None
    for i, line in enumerate(lines):
        if start is None and line.lstrip().startswith("nav = ["):
            start = i
        elif start is not None and line.strip() == "]":
            end = i
            break
    if start is None or end is None:
        raise RuntimeError("Could not find nav = [...] block in zensical.toml")

    lines[start : end + 1] = new_block
    new_text = "\n".join(lines)
    if new_text != text:
        CONFIG.write_text(new_text)
        print(f"Updated nav with {len(visible)} visible posts + archive link")


def generate_archive():
    """Write docs/archive.md grouping all published posts by year and month, newest first."""
    posts = _published_posts()
    lines = [
        "---",
        "title: All Posts",
        "description: A complete index of every Radius Red blog post.",
        "---",
        "",
        "# All Posts",
        "",
    ]
    last_year = last_month = None
    for d, title, fname in posts:
        if d.year != last_year:
            if last_year is not None:
                lines.append("")
            lines += [f"## {d.year}", ""]
            last_year, last_month = d.year, None
        if d.month != last_month:
            if last_month is not None:
                lines.append("")
            lines += [f"### {d.strftime('%B')}", ""]
            last_month = d.month
        slug = fname.removesuffix(".md")
        lines.append(f"- **{d.isoformat()}** — [{title}](posts/{slug}.md)")
    lines.append("")

    ARCHIVE_PAGE.write_text("\n".join(lines))
    print(f"Generated archive page with {len(posts)} posts.")


def generate_atom_feed():
    """Generate Atom 1.0 feed from blog posts."""
    posts = []

    for post_file in sorted(DOCS_BLOG.glob("*.md"), reverse=True):
        with open(post_file, "r") as f:
            content = f.read()

        fm, body = parse_frontmatter(content)

        if not all(k in fm for k in ["title", "date", "description"]):
            continue

        post_date = datetime.fromisoformat(fm["date"])
        if post_date > datetime.now():
            continue

        posts.append(
            {
                "title": fm["title"],
                "date": fm["date"],
                "description": fm["description"],
                "slug": post_file.stem,
                "filename": post_file.name,
            }
        )

    now = datetime.now().isoformat() + "Z"
    latest_date = posts[0]["date"] + "T00:00:00Z" if posts else now

    feed = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Radius Red Blog</title>
  <subtitle>Engineering notes, release updates, and insights from the Radius Red team.</subtitle>
  <link href="https://radiusred.github.io/blog/atom.xml" rel="self" />
  <link href="https://radiusred.github.io/blog/" rel="alternate" />
  <id>https://radiusred.github.io/blog/</id>
  <updated>{latest_date}</updated>
  <author>
    <name>Radius Red Ltd.</name>
  </author>
"""

    for post in posts:
        post_url = f"https://radiusred.github.io/blog/{post['slug']}/"
        entry_date = post["date"] + "T00:00:00Z"
        feed += f"""  <entry>
    <title>{post['title']}</title>
    <link href="{post_url}" rel="alternate" />
    <id>{post_url}</id>
    <updated>{entry_date}</updated>
    <summary>{post['description']}</summary>
  </entry>
"""

    feed += "</feed>\n"

    with open("docs/atom.xml", "w") as f:
        f.write(feed)

    print(f"Generated Atom feed with {len(posts)} posts")


def main():
    reconcile_drafts()
    regenerate_nav()
    generate_archive()
    generate_atom_feed()


if __name__ == "__main__":
    main()
