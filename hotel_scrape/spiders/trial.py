import scrapy


class TrialSpider(scrapy.Spider):
    name = 'trial'
    allowed_domains = ['scrapeme.live']
    start_urls = ['http://scrapeme.live/']

    def parse(self, response):
        pass
