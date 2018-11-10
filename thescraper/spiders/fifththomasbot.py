# -*- coding: utf-8 -*-
import scrapy


class FifththomasbotSpider(scrapy.Spider):
    name = 'fifththomasbot'
    start_urls = ['http://www.fifthandthomas.com/events/list/']
    custom_settings = {
        'FEED_URI': 'output/fifththomasoutput.json'
    }

    def parse(self, response):
        # follow links to concert pages
        for href in response.css("a.tribe-event-url::attr(href)"):
            yield response.follow(href, self.parse_concert)


    def parse_concert(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first()

        yield {
            'headliner' : extract_with_css("h1.tribe-events-single-event-title::text"),
            'venue' : "Fifth and Thomas",
            'venue_address' : '1122 Thomasville Rd',
            'venue_website' : 'http://www.fifthandthomas.com/',
            'website' : response.request.url,
            'date_time' : extract_with_css("h2 span.tribe-event-date-start::text"),
            'cover_age' : response.css("div.tribe-events-content p strong::text").extract(),
            'notes' : response.css("div.tribe-events-content div p::text").extract(),
        }
