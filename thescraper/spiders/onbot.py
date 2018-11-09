# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector


class OnbotSpider(scrapy.Spider):
    name = 'onbot'
    start_urls = ['https://openingnights.fsu.edu/events/']
    custom_settings = {
        'FEED_URI': 'output/openingnightsoutput.json'
    }

    def parse(self, response):
        # follow links to concert pages
        for href in response.css("p.buttons a.btn.btn-primary.btn-sm::attr(href)"):
            yield response.follow(href, self.parse_concert)


        # follow links for pagination
        for href in response.css("a.page-numbers::attr(href)"):
            yield response.follow(href, self.parse)


    def parse_concert(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first()

        yield {
            'headliner' : extract_with_css("div.event-header h1::text"),
            'website' : response.request.url,
            'info_dump' : response.css("div.meta p::text").extract(),
            'venue' : extract_with_css("div.meta p a::text"),
            'genres' : response.css("div.meta p i a::text").extract(),
        }
