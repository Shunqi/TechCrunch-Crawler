# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request
from urllib import parse

from TechSpider.items import TechCrunchArticleItem, ArticleItemLoader


class TechcrunchSpider(scrapy.Spider):
    name = 'techcrunch'
    allowed_domains = ['techcrunch.com']
    api_base_url = "https://techcrunch.com/wp-json/tc/v1/magazine?page="
    start_urls = []

    for i in range(1, 2):
        start_urls.append(api_base_url + str(i))

    def parse(self, response):

        articles = json.loads(response.body)

        for article_info in articles:
            yield Request(url=parse.urljoin(response.url, article_info["guid"]["rendered"]),
                          meta={}, callback=self.parse_detail)

        pass

    @staticmethod
    def parse_detail(response):
        item_loader = ArticleItemLoader(item=TechCrunchArticleItem(), response=response)

        script = json.loads(response.xpath("//script[@type='application/ld+json']/text()").extract_first())
        title = script['headline']
        create_date = script['dateCreated']
        author = script['creator']
        article_id = script['keywords'][0].split(":")[1]
        img_url = script['image']['url']

        item_loader.add_value("url", response.url)
        item_loader.add_xpath("content", "//*[@class='article-content']/p/text()")
        item_loader.add_xpath("tags", "/html/head/meta[@name='sailthru.tags']/@content")
        item_loader.add_value("title", title)
        item_loader.add_value("create_date", create_date)
        item_loader.add_value("author", author)
        item_loader.add_value("article_id", article_id)
        item_loader.add_value("image_url", img_url)

        content_html = response.css("div.article-content").extract()

        article_item = item_loader.load_item()

        yield article_item
