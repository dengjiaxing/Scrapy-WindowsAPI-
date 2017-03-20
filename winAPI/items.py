# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WinapiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    APIName=scrapy.Field()
    documentation=scrapy.Field()
    example_url=scrapy.Field()
    example=scrapy.Field()
