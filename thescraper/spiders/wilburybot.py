# -*- coding: utf-8 -*-
import scrapy


class WilburybotSpider(scrapy.Spider):
    name = 'wilburybot'
    allowed_domains = ['thewilburytallahassee.com/music']
    start_urls = ['http://thewilburytallahassee.com/music/']
    custom_settings = {
        'FEED_URI': 'output/wilburyoutput.json'
    }

    def parse(self, response):
        for li in response.css("ul.upcoming-events li"):
            yield {
                'headliner_support': li.css("strong.event-summary::text").extract_first(),
                'venue' : "The Wilbury",
                'venue_address' : '513 W Gaines St',
                'venue_website' : 'https://thewilburytallahassee.com/music/',
                'date_time': li.css("span.event-when::text").extract_first(),
                'price_etc': li.css("span.event-description::text").extract_first(),
                'url' : response.request.url,
            }
