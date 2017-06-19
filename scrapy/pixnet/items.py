# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PixnetItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    author_info = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    links = scrapy.Field()
    image_num = scrapy.Field()
    links_num = scrapy.Field()
    global_cat = scrapy.Field()
    custom_cat = scrapy.Field()
