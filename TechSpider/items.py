# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class TechspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def convert_date(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


class TechCrunchArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(convert_date)
    )
    url = scrapy.Field()
    article_id = scrapy.Field()
    image_url = scrapy.Field(
        # override the default processer, need full string here
        output_processor=MapCompose(lambda url: url)
    )
    image_path = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field(
        output_processor=Join(",")
    )
    author = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into TechCrunch(title, create_date, url, article_id, image_url, image_path, tags, content, author)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        params = (self["title"], self["create_date"], self["url"],  self["article_id"],
                  self["image_url"], self["image_path"], self["tags"],
                  self["content"], self["author"])
        return insert_sql, params
