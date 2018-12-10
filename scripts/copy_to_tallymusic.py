import datetime
from shutil import copyfile

def copy_json_to_tallymusic(dotdot=''):

    # First we'll need today's date
    date = datetime.datetime.now()
    date = str(date.date())

    copyfile(
        dotdot + 'parsed_output/concerts-%s.json' % date,
        dotdot + '../../tallymusic/TallyMusic/json/concerts-%s.json' % date
    )


if __name__ == '__main__':
    copy_json_to_tallymusic(dotdot='../')
