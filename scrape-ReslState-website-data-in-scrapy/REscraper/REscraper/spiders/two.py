import scrapy
import json
from ..items import RescraperItem
from scrapy import Request
# from scrapy import Request
import re
# from scrapy.crawler import CrawlerProcess
# from scrapy.selector import Selector
# from scrapy.loader import ItemLoader
# from urllib.parse import urljoin, urlencode


def cleanup(input_string):
    if input_string:
        return re.sub(r'[\\r\\n\\t@]', '', input_string).strip()

class Myspider(scrapy.Spider):
    name = "data"

    headers = {
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
    }

    def start_requests(self):
        url = 'https://www.movoto.com/san-francisco-ca/new-7/p-1/@37.77493,-122.419416/'

        yield Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        all_data = response.css(".cardone a::attr(href)").getall()
        for data in all_data:
            print(data, "***********************")
            link = response.urljoin(data)
            print(link,"'''''''''''''''''''''''''''''''''''''''''''")
            yield Request(url=link, callback=self.parse_info)




    def parse_info(self, response):

        yield {
            'Property': response.css('.propertyTypeText span::text').get(),
            'Sqft': cleanup(response.css('div~ div+ div b::text').get()),
            'Location': cleanup(response.css('.dpp-header-title .title::text').get()),
            'price': response.css('.price-title::text').get(),
            'County': response.css('.flex-sm-6:nth-child(6) a::text').get(),
            # 'Mortgage Payment': cleanup(response.css('#scrollCal::text').get()),
            'Property type': cleanup(response.css('.flex-sm-6:nth-child(4) span+ span::text').get()),
            'Neighborhood': cleanup(response.css('.flex-sm-6:nth-child(5) a::text').get()),
            'Airbnb Estimate ': cleanup(response.css('#rentalValueLink::text').get()),
            'Status ': cleanup(response.css('.col-sm-6:nth-child(3) .text-bold::text').get()),
            'Year Built ': cleanup(response.css('.col-sm-6:nth-child(6) .text-bold::text').get()),
            'Description': cleanup(response.css('.paragraph::text').get()),
            'Img_Url': response.css('.img-done::attr(src)').getall()
        }






