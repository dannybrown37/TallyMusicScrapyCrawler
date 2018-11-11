# -*- coding: utf-8 -*-
import scrapy
from datetime import date
from dateutil.relativedelta import relativedelta
from scrapy.selector import HtmlXPathSelector


class BluetavernbotSpider(scrapy.Spider):
    name = 'bluetavernbot'
    start_urls = ['http://www.zebrawebworks.com/zebra/bluetavern/index.cfm/']
    custom_settings = {
        'FEED_URI' : 'output/bluetavernoutput.json'
    }

    def parse(self, response):
        now = date.today()
        later = date.today() + relativedelta(months=+1)

        while now <= later:
            y = now.year
            m = now.month
            d = now.day
            yield response.follow(
                "http://www.zebrawebworks.com/zebra/bluetavern/day.cfm?&year="
                + str(y) + "&month=" + str(m) + "&day=" + str(d),
                self.parse_concert
            )
            now += relativedelta(days=+1)

        #http://www.zebrawebworks.com/zebra/bluetavern/day.cfm?&year=2018&month=6&day=1

    def parse_concert(self, response):

        concert = {
            'headliner' : HtmlXPathSelector(response).select(
                "//b/font[@size='3']/text()").extract(),
            'website' : response.request.url,
            'notes' : HtmlXPathSelector(response).select(
                "//td[@class='topicText']/text()").extract(),
            'venue' : 'Blue Tavern',
            'venue_address' : '1206 N Monroe St',
            'venue_website' : 'http://www.bluetaverntallahassee.com/',
        }

        # if there is not a concert on a day, don't yield, just move on
        if concert['headliner'] == []:
            return

        # This data has a ton of junk, so we'll start by filtering that out
        escapes = ''.join([chr(char) for char in range(1, 32)])
        table = {ord(char): None for char in escapes}
        for i, item in enumerate(concert['notes']): # Remove escape chars
            concert['notes'][i] = item.translate(table)
            concert['notes'][i] = concert['notes'][i].replace(u'\xa0', u' ')
            concert['notes'][i] = concert['notes'][i].strip()
        # Remove empty strings
        concert['notes'] = filter(None, concert['notes'])

        

        yield concert
