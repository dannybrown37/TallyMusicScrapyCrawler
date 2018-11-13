# -*- coding: utf-8 -*-
import scrapy
import dateparser
from scripts.useful_functions import parse_date_and_time


class BbcbotSpider(scrapy.Spider):
    name = 'bbcbot'
    start_urls = ['https://bradfordvilleblues.com/events-tickets/']
    custom_settings = {
        'FEED_URI': 'output/bbcoutput.json'
    }


    def parse(self, response):
        date_index = -3
        headliner_index = -2
        price_index = -1
        for show in response.css(".panel-layout .panel-grid.panel-has-style"):
            date_index += 4
            headliner_index += 4
            price_index += 4
            # strange starting values above for indices are so we can place
            # these at top of the loop for organizational purposes
            concert = {
                'date_time' : show.xpath(
                    "//div[@data-index='%s']/div/div[@class='textwidget']"
                    "/p/text()" % date_index
                ).extract_first(),

                'headliner' : show.xpath(
                    "//div[@data-index='%s']/div/div[@class='textwidget']"
                    "/p//text()" % headliner_index
                ).extract_first(),

                'price' : show.xpath(
                    "//div[@data-index='%s']/div/div[@class='textwidget']"
                    "/p/text()" % price_index
                ).extract_first(),

                'website' : response.request.url,
                'venue' : "Bradfordville Blues Club",
                'venue_address' : "7152 Moses Ln",
                'venue_website' : (
                    "https://bradfordvilleblues.com/"
                ),
            }

            # If we don't have a headliner or date, skip to the next row
            if concert['headliner'] is None or concert['date_time'] is None:
                continue

            # Parse the date and time
            when_list = parse_date_and_time(concert['date_time'], "@")
            concert['date'], concert['time'] = when_list[0], when_list[1]
            del concert['date_time']

            # Yields away!
            yield concert
