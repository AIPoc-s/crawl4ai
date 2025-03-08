import re


def extract_api_urls(response):
    """Extract potential API documentation URLs from a page."""
    urls = response.css('a::attr(href)').getall()
    api_urls = []

    for url in urls:
        # Filter URLs that look like API documentation (customize regex as needed)
        if re.match(r'/[a-zA-Z0-9_-]+$', url):  # Simplified; adjust regex for your docs pattern
            api_urls.append(url)

    return api_urls