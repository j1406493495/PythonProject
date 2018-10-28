import scrapy
import re
from ..items import *


class NameSpider(scrapy.Spider):
    name = 'main_spider'
    start_urls = ['http://zh.asoiaf.wikia.com/wiki/Portal:%E4%BA%BA%E7%89%A9']
    detail_div_xpath = '//div[@id="mw-content-text"]'

    def parse(self, response):
        prefix_url = 'http://zh.asoiaf.wikia.com'

        level_one_pov_hrefs = response.xpath('//tr/td[text()="主要POV"]/../td[2]/a/@href').extract()
        level_two_pov_hrefs = response.xpath('//tr/td[text()="次要POV"]/../td[2]/a/@href').extract()
        classify_grage = response.xpath('//tr').extract()
        classify_region = response.xpath('//tr').extract()
        classify_organization = response.xpath('//tr').extract()
        classify_family = response.xpath('//tr').extract()

        for href in level_one_pov_hrefs:
            introduction_url = prefix_url + href
            yield scrapy.Request(introduction_url, meta={'level':1}, callback=self.parse_pov)

        for href in level_two_pov_hrefs:
            introduction_url = prefix_url + href
            yield scrapy.Request(introduction_url, meta={'level':2}, callback=self.parse_pov)

    #解析人物简要信息
    def parse_pov(self, response):
        introduction_item = IntroductionItem()
        introduction_item['level'] = response.meta['level']
        introduction_item['name'] = response.xpath('//h1[@class="page-header__title"]/text()').extract()
        introduction_item['avator'] = response.xpath('//img[@class="pi-image-thumbnail"]/@src').extract()

        self.parse_detail(response, introduction_item)

        yield introduction_item

    #解析人物详细信息页
    def parse_detail(self, response, introduction_item):
        detail_title = response.xpath(self.detail_div_xpath + '/h2//text()').extract()

        for index, title in enumerate(detail_title):
            if index == 0:
                introduction_item['main_info'] = response.xpath(self.detail_div_xpath + '/h2[1]/preceding-sibling::p//text()').extract()

            if '外貌' in title:
                appearance = self.get_detail_info(response, index + 1)
                introduction_item['appearance'] = appearance
            elif '历史' in title:
                history = self.get_detail_info(response, index + 1)
                introduction_item['history'] = history
            elif '近期事件' in title:
                event_book = self.get_event_book(response, index + 1)
                introduction_item['event_book'] = event_book

                event_detail = self.get_event_detail(response, index + 1)
                introduction_item['event_detail'] = event_detail

    #A节点后数据，A+1节点前数据的交叉部分
    def get_detail_info(self, response, index):
        detail_after = response.xpath(
            self.detail_div_xpath + '/h2[' + str(index) + ']/following-sibling::p//text()').extract()
        detail_before = response.xpath(
            self.detail_div_xpath + '/h2[' + str(index + 1) + ']/preceding-sibling::p//text()').extract()

        detail_after = ''.join(detail_after)
        detail_after = detail_after.split('\n')

        detail_before = ''.join(detail_before)
        detail_before = detail_before.split('\n')

        detail = [after for after in detail_after if after in detail_before]
        return detail

    #近期事件书籍title
    def get_event_book(self, response, index):
        book_after = response.xpath(
            self.detail_div_xpath + '/h2[' + str(index) + ']/following-sibling::h3//text()').extract()
        book_before = response.xpath(
            self.detail_div_xpath + '/h2[' + str(index + 1) + ']/preceding-sibling::h3//text()').extract()

        book = [after for after in book_after if after in book_before]
        return book

    #近期事件书籍详情
    def get_event_detail(self, response, index):
        book_title = response.xpath(self.detail_div_xpath + '/h3//text()').extract()
        print('book_title === ' + str(book_title))
        book_count = len(book_title)
        book_detail = []

        for book_index, book in enumerate(book_title):
            if book in ['权力的游戏', '列王的纷争', '冰雨的风暴', '群鸦的盛宴', '魔龙的狂舞', '凛冬的寒风']:
                    book_detail.append(self.get_book_detail_info(response, book_count, book_index + 1, index))

        return book_detail

    #B节点后数据，B+1节点前书籍详情数据的交叉部分
    def get_book_detail_info(self, response, book_count, book_index, index):
        book_detail_after = response.xpath(
            self.detail_div_xpath + '/h3[' + str(book_index) + ']/following-sibling::p//text()').extract()

        if book_index < book_count:
            book_detail_before = response.xpath(
                self.detail_div_xpath + '/h3[' + str(book_index + 1) + ']/preceding-sibling::p//text()').extract()
        else:
            book_detail_before = response.xpath(
                self.detail_div_xpath + '/h2[' + str(index + 1) + ']/preceding-sibling::p//text()').extract()

        book_detail_after = ''.join(book_detail_after)
        book_detail_after = book_detail_after.split('\n')

        book_detail_before = ''.join(book_detail_before)
        book_detail_before = book_detail_before.split('\n')

        book_detail = [after for after in book_detail_after if after in book_detail_before]
        return ''.join(book_detail)