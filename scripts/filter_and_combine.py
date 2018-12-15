# -*- coding: cp1252 -*-
import sys ; sys.dont_write_bytecode = True
import re
import json
import simplejson
import datetime
import dateparser


def combine_json_files(dotdot=''):
    # THE MOON
    try:
        with open(dotdot + 'output/moonoutput.json') as f:
            moon_data = json.load(f)
    except IOError:
        moon_data = []

    # THE WILBURY
    try:
        with open(dotdot + 'output/wilburyoutput.json') as f:
            wilbury_data = json.load(f)
    except IOError:
        print "not wilbury!"
        wilbury_data = []

    # FIFTH AND THOMAS
    try:
        with open(dotdot + 'output/fifththomasoutput.json') as f:
            fifththomas_data = json.load(f)
    except IOError:
        fifththomas_data = []

    # OPENING NIGHTS
    try:
        with open(dotdot + "output/openingnightsoutput.json") as f:
            openingnights_data = json.load(f)

    except IOError:
        openingnights_data = []

    # THE JUNCTION AT MONROE
    try:
        with open(dotdot + 'output/junctionoutput.json') as f:
            junction_data = json.load(f)
    except IOError:
        junction_data = []

    # COCA
    try:
        with open(dotdot + 'output/cocaoutput.json') as f:
            coca_data = json.load(f)
    except IOError:
        coca_data = []

    # BLUE TAVERN
    try:
        with open(dotdot + 'output/bluetavernoutput.json') as f:
            blue_data = json.load(f)
    except IOError:
        blue_data = []

    # BRADFORDVILLE BLUES CLUB
    try:
        with open(dotdot + 'output/bbcoutput.json') as f:
            bbc_data = json.load(f)
    except IOError:
        bbc_data = []

    # FSU
    try:
        with open(dotdot + 'output/fsuoutput.json') as f:
            fsu_data = json.load(f)
    except IOError:
        fsu_data = []

    # CDU
    try:
        with open(dotdot + 'output/cduoutput.json') as f:
            cdu_data = json.load(f)
    except IOError:
        cdu_data = []
    except ValueError: # might eventually need this for others???
        cdu_data = []

    # Civic Center
    try:
        with open(dotdot + 'output/civicoutput.json') as f:
            civic_data = json.load(f)
    except IOError:
        civic_data = []

###############################################################################

    # Combine all our data so far
    data = [ # The order I tackled the sites...
        moon_data,
        wilbury_data,
        fifththomas_data,
        openingnights_data,
        junction_data,
        coca_data,
        blue_data,
        bbc_data,
        fsu_data,
        cdu_data,
        civic_data
    ]


    date = datetime.datetime.now()
    date = str(date.date())
    # Combine each list of dicts into a master list of dicts
    master = []
    for sub_data in data:
        for item in sub_data:
            if item['date'] >= date:
                master.append(item)

    # Add a slug for every concert
    for concert in master:
        concert['slug'] = slugify(concert['headliner'], concert['date'])

    # Sort the list of dicts by date
    master.sort(key=lambda item:item['date'], reverse=False)

    # Output formatted data into new JSON file
    with open(dotdot + 'parsed_output/concerts-%s.json' % date, 'w') as f:
        simplejson.dump(master, f, indent=2)

###############################################################################

def slugify(headliner, date=""):
    slugify = headliner.lower().strip()
    slugify = re.sub(r"&+", "-and-", slugify)
    slugify = re.sub(r"[\s\W-]+", "-", slugify)
    slugify = re.sub(r"[\'\"]+", "", slugify)
    slugify = re.sub(r"^-", "", slugify)
    slugify = re.sub(r"-$", "", slugify)
    if date:
        slugify += "-" + date
    return slugify



if __name__ == "__main__":
    combine_json_files(dotdot='../')
