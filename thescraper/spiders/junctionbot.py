# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector


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

        yield {
            'headliner' : HtmlXPathSelector(response).select(
                            "//div[@class='row']/h1/text()").extract_first(),
            'date_time' : HtmlXPathSelector(response).select(
                            "//div[@class='row']/div/text()").extract_first().strip(),
            'cover' : HtmlXPathSelector(response).select(
                            "//div[@class='row']/b/text()").extract_first(),
            'ticket_prices' : HtmlXPathSelector(response).select(
                            "//td[@style='width:10%']/b/text()").extract(),
            'website' : response.request.url,
            'venue' : "The Junction at Monroe",
        }
