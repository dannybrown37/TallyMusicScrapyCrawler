# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CdubotSpider(CrawlSpider):
    name = 'cdubot'
    start_urls = ['https://union.fsu.edu/up/upcoming-events/']
    custom_settings = {
        'FEED_URI': 'output/cduoutput.json'
    }

    def parse(self, response):

        for href in response.xpath(
                '//div[@class="localist-widget-hl"]/ol/li/article[@class="event-card"]/a/@href'
                ).extract():
            yield response.follow(href, self.parse_concert)


    def parse_concert(self, response):
        yield {
            "website" : response.request.url,
        }
