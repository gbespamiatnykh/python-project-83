from urllib.parse import urlparse

import validators
from bs4 import BeautifulSoup


def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def validate(url):
    errors = []
    if not validators.url(url):
        errors.append("Invalid URL")
    elif len(url) > 255:
        errors.append("URL too long")
    return errors


def parse_html(html):
    parsed_html = BeautifulSoup(html, "html.parser")
    heading = parsed_html.h1.string if parsed_html.h1 else None
    title = parsed_html.title.string if parsed_html.title else None
    description = parsed_html.find("meta", {"name": "description"})
    description_content = description.get("content") if description else None
    return {"h1": heading, "title": title, "description": description_content}
