import sys ; sys.dont_write_bytecode = True
import smtplib
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import scripts.filter_and_combine
import scripts.email_json
import scripts.copy_to_tallymusic
import os

setting = get_project_settings()
process = CrawlerProcess(setting)

output_files = [
    "bbcoutput.json",
    "bluetavernoutput.json",
    "bsharpsoutput.json",
    "cduoutput.json",
    "civicoutput.json",
    "cocaoutput.json",
    "fifththomasoutput.json",
    "fsuoutput.json",
    "junctionoutput.json",
    "moonoutput.json",
    "openingnightsoutput.json",
    "wilburyoutput.json",
]

# If output file exists, delete it. Otherwise data will just be concatenated
for output_file in output_files:
    try:
        os.remove("output/" + output_file)
    except OSError:
        pass

# Have each spider in the project crawl its web
for spider_name in process.spiders.list():
    print ("Running spider %s" % (spider_name))
    process.crawl(spider_name, query="dvh") #query dvh is custom argument used
                                            # in your scrapy

process.start()

# Let's remove empty files
def check_for_empty_file(fpath):
    try:
        return os.stat(fpath).st_size == 0
    except WindowsError:
        pass
for output_file in output_files:
    output_path = os.path.abspath("output/" + output_file)
    if check_for_empty_file(output_path):
        print output_path
        try:
            os.remove(output_path)
        except OSError:
            pass

# Filter and combine the files
scripts.filter_and_combine.combine_json_files()

# Email myself the json file
try:
    scripts.email_json.send_email()
except smtplib.SMTPAuthenticationError: # Don't break everythying if that fails
    print("Email failed to send, moving to write SQL.")

# Copy the file to TallyMusic's JSON folder
# Obviously will need to be rewritten if/when paths change
scripts.copy_to_tallymusic.copy_json_to_tallymusic()
