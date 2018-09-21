# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IntroductionItem(scrapy.Item):
    level = scrapy.Field()
    name = scrapy.Field()
    avator = scrapy.Field()
    main_info = scrapy.Field()
