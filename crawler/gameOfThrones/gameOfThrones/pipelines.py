# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from gameOfThrones import dbmanager

class IntroductionPipeline(object):
    def open_spider(self, spider):
        print('open ====')
        role = dbmanager.Role()
        dbmanager.create_table(role)

    def process_item(self, item, spider):
        dbmanager.save_roles(item)
        return item

    def close_spider(self, spider):
        print('close ==== ')
