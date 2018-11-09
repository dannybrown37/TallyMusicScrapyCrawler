0# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.selector import HtmlXPathSelector


class FsubotSpider(scrapy.Spider):
    name = 'fsubot'
    start_urls = ['https://calendar.fsu.edu/main/calendar?event_types%5B%5D=89123']
    custom_settings = {
        'FEED_URI': 'output/fsuoutput.json'
    }


    def parse(self, response): # div.event_item a.box_left

        # follow links to concert pages
        for href in response.css(".heading .summary a::attr(href)"):
            yield response.follow(href, self.parse_concert)


    def parse_concert(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first()

        yield {
            "headliner" : extract_with_css("h1.summary::text").strip(),
            "date" : HtmlXPathSelector(response).select(
                            "//abbr[@class='dtstart']/@title")
                            .extract_first()[:10],
            "website" : response.request.url,
            "group" : extract_with_css("dd.event-group a::text"),
            "venue" : extract_with_css("p.location a::text").strip(),
            "venue_website" : extract_with_css("p.location a::attr(href)"),
            "venue_address" : extract_with_css("p.location span::text").strip(),
            "price" : extract_with_css("dd.event-cost p::text"),
            "tags" : response.css("dd.event-tags p a::text").extract(),
        }
