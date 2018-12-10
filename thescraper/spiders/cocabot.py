# -*- coding: utf-8 -*-
import scrapy
import dateparser
from scripts.useful_functions import parse_date_and_time


class CocabotSpider(scrapy.Spider):
    name = 'cocabot'
    start_urls = [('https://www.tallahasseearts.org/event/'
                   '?keyword&start_date&end_date&date_format'
                   '=m-d-Y&term=400&event_location&save_lst_list&view')]
    custom_settings = {
        'FEED_URI' : 'output/cocaoutput.json'
    }

    def parse(self, response):
        # follow links to concert pages
        for href in response.css("div.search-img a::attr(href)"):
            yield response.follow(href, self.parse_concert)

        # follow links to pagination pages
        for href in response.css("li a.next.page-numbers::attr(href)"):
            yield response.follow(href, self.parse)

    def parse_concert(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first()

        notes = []
        for p in response.css("div.desc-evt.apl-internal-content.hidden p"):
            notes.append(p.xpath(".//text()").extract())
        # flatten the notes, they are in nested lists right now
        notes = [item for sublist in notes for item in sublist]
        # now join the list into a string
        notes = ''.join(notes)

        concert = {
            'headliner' : extract_with_css("h1.p-ttl::text"),
            'venue' : extract_with_css(
                "div.locatn div.a-block-ct div b::text"
            ),
            'venue_address' : extract_with_css(
                "div.locatn div.a-block-ct div p::text"
            ),
            'venue_coca_url' : extract_with_css(
                "span.venue-event a::attr(href)"
            ),
            'event_url' : response.xpath(
                "//div[@class='a-block-ct']/p/"
                "a[contains(text(), 'Official Website')]/@href"
            ).extract_first(),
            'event_coca_url' : response.request.url,
            'date_time' : extract_with_css("ul.ind-time li::text"),
            'price' : extract_with_css(
                "div.a-block-ct div.apl-internal-content p::text"
            ),
            'notes' : notes,
        }

        # Parse the date and time
        when_list = parse_date_and_time(concert['date_time'], " at ")
        concert['date'], concert['time'] = when_list[0], when_list[1]
        concert['time'] = concert['time'].split("(")[0].strip()
        del concert['date_time']

        # Parse event website; select official first, COCA as a fallback
        if concert['event_url'] is not None:
            concert['website'] = concert['event_url']
        elif concert['event_coca_url'] is not None:
            concert['website'] = concert['event_coca_url']
        del concert['event_url']
        del concert['event_coca_url']

        # Parse the price, mainly removing null values
        if concert['price']:
            concert['price'] = concert['price'].strip()
        if not concert['price']:
            del concert['price']

        # Special case fix
        if concert['venue'] == "Fifth & Thomas":
            concert['venue'] = "Fifth and Thomas"

        # Let's eliminate duplicates from scraped venues now
        to_skip = [
            'Blue Tavern',
            'Bradfordville Blues Club',
            'Fifth and Thomas',
            'The Moon',
            'The Junction at Monroe',
            'The Wilbury',
        ]
        if any(venue in concert['venue'] for venue in to_skip):
            return

        # Get the official venue website rather than coca's
        venue_coca_url = concert['venue_coca_url']
        if venue_coca_url:
            yield scrapy.Request(
                venue_coca_url,
                meta={'item': concert},
                callback=self.parse_venue,
                dont_filter=True
            )
        else:
            del concert['venue_coca_url']
            yield concert

    def parse_venue(self, response):
        item = response.meta['item']
        item['venue_website'] = response.xpath(
            "//div[@class='art-social-item']/"
            "a[contains(text(), 'Website')]/@href"
        ).extract_first()

        # Parse the venue website // this is not pretty and could be redone
        if 'venue_website' in item:
            if item['venue_website'] is None and item['venue_coca_url']:
                item['venue_website'] = item['venue_coca_url']
                del item['venue_coca_url']
        try:
            if item['venue_coca_url'] is None:
                del item['venue_coca_url']
        except KeyError:
            pass
        if 'venue_coca_url' in item and 'venue_website' in item:
            del item['venue_coca_url']
        if 'venue_coca_url' not in item and 'venue_website' not in item:
            item['venue_website'] = ""

        yield item
