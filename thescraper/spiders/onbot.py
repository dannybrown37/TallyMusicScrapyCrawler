# -*- coding: utf-8 -*-
import scrapy
import dateparser
import re
from scrapy.selector import HtmlXPathSelector


class OnbotSpider(scrapy.Spider):
    name = 'onbot'
    start_urls = ['https://openingnights.fsu.edu/events/']
    custom_settings = {
        'FEED_URI': 'output/openingnightsoutput.json'
    }

    def parse(self, response):
        # follow links to concert pages
        for href in response.css("a.btn.btn-primary.btn-sm::attr(href)"):
            yield response.follow(href, self.parse_concert)

        # follow links for pagination
        for href in response.css("a.next.page-numbers::attr(href)"):
            yield response.follow(href, self.parse)


    def parse_concert(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first()

        # headliner and notes sometimes have sub-tags like <em>, so...
        headliner = []
        notes = []
        for elem in response.css("div.event-header h1"):
            headliner.append(elem.xpath(".//text()").extract())
        for elem in response.css("div.main p"):
            notes.append(elem.xpath(".//text()").extract())
        # flatten the headliner, it is in a nested list right now
        headliner = [item for sublist in headliner for item in sublist]
        notes = [item for sublist in notes for item in sublist]
        # now join the list into a string
        headliner = ', '.join(headliner).replace(", , ", ", ").encode('utf-8')
        notes = ''.join(notes).encode('utf-8')

        # Scrape the data!
        concert =  {
            'headliner' : headliner,
            'website' : response.request.url,
            'info_dump' : response.css("div.meta p::text").extract(),
            'venue' : extract_with_css("div.meta p a::text"),
            'venue_website' : extract_with_css("div.meta p a::attr(href)"),
            'genres' : response.css("div.meta p i a::text").extract(),
            'notes' : notes,
        }

        # Lowercase all genres and join into a string
        for index, genre in enumerate(concert['genres']):
            concert['genres'][index] = genre.lower()
        concert['genres']  = ', '.join(concert['genres']).encode('utf-8')

        # Join the notes into a string instead of a list and add genres to top
        concert['notes'] = ''.join(concert['notes'])
        concert['notes'] = '%s\n\n%s' % (concert['genres'], concert['notes'])

        # Parse the date
        parsed_date = dateparser.parse(concert['info_dump'][0])
        concert['date'] = str(parsed_date.date())

        # Parse the time
        concert['time'] = concert['info_dump'][1].strip()

         # Parse the price(s)
        concert['price'] = []
        for item in concert['info_dump']:
            if "$" in item and item.strip() not in concert['price']:
                concert['price'].append(item.strip())
        concert['price'] = ', '.join(concert['price']).encode('utf-8')

        # delete stuff we no longer need
        del concert['info_dump']
        del concert['genres']

        # Finally, go get the venue address from the venue page
        # It's not on the concert page, thanks FSU
        try:
            yield scrapy.Request(
                concert['venue_website'],
                meta={'item' : concert},
                callback=self.parse_venue,
                dont_filter = True # without it only gets one show per venue
            )
        except:
            # We need an address for a concert, so if it's still TBD,
            # let's skip it for now and hope to grab it in the future
            pass

    def parse_venue(self, response):
        item = response.meta['item']
        item['venue_address'] = response.css(
            "div.col-xs-12.col-md-4.col-md-push-8 p::text"
        ).extract()

        # Parse the venue address more appropriately
        for i in range(len(item['venue_address'])):
            item['venue_address'][i] = item['venue_address'][i].strip()
        # Filter out empty strings
        item['venue_address'] = filter(None, item['venue_address'])
        # List to string, yay
        item['venue_address'] = ', '.join(item['venue_address'])

        yield item
