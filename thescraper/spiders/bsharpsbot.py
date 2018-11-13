# -*- coding: utf-8 -*-
import scrapy
import dateparser
from dateparser.search import search_dates


class BsharpsbotSpider(scrapy.Spider):
    name = 'bsharpsbot'
    start_urls = ['http://www.b-sharps.com/calendar/']
    custom_settings = {
        'FEED_URI' : 'output/bsharpsoutput.json'
    }

    def parse(self, response):
        for div in response.css('div.txtNew'):
            concert = {
                'website' : response.request.url,
                'notes' : div.css('h1::text').extract(),
                'venue' : 'B Sharps Jazz Cafe',
                'venue_address' : '648 W Brevard St',
                'venue_website' : 'https://www.b-sharps.com/'
            }

            # Remove empty strings to start
            concert['notes'] = [n.strip() for n in concert['notes']]
            concert['notes'] = filter(None, concert['notes'])

            # Skip the concert if we're just facing an empty list
            if concert['notes'] == []:
                continue

            # Look for date and time with dateparser
            for i in range(len(concert['notes'])):
                found = search_dates(concert['notes'][i])
                if found:
                    pass

            yield concert
