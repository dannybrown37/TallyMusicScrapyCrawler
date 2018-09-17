# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector


class BbcbotSpider(scrapy.Spider):
    name = 'bbcbot'
    start_urls = ['https://bradfordvilleblues.com/events-tickets/']
    custom_settings = {
        'FEED_URI': 'output/bbcoutput.json'
    }


    def parse(self, response):

        for show in response.css("div.panel-grid.panel-has-style"):

            yield {
                'date_time' : HtmlXPathSelector(show).select(
                    "//div[@data-index='1']/div/div[@class='textwidget']/p/text()")
                    .extract_first().strip(),

                'headliner' : HtmlXPathSelector(show).select(
                    "//div[@data-index='2']/div/div[@class='textwidget']/p/text()")
                    .extract_first().strip(),

                'price' : HtmlXPathSelector(show).select(
                    "//div[@data-index='3']/div/div[@class='textwidget']/p/text()")
                    .extract_first().strip(),

                'website' : response.request.url,

                'venue' : "Bradfordville Blues Club",
            }
