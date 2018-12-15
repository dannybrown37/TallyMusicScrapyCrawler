# -*- coding: utf-8 -*-
import scrapy
import dateparser


class WilburybotSpider(scrapy.Spider):
    name = 'wilburybot'
    allowed_domains = ['thewilburytallahassee.com/music']
    start_urls = ['http://thewilburytallahassee.com/music/']
    custom_settings = {
        'FEED_URI': 'output/wilburyoutput.json'
    }

    def parse(self, response):
        for li in response.css("ul.upcoming-events li"):
            concert = {
                'headliner_support': li.css(
                    "strong.event-summary::text"
                ).extract_first(),
                'venue' : "The Wilbury",
                'venue_address' : '513 W Gaines St',
                'venue_website' : 'https://thewilburytallahassee.com/music/',
                'date_time': li.css(
                    "span.event-when::text"
                ).extract_first(),
                'price_etc': li.css(
                    "span.event-description::text"
                ).extract_first(),
                'website' : response.request.url,
            }

            # First parse the date and time for each show
            date_time = concert['date_time'].split(" at ")
            if len(date_time) == 1:
                date_time.append("")
            date = date_time[0]
            parsed_date = dateparser.parse(date)
            concert['date'] = str(parsed_date.date())
            time = date_time[1][0:7] if date_time[1] else ""
            concert['time'] = time
            del concert['date_time']

            # Next parse out the headliner and supporting bands
            headliner_support = concert['headliner_support'].split(" w/ ")
            if len(headliner_support) == 1:
                headliner_support.append("")
            concert['headliner'] = headliner_support[0].strip()
            concert['support'] = headliner_support[1].strip()
            del concert['headliner_support']

            # Next parse out the price of the show
            # If there's too much data let's just put it in the notes field,
            # which is hidden
            if concert['price_etc']:
                if len(concert['price_etc']) > 100:
                    concert['notes'] = concert['price_etc']
                elif "$" in concert['price_etc']:
                    concert['price'] = concert['price_etc']
                elif "free" in concert['price_etc'].lower():
                    concert['price'] = concert['price_etc']
                else:
                    concert['notes'] = concert['price_etc']
                del concert['price_etc']
            else:
                del concert['price_etc']

            # we done, son
            yield concert
