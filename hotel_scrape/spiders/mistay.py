import scrapy
import io
import json
from ..items import HotelScrapeItem

def get_details(details):
    product_type, latitude, longitude, hotel_url, email, phone, rating, review = '', '', '', '', '', '', '', ''
    details_dict = json.loads(details.strip())
    product_type = details_dict.get('@type', '')
    latitude = details_dict.get('geo', {}).get('latitude', '')
    longitude = details_dict.get('geo', {}).get('longitude', '')
    hotel_url = details_dict.get('url', '')
    email = details_dict.get('email', '')
    phone = details_dict.get('telephone', '')
    rating = details_dict.get('aggregateRating', {}).get('ratingValue', '')
    review = details_dict.get('aggregateRating', {}).get('reviewCount', '')
    return product_type, latitude, longitude, hotel_url, email, phone, rating, review

class MistaySpider(scrapy.Spider):
    name = 'mistay'
    # allowed_domains = ['mistay.in']
    # start_urls = ['http://mistay.in/']

    def start_requests(self):
        city_url = 'https://www.mistay.in/hotels-in-bangalore/?checkin_date=2021-05-14&checkin_slot=2&slot_count=3&guest_count=1&room_count=1#overlay_temp=0.9450360132160038'
        print('in start_requests')
        yield scrapy.Request(url=city_url, callback=self.parse_hotel_list)
    
    def parse_hotel_list(self, response):
        # details = response.text
        # print(details)
        # print('in parse_hotel_list')
        site_url = 'https://www.mistay.in'
        # hotel_url_list = response.xpath('//div[@class="hotel-list-item"]/div[@class="content"]/div[@class="left"]/div/a/@href').extract()
        hotel_url_list = response.xpath('//div[@class="hotels-list-mobile"]/a[@class="hotel-item"]/@href').extract()
        # print(hotel_url_list)
        for url in hotel_url_list:
            yield scrapy.Request(url=site_url + url, callback=self.parse_hotel)

        # QA Test
        # url = 'https://www.mistay.in/hotels-in-bangalore/ramada-encore/?checkin_date=2021-05-14&checkin_slot=2&slot_count=3&room_count=1&guest_count=1'
        # yield scrapy.Request(url=url, callback=self.parse_hotel)

    def parse_hotel(self, response):
        # print('in parse_hotel')
        # details = response.text
        # file1 = io.open('mistay_hotel.txt', 'w', encoding="utf-8")
        # file1.write(details)
        # file1.close()
        name = ''.join(response.xpath('//div[@class="cm-padded-10 cm-distinct-10 cm-title1"]/text()').extract())
        address = ''.join(response.xpath('//div[@class="cm-padded-10 cm-caption"]/text()').extract())
        hotel_amenities = ', '.join(response.xpath('//div[@class="cm-row vertical-scrollable"]/div[@class="amenities"]/div/text()').extract())
        hotel_room = ', '.join(response.xpath('//div[@class="cm-row relative amenities-list room-amenities-list"]/div[@class="cm-row vertical-scrollable"]/div[@class="amenities"]/div/text()').extract())
        price = ''.join(response.xpath('//div[@class="view-pricing"]/span[@class="total-price-payable"]/text()').extract())
        details = ''.join(response.xpath('//script[contains(text(), "PostalAddress")]/text()').extract())
        tags = ''.join(response.xpath('//div[@class="ui teal label"]/text()').extract())
        product_type, latitude, longitude, hotel_url, email, phone, rating, review = get_details(details)

        items = {
            'Name': name.strip(),
            'Address': address.strip(),
            'ProductType': product_type.strip(),
            'Latitude': str(latitude),
            'Longitude': str(longitude),
            'Email': email.strip(),
            'Phone': phone.strip(),
            'Url': hotel_url.strip(),
            'HotelAmenities': hotel_amenities.strip(),
            'RoomAmenities': hotel_room.strip(),
            'Price': str(price) if price else 'Sold Out',
            'Rating': rating.strip(),
            'Reviews': review.strip(),
            'Tags': tags.strip()
        }

        yield HotelScrapeItem(**items)

        
