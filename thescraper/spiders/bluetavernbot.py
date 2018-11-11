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

    def parse_concert(self, response):

        concert = {
            'headliner' : response.xpath(
                "//b/font[@size='3']/text()").extract(),
            'website' : response.request.url,
            'notes' : response.xpath(
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

        # Get the date from the querystring in the website and format
        date = concert['website'].split("?")[1]
        date = date.replace("&year=", "")\
                   .replace("&month=", "-")\
                   .replace("&day=", "-")
        date = date.split("-")
        date[1] = date[1].zfill(2)
        date[2] = date[2].zfill(2)
        concert['date'] = '-'.join(date)

        # Strip \r\n spaces off the end of lines, replace with: for others
        for i in range(len(concert['headliner'])):
            concert['headliner'][i] = unicode(concert['headliner'][i])\
                .strip("\r\n").replace("\r\n", ": ")

        # Yield multiple concerts for days that have multiple shows
        while len(concert['headliner']) > 1:
            new_concert = concert.copy()
            new_concert['headliner'] = unicode(concert['headliner'][0])
            new_concert['notes'] = []
            have_time = False
            for item in concert['notes']:
                if "pm" in item.lower() and have_time is False:
                    have_time = True
                    new_concert['notes'].append(item)
                elif "pm" in item.lower() and have_time is True:
                    break
                else:
                    new_concert['notes'].append(item)
            # Pop the stuff we just pulled out off of the meta-concert
            concert['headliner'].pop(0)
            for _ in range(len(new_concert['notes'])):
                concert['notes'].pop(0)

            # Yield the new concert
            yield new_concert

        # A few final things to handle before being done
        concert['headliner'] = unicode(concert['headliner'][0])

        # Yield that biznatch
        yield concert
