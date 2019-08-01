# -*- coding: utf-8 -*-
import scrapy


class TechcrunchSpider(scrapy.Spider):
    name = 'techcrunch'
    allowed_domains = ['techcrunch.com']
    start_urls = ['https://techcrunch.com/']

    def parse(self, response):
        pass
