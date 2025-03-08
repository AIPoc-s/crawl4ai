import asyncio
import json
import re
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

# Define relevant API documentation categories
RELEVANT_CATEGORIES = ["organization", "repository", "pull-requests", "branches", "commits", "comments"]

# Read URLs from 'links1.json' file
with open('links1.json', 'r') as file:
    all_urls = json.load(file)

# Filter URLs based on relevant categories
filtered_urls = [url_data.get('link', '') for url_data in all_urls if
                 any(category in url_data.get('link', '') for category in RELEVANT_CATEGORIES)]

# Compile regex for efficiency
CURL_REGEX = re.compile(r'```(?:curl|bash|sh)?\n([\s\S]*?)```', re.IGNORECASE)
SCHEMA_REGEX = re.compile(r'```(?:json|response schema)?\n([\s\S]*?)```', re.IGNORECASE)
INLINE_JSON_REGEX = re.compile(r'({[\s\S]*?})', re.MULTILINE)


# Function to extract cURL commands and response schemas
def extract_endpoint_info(markdown_text):
    endpoint_info = {"curl_commands": [], "response_schema": []}

    # Extract cURL commands
    curl_matches = CURL_REGEX.findall(markdown_text)
    endpoint_info["curl_commands"] = [cmd.strip() for cmd in curl_matches if "curl" in cmd.lower()]

    # Extract response schemas
    schema_matches = SCHEMA_REGEX.findall(markdown_text) + INLINE_JSON_REGEX.findall(markdown_text)
    for schema in schema_matches:
        try:
            endpoint_info["response_schema"].append(json.loads(schema.strip()))
        except json.JSONDecodeError:
            endpoint_info["response_schema"].append(schema.strip())

    return endpoint_info


async def crawl_and_process():
    run_conf = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, stream=True)
    all_endpoint_data = []

    async with AsyncWebCrawler() as crawler:
        results =await crawler.arun_many(filtered_urls, config=run_conf)  # ✅ Async generator

        async for result in results:  # ✅ Correct async iteration
            url = filtered_urls[len(all_endpoint_data)]  # Get corresponding URL

            if result.success:
                endpoint_info = extract_endpoint_info(result.markdown_v2.raw_markdown)

                url_info = {
                    "url": url,
                    "methods": {}
                }

                for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']:
                    if re.search(rf'\b{method}\b', result.markdown_v2.raw_markdown, re.IGNORECASE):
                        url_info["methods"][method] = {
                            "auth_type": "OAuth",
                            "curl_commands": endpoint_info['curl_commands'],
                            "response_schema": endpoint_info['response_schema']
                        }

                all_endpoint_data.append(url_info)
            else:
                all_endpoint_data.append({"url": url, "error": result.error_message})

    # Save results
    with open("api_endpoints.json", "w") as json_file:
        json.dump(all_endpoint_data, json_file, indent=4)

    print("\nFinished saving documentation to api_endpoints.json.")


if __name__ == "__main__":
    asyncio.run(crawl_and_process())
