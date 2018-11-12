# -*- coding: utf-8 -*-
import scrapy
import os


class FsubotSpider(scrapy.Spider):
    name = 'fsubot'
    start_urls = [
        'https://calendar.fsu.edu/main/calendar?event_types%5B%5D=89123'
    ]
    custom_settings = {
        'FEED_URI': 'output/fsuoutput.json'
    }


    def parse(self, response): # div.event_item a.box_left

        # follow links to concert pages
        for href in response.css("div.heading h3.summary a::attr(href)"):
            yield response.follow(href, self.parse_concert)


    def parse_concert(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first()

        concert = {
            "headliner" : extract_with_css("h1.summary::text").strip(),
            "date" : response.xpath(
                "//abbr[@class='dtstart']/@title").extract_first()[:10],
            "time" : response.xpath(
                "//abbr[@class='dtstart']/@title").extract_first()[11:16],
            "website" : response.request.url,
            "venue" :response.xpath(
                "//p[@class='location']/text()").extract()[1].strip(),
            "venue_website" : extract_with_css("p.location a::attr(href)"),
            "venue_address" : extract_with_css("p.location span::text"),
            "price" : extract_with_css("dd.event-cost p::text"),
            "tags" : response.css("dd.event-tags p a::text").extract(),
            "notes" : response.css("div.description p::text").extract(),
        }

        # Combine tags and notes, turn into a nice string
        concert['tags'] = ', '.join(list(set(concert['tags']))).strip()
        concert['notes'] = '\n\n'.join(concert['notes']).strip()
        concert['notes'] = concert['tags'] + '\n\n' + concert['notes']
        del concert['tags']

        # Convert time from standard to military
        concert['time'] = concert['time'].split(":")
        if int(concert['time'][0]) > 12:
            concert['time'][0] = str(int(concert['time'][0]) - 12)
            concert['time'] = ':'.join(concert['time']) + "pm"
        else:
            concert['time'] = ':'.join(concert['time']) + "am"

        yield concert
