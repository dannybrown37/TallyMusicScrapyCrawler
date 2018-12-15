import datetime
import subprocess
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

    # Now let's call the Django command that adds the JSON to our models
    subprocess.check_call(
        'cd ' + dotdot + '../../tallymusic' # cd to TM project
        ' && envtm\\scripts\\activate' # activate virtual environment
        ' && cd TallyMusic' # cd to inner project folders
        ' && python manage.py load_concerts ' + file_name, # command and comma
        shell=True # this was needed to make it work
    )


if __name__ == '__main__':
    copy_json_to_tallymusic(dotdot='../')
