# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from gameOfThrones import dbmanager

class IntroductionPipeline(object):
    def open_spider(self, spider):
        print('open ====')
        pov = dbmanager.Pov()
        dbmanager.create_table(pov)

    def process_item(self, item, spider):
        dbmanager.save_povs(item)
        return item

    def close_spider(self, spider):
        print('close ==== ')
