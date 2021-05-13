# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelScrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Name = scrapy.Field()
    Address= scrapy.Field()
    ProductType= scrapy.Field()
    Latitude = scrapy.Field()
    Longitude = scrapy.Field()
    Email = scrapy.Field()
    Phone = scrapy.Field()
    Url = scrapy.Field()
    HotelAmenities = scrapy.Field()
    RoomAmenities = scrapy.Field()
    Price = scrapy.Field()
    Rating = scrapy.Field()
    Reviews = scrapy.Field()
    Tags = scrapy.Field()
