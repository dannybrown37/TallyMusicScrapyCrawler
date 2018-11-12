# -*- coding: utf-8 -*-
import scrapy
import dateparser
import datetime


class JunctionbotSpider(scrapy.Spider):
    name = 'junctionbot'
    start_urls = ['http://junctionatmonroe.com/events.asp']
    custom_settings = {
        'FEED_URI': 'output/junctionoutput.json'
    }


    def parse(self, response):
        # follow links to concert pages
        for href in response.xpath(
            '//div/a[@title="View event details and order tickets"]/@href'
        ).extract():
            yield response.follow(href, self.parse_concert)


    def parse_concert(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first()

        concert = {
            'headliner' : response.xpath(
                "//div[@class='row']/h1/text()").extract_first(),
            'date_time' : response.xpath(
                "//div[@class='row']/div/text()").extract_first().strip(),
            'cover' : response.xpath(
                "//div[@class='row']/b/text()").extract_first(),
            'ticket_prices' : response.xpath(
                "//td[@style='width:10%']/b/text()").extract(),
            'website' : response.request.url,
            'venue' : "The Junction at Monroe",
            'venue_address' : '2011 S Monroe St',
            'venue_website' : 'http://junctionatmonroe.com/',
            'notes' : response.xpath(
                "//div[@class='row']/div[2]/text()"
            ).extract()
        }

        concert['notes'] = '\n'.join(concert['notes'])

        #  Parse the date and time
        parsed_date = dateparser.parse(concert['date_time'])
        concert['date'] = str(parsed_date.date())
        time = str(parsed_date.time())
        time = datetime.datetime.strptime(time, "%H:%M:%S")
        time = time.replace(second=0, microsecond=0)
        concert['time'] = time.strftime("%#I:%M %p")
        del concert['date_time']

        # Parse the cover or ticket price
        if concert['cover']:
            if "cover" in concert['cover'].lower() or "$" in concert['cover']:
                concert['price'] = concert['cover']
        elif concert['ticket_prices']:
            concert['price'] = ', '.join(concert['ticket_prices'])
        del concert['cover']
        del concert['ticket_prices']

        yield concert
