#!/usr/bin/env python3
"""
Pull all published pages from the WP REST API and convert to Hugo Markdown.
Usage: python3 scripts/wp_to_hugo.py
"""
import json
import os
import re
import urllib.request
from markdownify import markdownify

BASE_URL = "http://www.fsyo.org.uk/wp-json/wp/v2"
CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "content")

# Pages that get their own section directory (so Hugo treats them as branch bundles)
SECTION_PAGES = {"home", "about", "concerts-and-events"}

# Slug remapping: WP slug → Hugo path
SLUG_MAP = {
    "home": "_index",
    "concerts-events-archive": "concerts-events-archive",
}

# WP media base URL prefix to rewrite to /images/
WP_UPLOAD_PREFIX = "http://www.fsyo.org.uk/wp-content/uploads/"


def fetch_pages():
    url = f"{BASE_URL}/pages?per_page=50&status=publish&_fields=slug,title,content,parent"
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read())


WP_SITE_URL = "http://www.fsyo.org.uk"

HTML_ENTITIES = {
    "&#038;": "&",
    "&#8211;": "–",
    "&#8212;": "—",
    "&#8216;": "'",
    "&#8217;": "'",
    "&#8220;": "“",
    "&#8221;": "”",
    "&amp;": "&",
    "&nbsp;": " ",
}


def decode_entities(text: str) -> str:
    for entity, char in HTML_ENTITIES.items():
        text = text.replace(entity, char)
    return text


def rewrite_urls(md: str) -> str:
    # Rewrite absolute WP image URLs to relative /images/ paths
    md = md.replace(WP_UPLOAD_PREFIX, "/images/")
    # Rewrite absolute internal links to relative paths
    md = md.replace(f"]({WP_SITE_URL}/", "](/")
    # Also handle links that include www vs non-www
    md = md.replace("](http://fsyo.org.uk/", "](/")
    return md


def clean_markdown(md: str) -> str:
    # Collapse 3+ blank lines to 2
    md = re.sub(r"\n{3,}", "\n\n", md)
    # Remove WP caption shortcodes that slipped through
    md = re.sub(r"\[/?caption[^\]]*\]", "", md)
    return md.strip()


def convert_page(page: dict) -> tuple[str, str]:
    """Returns (output_path, markdown_content)."""
    slug = page["slug"]
    title = page["title"]["rendered"]
    raw_html = page["content"]["rendered"]

    md = markdownify(raw_html, heading_style="ATX", strip=["script", "style"])
    md = rewrite_urls(md)
    md = clean_markdown(md)

    title = decode_entities(title)
    front_matter = f'---\ntitle: "{title}"\n---\n\n'
    content = front_matter + md

    # Determine output file path
    if slug == "home":
        path = os.path.join(CONTENT_DIR, "_index.md")
    elif slug in SECTION_PAGES:
        os.makedirs(os.path.join(CONTENT_DIR, slug), exist_ok=True)
        path = os.path.join(CONTENT_DIR, slug, "_index.md")
    else:
        hugo_slug = SLUG_MAP.get(slug, slug)
        path = os.path.join(CONTENT_DIR, f"{hugo_slug}.md")

    return path, content


def main():
    os.makedirs(CONTENT_DIR, exist_ok=True)
    pages = fetch_pages()
    print(f"Fetched {len(pages)} pages")
    for page in pages:
        path, content = convert_page(page)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  wrote {os.path.relpath(path)}")


if __name__ == "__main__":
    main()
