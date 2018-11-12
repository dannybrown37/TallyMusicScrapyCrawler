# -*- coding: cp1252 -*-
import sys ; sys.dont_write_bytecode = True
import re
import json
import datetime
import dateparser


def combine_json_files(dotdot=''):

    # THE MOON
    try:
        with open(dotdot + 'output/moonoutput.json') as f:
            moon_data = json.load(f)
    except IOError:
        moon_data = []

    for concert in moon_data:
        # Parse the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])


    # THE WILBURY
    try:
        with open(dotdot + 'wilburyoutput.json') as f:
            wilbury_data = json.load(f)
    except IOError:
        wilbury_data = []

    for concert in wilbury_data:
        # Parse the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])


    # FIFTH AND THOMAS
    try:
        with open(dotdot + 'output/fifththomasoutput.json') as f:
            fifththomas_data = json.load(f)
    except IOError:
        fifththomas_data = []

    for concert in fifththomas_data:
        # Parse the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])


    # OPENING NIGHTS
    try:
        with open(dotdot + "output/openingnightsoutput.json") as f:
            openingnights_data = json.load(f)

    except IOError:
        openingnights_data = []

    for concert in openingnights_data:
        # Parse the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])

        # Parse unicode characters out of the venue
        concert['venue'] = concert['venue'].replace(u"�", "'")


    # THE JUNCTION AT MONROE
    try:
        with open(dotdot + 'output/junctionoutput.json') as f:
            junction_data = json.load(f)
    except IOError:
        junction_data = []

    for concert in junction_data:
        # Parse the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])


    # COCA
    try:
        with open(dotdot + 'output/cocaoutput.json') as f:
            coca_data = json.load(f)
    except IOError:
        coca_data = []

    for concert in coca_data:
        # Parse the concert slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])


    # BLUE TAVERN
    try:
        with open(dotdot + 'output/bluetavernoutput.json') as f:
            blue_data = json.load(f)
    except IOError:
        blue_data = []

    for concert in blue_data:
        # Create the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])
###############################################################################

    # Combine all our data so far
    data = [
        moon_data,
        wilbury_data,
        fifththomas_data,
        openingnights_data,
        junction_data,
        coca_data,
        blue_data
    ]

    # Combine each list of dicts into a master list of dicts
    master = []
    for sub_data in data:
        for item in sub_data:
            master.append(item)

    # Sort the list of dicts by date
    master.sort(key=lambda item:item['date'], reverse=False)

    date = datetime.datetime.now()
    date = str(date.date())
    # Output formatted data into new JSON file
    with open(dotdot + 'parsed_output/concerts-%s.json' % date, 'w') as f:
        json.dump(master, f, indent=2)

###############################################################################

def slugify(headliner, date=""):
    try:
        slugify = headliner.lower().strip()
        slugify = re.sub(r"&+", "-and-", slugify)
        slugify = re.sub(r"[\s\W-]+", "-", slugify)
        slugify = re.sub(r"[\'\"]+", "", slugify)
        slugify = re.sub(r"^-", "", slugify)
        slugify = re.sub(r"-$", "", slugify)
        if date:
            slugify += "-" + date
        return slugify
    except AttributeError:
        print "Something is wrong with the %s show!" % headliner
        wait = raw_input("press enter")


if __name__ == "__main__":
    combine_json_files(dotdot='../')
