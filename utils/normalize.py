from urllib.parse import urljoin, urlparse

def normalize_link(link, base_url):
    """Normalize a link to its absolute form."""
    return urljoin(base_url, link)

def is_relevant_link(link):
    """Filter out non-relevant links."""
    irrelevant_extensions = ['.css', '.js', '.png', '.jpg', '.jpeg', '.svg', '.ico']
    parsed_url = urlparse(link)
    # Exclude links with irrelevant extensions or fragments
    if any(parsed_url.path.endswith(ext) for ext in irrelevant_extensions):
        return False
    if parsed_url.fragment:  # Exclude links with fragments (e.g., #section)
        return False
    return True

def is_endpoint(link):
    """Identify API endpoints based on patterns."""
    endpoint_keywords = ['/api/', '/v1/', '/v2/', '/endpoint/', '/rest/']
    return any(keyword in link for keyword in endpoint_keywords)