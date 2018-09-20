import scrapy
from ..items import FirstscrapyItem


class GanjiSpider(scrapy.Spider):
    name = 'zufang'
    start_urls = ['http://hz.ganji.com/fang1/xihu/']

    def parse(self, response):
        # print(response)
        zf = FirstscrapyItem()
        titles = response.xpath("//dl[@class='f-list-item-wrap f-clear']//dd[@class='dd-item title']/a/text()").extract()
        prices = response.xpath("//div[@class='f-list-item ershoufang-list']//span[@class='num']/text()").extract()

        for i,j in zip(titles, prices):
            zf['title'] = i
            zf['money'] = j
            yield zf
            # print("title == ", i, ", price == ", j)
