# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest



class BarkbotSpider(scrapy.Spider):
    pass
    """
    # Scraping FB is not allowed, so I need to find another way to tackle
    # collecting this data
    name = 'barkbot'
    start_urls = [
        'http://www.facebook.com/pg/TheBarkFL/events/?ref=page_internal/'
    ]
    custom_settings = {
        'FEED_URI': 'output/barkoutput.json'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url,
                self.parse,
            )

    def parse(self, response):
        for href in response.css("div#upcoming_events_card a::attr(href)").extract():
            yield response.follow(href, self.parse_concert)

    def parse_concert(self, response):
        concert = {

            "headliner" : response.xpath(
                "//h1[@id='seo_h1_tag']/text()"
            ).extract_first(),

            "venue" : "The Bark",
            "venue_address" : "507 All Saints St.",
            "venue_website" : "https://www.facebook.com/TheBarkFL",

            "date_time" : response.xpath(
                "//li[@id='event_time_info']//text()"
            ).extract(),

            "notes" : response.xpath(
                "//div[@data-testid='event-permalink-details']/span/text()"
            ).extract()

        }

        if concert['headliner']:
            yield concert
        """
