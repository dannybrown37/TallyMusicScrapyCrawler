# -*- coding: utf-8 -*-
import scrapy

# Command line syntax to get us started:
# scrapy genspider moonbot tallahassee.moonevents.com/events

class MoonbotSpider(scrapy.Spider):
    name = 'moonbot'
    start_urls = ['http://tallahassee.moonevents.com/events/']
    custom_settings = {
        'FEED_URI': 'output/moonoutput.json'
    }

    def parse(self, response):
        # follow links to concert pages
        for href in response.css("a.imagecache-all-events-page::attr(href)"):
            yield response.follow(href, self.parse_concert)

        # will need to follow links for pagination once available
        for href in response.css("li.pager-item a::attr(href)"):
            yield response.follow(href, self.parse)

    def parse_concert(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'headliner' : extract_with_css("div.field-event-title::text"),
            'venue' : "The Moon",
            'support' : extract_with_css("div.field-special-guests::text"),
            'date' : extract_with_css("div.field-event-date span.date-display-single::text"),
            'doors' : extract_with_css("div.field-doors-open::text"),
            'show' : extract_with_css("div.field-show-starts::text"),
            #'info' : extract_with_css("div.event-body"),
            'url' : response.request.url,
        }
