import scrapy
from scrapy_api_docs.items import ApiEndpointItem

class EndpointSpider(scrapy.Spider):
    name = 'endpoint'
    start_urls = ['https://example.com/api/endpoint']  # Replace with actual endpoint URLs

    def parse(self, response):
        item = ApiEndpointItem()
        item['url'] = response.url
        item['method'] = response.css('span.method::text').get()
        item['params'] = response.css('div.params::text').getall()
        item['responses'] = response.css('div.responses::text').getall()

        yield item
