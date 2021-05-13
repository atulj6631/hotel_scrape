import scrapy


class IndiaMartSpider(scrapy.Spider):
    name = 'india_mart'
    allowed_domains = ['dir.indiamart.com']
    start_urls = ['http://dir.indiamart.com/']

    def parse(self, response):
        pass
