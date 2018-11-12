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

    def parse(self, response):
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

        # If there's no venue, it's probably not a concert and won't satisfy
        # foreign key requirements, so skip it
        if not concert['venue']:
            return

        # Combine tags and notes, turn into a nice string
        concert['tags'] = ', '.join(list(set(concert['tags']))).strip()
        concert['notes'] = '\n\n'.join(concert['notes']).strip()
        if concert['tags']:
            concert['notes'] = concert['tags'] + '\n\n' + concert['notes']
        del concert['tags']

        # Convert time from military to standard
        concert['time'] = concert['time'].split(":")
        if int(concert['time'][0]) > 12:
            concert['time'][0] = str(int(concert['time'][0]) - 12)
            concert['time'] = ':'.join(concert['time']) + "pm"
        elif int(concert['time'][0]) == 12:
            concert['time'] = ':'.join(concert['time']) + "pm"
        else:
            concert['time'] = ':'.join(concert['time']) + "am"

        # Now let's pick out the venues from this list
        root = "https://calendar.fsu.edu/"
        fsu_venues = [
            {
                # I lazily didn't want to figure out the weird character in
                # Dohnányi Recital Hall, lazily handled below instead 
                "venue" : "yi Recital Hall",
                "venue_address" : "122 N Copeland St",
                "venue_website" : root + "dohnanyi_recital_hall_drh",
            },
            {
                "venue": "Housewright Music Building",
                "venue_address" : "122 N Copeland St",
                "venue_website" : root + "housewright_music_buildinghmu"

            },
            {
                "venue": "Lindsay Recital Hall",
                "venue_address" : "114 N Copeland St",
                "venue_website" : root + "lindsay_recital_hall_lrh"
            },
            {
                "venue": "Longmire Recital Hall",
                "venue_address" : "126 Convocation Way",
                "venue_website" : root + "longmire_recital_hall_lon"
            },
            {
                "venue": "Opperman Music Hall",
                "venue_address" : "114 N Copeland St",
                "venue_website" : root + "opperman_music_hall_omh"
            },
            {
                "venue": "Ruby Diamond Concert Hall",
                "venue_address" : "222 S Copeland St",
                "venue_website" : root + "ruby_diamond_rdch"
            }
        ]

        # Assign the venue info for each concert
        for venue in fsu_venues:
            if venue['venue'] in concert['venue']:
                concert['venue'] = venue['venue']
                if concert['venue'] == "yi Recital Hall":
                    concert['venue'] = "Dohnányi Recital Hall" # so lazy
                concert['venue_address'] = venue['venue_address']
                concert['venue_website'] = venue['venue_website']
                break

        # Now if something has a venue that doesn't have an address, let's skip
        # it, as address is a required field.
        if not concert['venue_address']:
            return

        # Yee-haw!
        yield concert
