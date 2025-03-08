import requests
import requests.adapters
from config import LOGGING_CONFIG, CACHE_ENABLED, CACHE_DIR, CONNECTION_POOL_SIZE, REQUEST_TIMEOUT, REQUEST_DELAY
import logging
import os
import time

# Set up logging
logging.basicConfig(**LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Enable caching if configured
if CACHE_ENABLED:
    os.makedirs(CACHE_DIR, exist_ok=True)
    from requests_cache import CachedSession
    session = CachedSession(cache_name=os.path.join(CACHE_DIR, 'api_cache'), expire_after=3600)  # Cache for 1 hour
else:
    session = requests.Session()

# Increase connection pool size
adapter = requests.adapters.HTTPAdapter(pool_connections=CONNECTION_POOL_SIZE, pool_maxsize=CONNECTION_POOL_SIZE)
session.mount('http://', adapter)
session.mount('https://', adapter)

def fetch_url(url):
    """Fetch HTML content from a URL."""
    time.sleep(REQUEST_DELAY)  # Add a delay between requests
    try:
        response = session.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        return None