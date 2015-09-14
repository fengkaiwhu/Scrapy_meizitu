# -*- coding: utf-8 -*-
import scrapy
from scrapy_meizitu.items import ScrapyMeizituItem
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
import logging

logger = logging.getLogger('meizitu')

class MeizituSpider(scrapy.Spider):
    name = "meizitu"
    allowed_domains = ["meizitu.com"]
    start_urls = (
        'http://www.meizitu.com/a/list_1_1.html',
    )

    link_extractor = {
        # 'page': LinkExtractor(allow='list_1_\d+\.html'),
        'content': LinkExtractor(allow='a/\d+\.html')
    }

    _x_query = {
        'name': "//div[@class='metaRight']/h2/a/text()",
        'tags': "//div[@class='metaRight']/p/text()",
        'image_urls': "//div[@id='picture']/p/img/@src"
    }

    def parse(self, response):
        if not response.xpath("//div[@id='wp_page_numbers']/ul/li[@class='thisclass']/text()").extract():
            return

        currentpage = int(response.xpath("//div[@id='wp_page_numbers']/ul/\
        li[@class='thisclass']/text()").extract()[0]) + 1
        nextURL = 'http://www.meizitu.com/a/list_1_' + str(currentpage) + '.html'
        logger.info('Dealing with page: %s', currentpage)
        yield scrapy.Request(url=nextURL, callback=self.parse)

        for link in self.link_extractor['content'].extract_links(response):
            yield scrapy.Request(url=link.url, callback=self.parse_content)

    def parse_content(self, response):
        logger.info('Dealing with images: %s', response.url)
        item_load = ItemLoader(item=ScrapyMeizituItem(), response=response)
        item_load.add_value('url', response.url)
        item_load.add_xpath('name', self._x_query['name'])
        item_load.add_xpath('tags', self._x_query['tags'])
        item_load.add_xpath('image_urls', self._x_query['image_urls'])

        return item_load.load_item()

