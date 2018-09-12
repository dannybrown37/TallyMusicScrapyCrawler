<<<<<<< HEAD
import sys ; sys.dont_write_bytecode = True
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import filter_and_combine
import os

setting = get_project_settings()
process = CrawlerProcess(setting)

output_files = [
    "bluetavernoutput.json",
    "cduoutput.json",
    "cocaoutput.json",
    "fifththomasoutput.json",
    "fsuoutput.json",
    "junctionoutput.json",
    "moonoutput.json",
    "openingnightsoutput.json",
    "wilburyoutput.json",
]

# If output file exists, delete it
for output_file in output_files:
    try:
        os.remove("output/" + output_file)
    except OSError:
        pass

# Have each spider in the project crawl its web
for spider_name in process.spiders.list():
    print ("Running spider %s" % (spider_name))
    process.crawl(spider_name, query="dvh") #query dvh is custom argument used in your scrapy

process.start()

# Filter and combine the files
filter_and_combine.combine_json_files()
=======
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
>>>>>>> 3f3467f5b5471529dfc1aa4524d39fad5b2e3df6
