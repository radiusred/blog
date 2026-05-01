import os
import re
from datetime import datetime
from pathlib import Path

def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown file."""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter_text = match.group(1)
    body = content[match.end():]

    data = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip().strip('"\'')

    return data, body

def generate_atom_feed():
    """Generate Atom 1.0 feed from blog posts."""
    blog_dir = Path('docs/blog')
    posts = []

    # Collect all blog posts
    for post_file in sorted(blog_dir.glob('*.md'), reverse=True):
        with open(post_file, 'r') as f:
            content = f.read()

        fm, body = parse_frontmatter(content)

        # Skip posts without required fields
        if not all(k in fm for k in ['title', 'date', 'description']):
            continue

        # Skip future-dated posts
        post_date = datetime.fromisoformat(fm['date'])
        if post_date > datetime.now():
            continue

        posts.append({
            'title': fm['title'],
            'date': fm['date'],
            'description': fm['description'],
            'slug': post_file.stem,
            'filename': post_file.name
        })

    # Generate Atom feed
    now = datetime.now().isoformat() + 'Z'
    latest_date = posts[0]['date'] + 'T00:00:00Z' if posts else now

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
        entry_date = post['date'] + 'T00:00:00Z'
        feed += f"""  <entry>
    <title>{post['title']}</title>
    <link href="{post_url}" rel="alternate" />
    <id>{post_url}</id>
    <updated>{entry_date}</updated>
    <summary>{post['description']}</summary>
  </entry>
"""

    feed += "</feed>\n"

    # Write feed to docs directory so it's included in the build
    with open('docs/atom.xml', 'w') as f:
        f.write(feed)

    print(f"Generated Atom feed with {len(posts)} posts")

def main():
    generate_atom_feed()

if __name__ == "__main__":
    main()
