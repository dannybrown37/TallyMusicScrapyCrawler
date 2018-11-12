# -*- coding: utf-8 -*-
import scrapy
import dateparser
from scrapy.selector import HtmlXPathSelector


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
                    "/p/a/strong/text()" % headliner_index
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

            # This will grab the headliner when there is no link
            if concert['date_time'] is not None:
                if concert['headliner'] is None:
                    concert['headliner'] = show.xpath(
                        "//div[@data-index='%s']/div/div[@class='textwidget']"
                        "/p/strong/text()" % headliner_index
                    ).extract_first()

            # If we still don't have a headliner, skip to the next row
            if concert['headliner'] is None:
                continue

            # Parse the date and time
            date_time = concert['date_time'].split("@")
            if len(date_time) == 1:
                date_time.append("")
            date = date_time[0].strip()
            parsed_date = dateparser.parse(date)
            concert['date'] = str(parsed_date.date())
            concert['time'] = date_time[1].strip()
            del concert['date_time']

            # Yield it as long as there is a headliner and a date
            yield concert
