import datetime
from shutil import copyfile

def copy_json_to_tallymusic(dotdot=''):

    # First we'll need today's date
    date = datetime.datetime.now()
    date = str(date.date())

    scraper_location = dotdot + 'parsed_output/concerts-%s.json' % date
    tm_path = dotdot + '../../tallymusic/TallyMusic'
    json_extension = '/json/'
    file_name = 'concerts-%s.json' % date
    new_location = tm_path + json_extension + file_name

    copyfile(
        # Obviously will need to be rewritten if/when paths change
        scraper_location,
        new_location
    )

    




if __name__ == '__main__':
    copy_json_to_tallymusic(dotdot='../')
