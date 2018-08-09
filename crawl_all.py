import sys ; sys.dont_write_bytecode = True
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import filter_and_combine

setting = get_project_settings()
process = CrawlerProcess(setting)

for spider_name in process.spiders.list():
    print ("Running spider %s" % (spider_name))
    process.crawl(spider_name,query="dvh") #query dvh is custom argument used in your scrapy

process.start()

filter_and_combine.combine_json_files()
