import scrapy

class ApiDocItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()

class ApiEndpointItem(scrapy.Item):
    url = scrapy.Field()
    method = scrapy.Field()
    params = scrapy.Field()
    responses = scrapy.Field()
