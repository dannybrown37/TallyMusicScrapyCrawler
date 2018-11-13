# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
from scripts.useful_functions import military_time_to_standard


class CdubotSpider(CrawlSpider):
    name = 'cdubot'
    start_urls = ['https://union.fsu.edu/up/upcoming-events/']
    custom_settings = {
        'FEED_URI': 'output/cduoutput.json'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url,
                self.parse,
            )

    def parse(self, response):
        for href in response.xpath(
            '//div[@class="localist-widget-hl"]'
            '/ol/li/article[@class="event-card"]/a/@href'
        ).extract():
            yield response.follow(href, self.parse_concert)

    def parse_concert(self, response):
        concert = {
            "headliner" : response.xpath(
                '//h1[@class="summary"]/text()').extract_first().strip(),
            "notes" : response.xpath(
                '//div[@class="description"]/p/text()'
            ).extract(),
            "date" : response.xpath(
                "//abbr[@class='dtstart']/@title").extract_first()[:10],
            "time" : response.xpath(
                "//abbr[@class='dtstart']/@title").extract_first()[11:16],
            "venue" : response.xpath(
                "//p[@class='location']/text()").extract(),
            "venue_address" : response.xpath(
                "//p[@class='location']"
                "/span/text()").extract_first().strip(),
            "website" : response.request.url,
        }

        # CDU includes all kinds of nonsense with its headliner names...
        if "CDU Presents".lower() not in concert['headliner'].lower():
            return # skip the ones that aren't music, CDU presents indicates
        concert['headliner'] = concert['headliner'].split(":")[1].strip()
        concert['headliner'] = concert['headliner'].split(" at ")[0].strip()

        # All kinds of fixes needed on the venue;
        concert['venue'] = [v.strip() for v in concert['venue']]
        concert['venue'] = ''.join(concert['venue'])

        # The venue won't have been grabbed if it's in a link, so let's
        # correct that
        if not concert['venue']:
            concert['venue'] = response.xpath(
                "//p[@class='location']/a/text()"
            ).extract_first().strip()
            concert['venue_website'] = response.xpath(
                "//p[@class='location']/a/@href"
            ).extract_first()

        # Replace \r\n with just \n, then join into a nice string
        concert['notes'] = [n.replace("\r", "") for n in concert['notes']]
        concert['notes'] = ''.join(concert['notes'])

        # Convert time from military to standard
        concert['time'] = military_time_to_standard(concert['time'])


        yield concert
