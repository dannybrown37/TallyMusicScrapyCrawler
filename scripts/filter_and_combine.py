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

    # Filter out classes, camps, workshops, lessons
    to_remove = []
    for i in xrange(len(coca_data)):
        if "camp" in coca_data[i]['headliner'].lower() or \
               "class" in coca_data[i]['headliner'].lower() or \
               "workshop" in coca_data[i]['headliner'].lower() or \
               "lessons" in coca_data[i]['headliner'].lower():
            to_remove.insert(0, i)
    for integer in to_remove:
        coca_data.pop(integer)

    # Now we parse the leftover data
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

        # Get the date from the querystring in the website and format
        date = concert['website'].split("?")[1]
        date = date.replace("&year=", "")\
                   .replace("&month=", "-")\
                   .replace("&day=", "-")
        date = date.split("-")
        date[1] = date[1].zfill(2)
        date[2] = date[2].zfill(2)
        concert['date'] = '-'.join(date)

    # Now filter out dates that have multiple shows and create separate objects
    new_concerts = []
    for concert in blue_data:
        if len(concert['headliner']) > 1:
            for _ in range(len(concert['headliner'])):
                new_concert = concert.copy()
                new_concert['headliner'] = str(concert['headliner'][0])
                div = len(concert['notes']) / len(concert['headliner'])
                new_concert['notes'] = new_concert['notes'][:div]
                new_concerts.append(new_concert)
                concert['headliner'].pop(0)
                for _ in range(div):
                    concert['notes'].pop(0)

    blue_data = blue_data + new_concerts

    for concert in blue_data:

        try:
            # Now that all dates have one show, let's extract the data
            concert['headliner'] = str(concert['headliner'])\
                                            .replace("\r", "")\
                                            .replace("\n", " ")\
                                            .replace("[u'", "")\
                                            .replace("']", "")\
                                            .replace("\\r", "")\
                                            .replace("\\n", " ")


        except:
            pass

        # Create the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])

        print concert
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

    master = []
    for sub_data in data:
        for item in sub_data:
            master.append(item)

    date = datetime.datetime.now()
    date = str(date.date())

    # Sort the list of dicts by date
    master.sort(key=lambda item:item['date'], reverse=False)

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
