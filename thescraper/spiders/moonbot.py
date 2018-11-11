# -*- coding: utf-8 -*-
import scrapy
import dateparser
from scrapy.selector import HtmlXPathSelector

# Command line syntax to get us started:
# scrapy genspider moonbot tallahassee.moonevents.com/events

class MoonbotSpider(scrapy.Spider):
    name = 'moonbot'
    start_urls = ['http://tallahassee.moonevents.com/events/']
    custom_settings = {
        'FEED_URI': 'output/moonoutput.json'
    }

    def parse(self, response):
        # follow links to concert pages
        for href in response.css("a.imagecache-all-events-page::attr(href)"):
            yield response.follow(href, self.parse_concert)

        # will need to follow links for pagination once available
        for href in response.css("li.pager-item a::attr(href)"):
            yield response.follow(href, self.parse)

    def parse_concert(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        concert = {
            'headliner' : extract_with_css("div.field-event-title::text"),
            'venue' : "The Moon",
            'venue_address' : '1105 E Lafayette St',
            'venue_website' : 'http://tallahassee.moonevents.com/events',
            'support' : extract_with_css("div.field-special-guests::text"),
            'date' : extract_with_css("div.field-event-date span.date-display-single::text"),
            'doors' : extract_with_css("div.field-doors-open::text"),
            'show' : extract_with_css("div.field-show-starts::text"),
            'notes' : extract_with_css("div.event-body p::text"),
            'website' : response.request.url,
            'ticket_link' : response.css("div.field-ticket-url a::attr(href)").extract_first()
        }

        # Parse the date
        parsed_date = dateparser.parse(concert['date'])
        concert['date'] = str(parsed_date.date())

        # Parse the time
        concert['time'] = concert['doors'] + " // " + concert['show']
        del concert['doors']
        del concert['show']


        # Follow the ticket link to extract price(s)
        if concert['ticket_link']:
            yield scrapy.Request(
                concert['ticket_link'],
                meta={'item' : concert},
                callback=self.parse_ticket_price
            )
        else:
            yield concert

    # Extract ticket price(s)
    def parse_ticket_price(self, response):
        item = response.meta['item']
        item['price'] = HtmlXPathSelector(response).select(
            "//tr[@class='ListRow']/td/b/text()"
        ).extract()
        yield item
