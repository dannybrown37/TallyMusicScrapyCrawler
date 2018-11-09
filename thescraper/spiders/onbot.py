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

        concert =  {
            'headliner' : extract_with_css("div.event-header h1::text"),
            'website' : response.request.url,
            'info_dump' : response.css("div.meta p::text").extract(),
            'venue' : extract_with_css("div.meta p a::text"),
            'venue_website' : extract_with_css("div.meta p a::attr(href)"),
            'genres' : response.css("div.meta p i a::text").extract(),
            'notes' : response.css("div.main p::text").extract(),
        }

        venue_website = concert['venue_website']
        if venue_website:
            yield scrapy.Request(
                venue_website,
                meta={'item' : concert},
                callback=self.parse_venue
            )
        else:
            yield concerts

    def parse_venue(self, response):
        item = response.meta['item']
        item['venue_address'] = response.css(
            "div.col-xs-12.col-md-4.col-md-push-8 p::text"
        ).extract()
        yield item
