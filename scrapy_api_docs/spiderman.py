import scrapy


class SpidermanSpider(scrapy.Spider):
    name = "spiderman"
    allowed_domains = ["docs.github.com"]
    start_urls = ["https://docs.github.com/en/rest?apiVersion=2022-11-28"]

    def parse(self, response):
        pass
