import scrapy
from scrapy_api_docs.items import ApiDocItem


class ApiDocsSpider(scrapy.Spider):
    name = 'api_docs'
    start_urls = ["https://docs.github.com/en/rest?apiVersion=2022-11-28"]  # Replace with the actual documentation URL

    def parse(self, response):
        # Extract links to API documentation endpoints
        api_links = response.css('a.api-endpoint::attr(href)').getall()

        for link in api_links:
            yield response.follow(link, self.parse_endpoint)

    def parse_endpoint(self, response):
        item = ApiDocItem()
        item['url'] = response.url
        item['title'] = response.css('h1::text').get()
        item['description'] = response.css('div.description::text').get()

        # Find the endpoints on this page
        endpoint_links = response.css('a.endpoint-link::attr(href)').getall()

        for endpoint in endpoint_links:
            yield response.follow(endpoint, self.parse_endpoint_details)

        yield item

    def parse_endpoint_details(self, response):
        # This is a recursive function that scrapes the individual endpoint details
        endpoint_item = ApiDocItem()
        endpoint_item['url'] = response.url
        endpoint_item['method'] = response.css('span.method::text').get()
        endpoint_item['params'] = response.css('div.params::text').getall()
        endpoint_item['responses'] = response.css('div.responses::text').getall()

        yield endpoint_item
