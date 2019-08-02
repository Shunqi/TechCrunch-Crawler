# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class TechspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class TechCrunchArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    article_id = scrapy.Field()
    image_url = scrapy.Field(
        output_processor=MapCompose(lambda url: url)
    )
    image_path = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field(
        output_processor=Join(",")
    )
    author = scrapy.Field()
