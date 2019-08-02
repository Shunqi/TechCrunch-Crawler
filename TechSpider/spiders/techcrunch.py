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

    for i in range(1, 4):
        start_urls.append(api_base_url + str(i))

    def parse(self, response):

        articles = json.loads(response.body)

        for article_info in articles:
            yield Request(url=parse.urljoin(response.url, article_info["guid"]["rendered"]),
                          meta={}, callback=self.parse_detail)

        pass


    def parse_detail(self, response):

        article = TechCrunchArticleItem()

        item_loader = ArticleItemLoader(item=TechCrunchArticleItem(), response=response)



        url = response.url

        content = "\n".join(response.xpath("//*[@class='article-content']/p/text()").extract())
        content_html = response.css("div.article-content").extract()

        script = json.loads(response.xpath("//script[@type='application/ld+json']/text()").extract_first())
        title = script['headline']
        create_date = script['dateCreated']
        author = script['creator']

        article_id = script['keywords'][0].split(":")[1]
        tags = response.xpath("/html/head/meta[@name='sailthru.tags']/@content").get("")

        img_url = script['image']['url']



        pass
