# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DemoDownloaderItem(scrapy.Item):
    file_urls = scrapy.Item()
    files = scrapy.Item()
    name = scrapy.field()
    res = scrapy.field()