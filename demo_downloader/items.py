# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DemoDownloaderItem(scrapy.Item):
    # file_urls = scrapy.Item()
    # files = scrapy.Item()
    
    # name = scrapy.field()
    # comment = scrapy.field()
    
    CollegeCode = scrapy.field()
    CollegeName = scrapy.field()
    BranchCode = scrapy.field()
    BranchName = scrapy.field()
    OC = scrapy.field()
    BC = scrapy.field()
    BCM = scrapy.field()
    MBC = scrapy.field()
    SC = scrapy.field()
    SCA = scrapy.field()
    ST = scrapy.field()

    # username    =scrapy.field()
    # title       =scrapy.field()
    # pay_method  =scrapy.field()
    # time        =scrapy.field()
    # amount      =scrapy.field()