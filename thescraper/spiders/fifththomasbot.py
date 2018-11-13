# -*- coding: utf-8 -*-
import scrapy
import dateparser
from scripts.useful_functions import parse_date_and_time


class FifththomasbotSpider(scrapy.Spider):
    name = 'fifththomasbot'
    start_urls = ['http://www.fifthandthomas.com/events/list/']
    custom_settings = {
        'FEED_URI': 'output/fifththomasoutput.json'
    }

    def parse(self, response):
        # follow links to concert pages
        for href in response.css("a.tribe-event-url::attr(href)"):
            yield response.follow(href, self.parse_concert)


    def parse_concert(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first()

        # This portion handles the notes key of the concert
        notes = []
        for p in response.css("div.tribe-events-content p"):
            notes.append(p.xpath(".//text()").extract())
        # flatten the notes, they are in nested lists right now
        notes = [item for sublist in notes for item in sublist]
        # now join the list into a string
        notes = ''.join(notes)

        # It's simpler to get the rest of the data
        concert = {
            'headliner' : extract_with_css(
                "h1.tribe-events-single-event-title::text"),
            'venue' : "Fifth and Thomas",
            'venue_address' : '1122 Thomasville Rd',
            'venue_website' : 'http://www.fifthandthomas.com/',
            'website' : response.request.url,
            'date_time' : extract_with_css(
                "h2 span.tribe-event-date-start::text"),
            'cover_age' : response.css(
                "div.tribe-events-content p strong::text").extract(),
            'notes' : notes,
        }

        # Pull out supporting act from headliner if "w/" syntax is used
        if 'w/' in concert['headliner']:
            headliner = concert['headliner'].split('w/')[0].strip()
            concert['support'] = concert['headliner'].split('w/')[1].strip()
            concert['headliner'] = headliner

        # Parse the date and time
        when_list = parse_date_and_time(concert['date_time'], " @ ")
        concert['date'], concert['time'] = when_list[0], when_list[1]
        del concert['date_time']

        # Parse the price, age, and start time if available
        price = []
        for item in concert['cover_age']:

            # price
            if "|" in item:
                split_item = item.split("|")
                for sub_item in split_item:
                    if "cover" in sub_item.lower() or "$" in sub_item:
                        price.append(sub_item.strip())
            elif "cover" in item.lower() or "$" in item:
                price.append(item.strip())

            # age
            if "ages" in item.lower():
                if "|" in item:
                    split_item = item.split("|")
                    for sub_item in split_item:
                        if "ages" in sub_item.lower():
                            concert['age'] = sub_item.strip()
                else:
                    concert['age'] = item.strip()

            # check for and add keys if necessary
            keys = ['price', 'age', 'time']
            for key in keys:
                try:
                    concert[key]
                except KeyError:
                    concert[key] = ""

        concert['price'] = ', '.join(price)
        del concert['cover_age']



        # it's on
        yield concert
