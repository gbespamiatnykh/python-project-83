from urllib.parse import urlparse

import validators


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
