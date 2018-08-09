# -*- coding: utf-8 -*-
import scrapy


class QuotesbotSpider(scrapy.Spider):
    name = 'quotesbot'
    start_urls = ['http://quotes.toscrape.com/page/1/',
                  'http://quotes.toscrape.com/page/2/']

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
