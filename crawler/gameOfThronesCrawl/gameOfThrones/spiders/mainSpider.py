import scrapy
from ..items import *


class NameSpider(scrapy.Spider):
    name = 'main_spider'
    start_urls = ['http://zh.asoiaf.wikia.com/wiki/Portal:%E4%BA%BA%E7%89%A9']

    def parse_introduction(self, response):
        introduction_item = IntroductionItem()
        introduction_item['level'] = 1
        introduction_item['name'] = response.xpath('//h1[@class="page-header__title"]/text()').extract()
        introduction_item['avator'] = response.xpath('//img[@class="pi-image-thumbnail"]/@src').extract()
        introduction_item['main_info'] = response.xpath('//div[@id="mw-content-text"]/p[1]//text()').extract()

        tree = response.xpath('//table[@class="familyTree"]//a/text()').extract()
        print('tree ==== ' + str(tree))
        
        yield introduction_item

    def parse(self, response):
        prefix_url = 'http://zh.asoiaf.wikia.com'
        hrefs = response.xpath('//tr/td[text()="主要POV"]/../td[2]/a/@href').extract()
        print(hrefs)

        for href in hrefs:
            introduction_url = prefix_url + href
            yield scrapy.Request(introduction_url, callback=self.parse_introduction)


