# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline


class ScrapyMeizituPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)
    '''
    def item_completed(self, results, item, info):
        image_paths, image_urls = [(x['path'], x['url']) for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        for image_path, image_url in image_paths, image_urls:
            new_image_path = '_'.join(image_url.split('/')[-4])
            os.rename(image_path, new_image_path)
        return item
    '''

