# -*- coding: utf-8 -*-
import scrapy
import dateparser


class CivicbotSpider(scrapy.Spider):
    name = 'civicbot'
    start_urls = ['http://www.tuckerciviccenter.com/events/']
    custom_settings = {
        'FEED_URI': 'output/civicoutput.json'
    }

    def parse(self, response):
        for href in response.xpath(
            '//div[@id="eventsList"]/div/div[2]/a/@href'
        ).extract():
            yield response.follow(href, self.parse_concert)

    def parse_concert(self, response):
        concert = {
            "headliner" : response.xpath(
                "//h1[@class='summary']/text()").extract_first().strip(),
            "support" : response.xpath(
                "//div[@class='event_desc']/h2/text()"
            ).extract_first(),
            "notes" : response.xpath(
                "//div[@class='desc_inner']/p//text()").extract(),
            "date" : response.xpath(
                "//div[@class='showing_detail']/span[@class='date']/text()"
            ).extract(),
            "time" : response.xpath(
                "//div[@class='showing_detail']/span[@class='time']/text()"
            ).extract(),
            "price" : response.xpath(
                "//label[contains(text(), 'Ticket Prices')]/../../td[2]"
                "/div/div/p/text()"
            ).extract_first(),
            "website" : response.request.url,
            "venue" : "Donald L. Tucker Civic Center",
            "venue_website" : "https://www.tuckerciviccenter.com/events",
            "venue_address" : "505 W Pensacola St"
        }

        # Join notes into a string
        concert['notes'] = ''.join(concert['notes'])

        # Then check notes for keywords that might refer to a music event,
        # since the civic center doesn't tag them specifically.
        keywords = ['music','band','singer','songwriter','rapper','album']
        # probably don't want to go too deep with terms here...
        if not any(k in concert['notes'] for k in keywords):
            return # skip this non-concert if none of these keywords appear

        # Cut off "at" from time and convert into string
        if len(concert['time']) == 1:
            concert['time'] = ''.join(concert['time'])
            concert['time'] = concert['time'].replace("at", "").strip()
        else: # This is unlikely to be needed because Tallahassee
            wait = raw_input("Need to update to handle multiple shows!")

        # Parse the date
        if len(concert['date']) == 1:
            concert['date'] = ''.join(concert['date'])
            parsed_date = dateparser.parse(concert['date'])
            concert['date'] = str(parsed_date.date())
        else: # This is unlikely to be needed because Tallahassee
            wait = raw_input("Need to update to handle multiple shows!")

        # Take the disclaimer off of the price
        disclaimer = "*subject to applicable fees"
        concert['price'] = concert['price'].replace(disclaimer, "").strip()

        yield concert
