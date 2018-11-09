# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector


class CocabotSpider(scrapy.Spider):
    name = 'cocabot'
    start_urls = ['https://www.tallahasseearts.org/event/?keyword&start_date&end_date&date_format=m-d-Y&term=400&event_location&save_lst_list&view']
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

        concert = {
            'headliner' : extract_with_css("h1.p-ttl::text"),
            'venue' : extract_with_css("div.locatn div.a-block-ct div b::text"),
            'venue_address' : extract_with_css("div.locatn div.a-block-ct div p::text"),
            'venue_coca_url' : extract_with_css("span.venue-event a::attr(href)"),
            'event_url' : HtmlXPathSelector(response).select(
                "//div[@class='a-block-ct']/p/a[contains(text(), 'Official Website')]/@href")\
                .extract_first(),
            'event_coca_url' : response.request.url,
            'date_time' : extract_with_css("ul.ind-time li::text"),
            'price' : extract_with_css("div.a-block-ct div.apl-internal-content p::text"),
            'notes' : response.css("div.desc-evt p::text").extract(),
        }

        venue_coca_url = concert['venue_coca_url']
        if venue_coca_url:
            yield scrapy.Request(
                                 venue_coca_url,
                                 meta={'item': concert},
                                 callback=self.parse_venue
                                )
        else:
            yield concert

    def parse_venue(self, response):
        item = response.meta['item']
        item['venue_website'] = HtmlXPathSelector(response).select(
                    "//div[@class='art-social-item']/a[contains(text(), 'Website')]/@href")\
                    .extract_first()
        yield item
