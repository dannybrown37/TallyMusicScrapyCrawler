<<<<<<< HEAD
# -*- coding: cp1252 -*-
import sys ; sys.dont_write_bytecode = True
import re
import json
import datetime
import dateparser


def combine_json_files():

    # THE MOON
    try:
        with open('output/moonoutput.json') as f:
            moon_data = json.load(f)
    except IOError:
        moon_data = []

    for concert in moon_data:

        # Parse the date
        parsed_date = dateparser.parse(concert['date'])
        concert['date'] = str(parsed_date.date())

        # Parse the time
        concert['time'] = concert['doors'] + " // " + concert['show']
        del concert['doors']
        del concert['show']

        # Parse the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])

        # Rename url to website
        concert['website'] = concert['url']
        del concert['url']


    # THE WILBURY
    try:
        with open('wilburyoutput.json') as f:
            wilbury_data = json.load(f)
    except IOError:
        wilbury_data = []

    for concert in wilbury_data:

        # First parse the date and time for each show
        date_time = concert['date_time'].split(" at ")
        if len(date_time) == 1:
            date_time.append("")
        date = date_time[0]
        parsed_date = dateparser.parse(date)
        concert['date'] = str(parsed_date.date())
        time = date_time[1][0:7] if date_time[1] else ""
        concert['time'] = time
        del concert['date_time']

        # Next parse out the headliner and supporting bands
        headliner_support = concert['headliner_support'].split(" w/ ")
        if len(headliner_support) == 1:
            headliner_support.append("")
        concert['headliner'] = headliner_support[0].strip()
        concert['support'] = headliner_support[1].strip()
        del concert['headliner_support']

        # Next parse out the price of the show
        if concert['price_etc'] is not None:
            if "$" in concert['price_etc'] or "Free" in concert['price_etc']:
                concert['price'] = concert['price_etc']
            else:
                concert['price'] = ""
        else:
            concert['price'] = ""
        del concert['price_etc']

        # Parse the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])

        # Rename url to website
        concert['website'] = concert['url']
        del concert['url']


    # FIFTH AND THOMAS
    try:
        with open('output/fifththomasoutput.json') as f:
            fifththomas_data = json.load(f)
    except IOError:
        fifththomas_data = []

    for concert in fifththomas_data:

        # Parse the date and time
        date_time = concert['date_time'].split(" @ ")
        concert['date'] = date_time[0]
        concert['time'] = date_time[1]
        parsed_date = dateparser.parse(concert['date'])
        concert['date'] = str(parsed_date.date())
        del concert['date_time']

        # Parse the price, age, and start time if available
        for item in concert['cover_age']:
            if "cover" in item.lower() or "$" in item:
                if "|" in item and "doors" not in item.lower():
                    concert['price'] = item.split(" | ")[0]
                else:
                    concert['price'] = item

            if "ages" in item.lower():
                if "|" in item and "doors" not in item.lower():
                    try:
                        concert['age'] = item.split(" | ")[1]
                    except IndexError:
                        pass
                else:
                    concert['age'] = item

            if "pm" in item.lower() and "until" not in item.lower():
                concert['time'] = item

            try:
                concert['price']
            except KeyError:
                concert['price'] = ""
            try:
                concert['age']
            except KeyError:
                concert['age'] = ""
            try:
                concert['time']
            except KeyError:
                concert['time'] = ""

        del concert['cover_age']

        # Parse the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])


    # OPENING NIGHTS
    try:
        with open("output/openingnightsoutput.json") as f:
            openingnights_data = json.load(f)

    except IOError:
        openingnights_data = []

    for concert in openingnights_data:
        # Parse the date
        parsed_date = dateparser.parse(concert['info_dump'][0])
        concert['date'] = str(parsed_date.date())

        # Parse the time
        concert['time'] = concert['info_dump'][1].strip()

         # Parse the price(s)
        concert['price'] = []
        for item in concert['info_dump']:
            if "$" in item:
                concert['price'].append(item.strip())

        # The price is now in a list; stringify it!
        string_price = ""
        for price in concert['price']:
            string_price += price + ", "
        concert['price'] = string_price.strip()[:-1]

        # Lowercase all genres
        for index, genre in enumerate(concert['genres']):
            concert['genres'][index] = genre.lower()

        del concert['info_dump']

        # Parse the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])

        # Parse unicode characters out of the venue
        concert['venue'] = concert['venue'].replace(u"ï¿½", "'")


    # THE JUNCTION AT MONROE
    try:
        with open('output/junctionoutput.json') as f:
            junction_data = json.load(f)
    except IOError:
        junction_data = []

    for concert in junction_data:

        #  Parse the date and time
        parsed_date = dateparser.parse(concert['date_time'])
        concert['date'] = str(parsed_date.date())
        time = str(parsed_date.time())
        time = datetime.datetime.strptime(time, "%H:%M:%S")
        time = time.replace(second=0, microsecond=0)
        concert['time'] = time.strftime("%#I:%M %p")
        del concert['date_time']

        # Parse the cover or ticket price
        if concert['cover']:
            if "cover" in concert['cover'] or "$" in concert['cover']:
                concert['price'] = concert['cover']
        elif concert['ticket_prices']:
            string_prices = ""
            for price in concert['ticket_prices']:
                string_prices += price + ", "
            concert['price'] = string_prices.strip()[:-1]
        del concert['cover']
        del concert['ticket_prices']

        # Parse the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])


    # COCA
    try:
        with open('output/cocaoutput.json') as f:
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

        # Parse the date and time
        date = concert['date_time'].split(" at ")[0]
        time = concert['date_time'].split(" at ")[1]
        parsed_date = dateparser.parse(date)
        concert['date'] = str(parsed_date.date())
        concert['time'] = time.split(" - ")[0]
        if concert['time'][0] == "0": # strip leading zeros from time
            concert['time'] = concert['time'][1:]
        del concert['date_time']

        # Parse event website; select official first, COCA as a fallback
        if concert['event_url'] is not None:
            concert['website'] = concert['event_url']
        elif concert['event_coca_url'] is not None:
            concert['website'] = concert['event_coca_url']
        del concert['event_url']
        del concert['event_coca_url']

        # Parse the venue website
        if 'venue_website' in concert:
            if concert['venue_website'] is None and concert['venue_coca_url']:
                concert['venue_website'] = concert['venue_coca_url']
                del concert['venue_coca_url']
        if 'venue_coca_url' in concert and concert['venue_coca_url'] is None:
            del concert['venue_coca_url']
        if 'venue_coca_url' in concert and 'venue_website' in concert:
            del concert['venue_coca_url']
        if 'venue_coca_url' not in concert and 'venue_website' not in concert:
            concert['venue_website'] = ""


        # Parse the price, mainly removing null values
        if concert['price']:
            concert['price'] = concert['price'].strip()
        if not concert['price']:
            del concert['price']

        # Parse the venue slug
        concert['venue_slug'] = slugify(concert['venue'])

        # Special case fix:
        if concert['venue'] == "Fifth & Thomas":
            concert['venue'] = "Fifth and Thomas"

        # Parse the concert slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])


    # BLUE TAVERN
    try:
        with open('output/bluetavernoutput.json') as f:
            blue_data = json.load(f)
    except IOError:
        blue_data = []

    # Filter out dates without shows
    to_remove = []
    for i in xrange(len(blue_data)):
        if blue_data[i]['headliner'] == []:
            to_remove.insert(0, i)
    for integer in to_remove:
        blue_data.pop(integer)

    for concert in blue_data:

        # This data has a ton of junk, so we'll start by filtering that out
        escapes = ''.join([chr(char) for char in range(1, 32)])
        table = {ord(char): None for char in escapes}
        for i, item in enumerate(concert['data']): # Remove escape chars
            concert['data'][i] = item.translate(table)
            concert['data'][i] = concert['data'][i].replace(u'\xa0', u' ')
            concert['data'][i] = concert['data'][i].strip()
        concert['data'] = filter(None, concert['data']) # Remove empty strings

        # Get the date from the querystring in the website and format
        date = concert['website'].split("?")[1]
        date = date.replace("&year=", "")\
                   .replace("&month=", "-")\
                   .replace("&day=", "-")
        date = date.split("-")
        date[1] = date[1].zfill(2)
        date[2] = date[2].zfill(2)
        concert['date'] = '-'.join(date)

    # Now filter out dates that have two shows and create separate objects
    new_concerts = []
    for concert in blue_data:

        try:
            if len(concert['headliner']) == 2:
                new_concert = concert.copy()
                new_concert['headliner'] = str(new_concert['headliner'][1])
                concert['headliner'] = str(concert['headliner'][0])
                mid = len(concert['data']) / 2
                new_concert['data'] = new_concert['data'][mid:]
                concert['data'] = concert['data'][0:mid]
                new_concerts.append(new_concert)
        except UnicodeEncodeError:
            pass

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


            # Get the time
            if "PM" in concert['data'][0].upper():
                 concert['time'] = concert['data'][0]
            # Get the price
            if "$" in concert['data'][1]:
                concert['price'] = concert['data'][1].replace("FEE:", "").strip()
            # Genres are going to be intense
            if len(concert['data']) == 3:
                concert['genres'] = [""]
                concert['genres'][0] = concert['data'][2].lower()
            else:
                concert['genres'] = []
            del concert['data']

            if " - " in concert['headliner']:
                genre = concert['headliner'].split(" - ")[1]
                concert['genres'].append(genre)
                concert['headliner'] = concert['headliner'].split(" - ")[0]

            # Details for specific, regular, repeating concerts
            if "belmont & jones" in concert['headliner'].lower():
                concert['headliner'] = "Belmont & Jones"
                concert['genres'][0] = "country"
                concert['genres'].append("blues")
                concert['genres'].append("traditional")

            if "roda vibe" in concert['headliner'].lower():
                concert['genres'][0] = "brazilian"

            for i, genre in enumerate(concert['genres']):
                if "acoustic" in genre.lower():
                    concert['genres'][i] = "acoustic"
                if "songster" in genre.lower():
                    concert['genres'][i] = "songster"
                if "storytelling" in genre.lower():
                    concert['genres'][i] = "storytelling"
                    concert['genres'].append("spoken word")
                if "songwriters" in genre.lower():
                    concert['genres'][i] = "singer-songwriter"
                if len(genre) > 25 and ", " in genre:
                    genres = concert['genres'][i].split(", ")
                    concert['genres'] = []
                    for item in genres:
                        concert['genres'].append(item)
                if "funky time piano" in genre.lower():
                    concert['genres'] = ["funky time piano"]
                if "fee:" in genre.lower() or "$" in genre:
                    concert['price'] = genre.replace("fee:", "").strip()
                    concert['genres'].pop(i)
                if "blues" in genre.lower():
                    concert['genres'][i] = "blues"
                if "bluegrass" in genre.lower():
                    concert['genres'][i] = "bluegrass"
                if "jazz" in genre.lower():
                    concert['genres'][i] = "jazz"
                if "roots" in genre.lower():
                    concert['genres'][i] = "roots"
                if " & " in genre.lower():
                    genres = concert['genres'][i].split(" & ")
                    concert['genres'] = []
                    for item in genres:
                        concert['genres'].append(item)
                if " - " in genre:
                    concert['genres'][i] = ""
        except:
            pass

            # This is just stubborness to do this via programming at this point
            # These are one-off concerts that are just giving the above trouble
            for i in range(len(concert['genres'])):
                if concert['genres'][i].lower() == "blues and jazz":
                    concert['genres'][i] = "blues"
                if "banjo" in concert['genres'][i].lower():
                    concert['genres'][i] = "banjo"
                if "grandfather" in concert['genres'][i].lower():
                    concert['genres'][i] = ""
                if "mississippi sharecropper" in concert['genres'][i].lower():
                    concert['genres'][i] = ""
                if "lyrical" in concert['genres'][i].lower():
                    concert['genres'][i] = "lyrical"

            # Add the venue; should have done this in my spider.
            concert['venue'] = "Blue Tavern"

            # Remove emptry strings for value?
            emptys = []
            for i in range(len(concert['genres'])):
                if concert['genres'][i] == "":
                    emptys.insert(0, i)
            for index in emptys:
                concert['genres'].pop(index)

        # Parse the slug
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

    master = []
    for sub_data in data:
        for item in sub_data:
            master.append(item)


    date = datetime.datetime.now()
    # Output formatted data into new JSON file
    with open('concerts-' + str(date.date()) + '.json', 'w') as f:
        json.dump(master, f, indent=2)

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
    combine_json_files()
=======
# -*- coding: cp1252 -*-
import sys ; sys.dont_write_bytecode = True
import re
import json
import datetime
import dateparser


def combine_json_files():

    # THE MOON
    try:
        with open('output/moonoutput.json') as f:
            moon_data = json.load(f)
    except IOError:
        moon_data = []        

    for concert in moon_data:

        # Parse the date
        parsed_date = dateparser.parse(concert['date'])
        concert['date'] = str(parsed_date.date())

        # Parse the time
        concert['time'] = concert['doors'] + " // " + concert['show']
        del concert['doors']
        del concert['show']

        # Parse the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])

        # Rename url to website
        concert['website'] = concert['url']
        del concert['url']


    # THE WILBURY
    try:
        with open('wilburyoutput.json') as f:
            wilbury_data = json.load(f)
    except IOError:
        wilbury_data = []

    for concert in wilbury_data:
        
        # First parse the date and time for each show
        date_time = concert['date_time'].split(" at ")
        if len(date_time) == 1:
            date_time.append("")
        date = date_time[0]
        parsed_date = dateparser.parse(date)
        concert['date'] = str(parsed_date.date())
        time = date_time[1][0:7] if date_time[1] else ""
        concert['time'] = time
        del concert['date_time']
        
        # Next parse out the headliner and supporting bands
        headliner_support = concert['headliner_support'].split(" w/ ")
        if len(headliner_support) == 1:
            headliner_support.append("")
        concert['headliner'] = headliner_support[0].strip()
        concert['support'] = headliner_support[1].strip()
        del concert['headliner_support']
        
        # Next parse out the price of the show
        if concert['price_etc'] is not None:
            if "$" in concert['price_etc'] or "Free" in concert['price_etc']:
                concert['price'] = concert['price_etc']
            else:
                concert['price'] = ""
        else:
            concert['price'] = ""
        del concert['price_etc']
        
        # Parse the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])

        # Rename url to website
        concert['website'] = concert['url']
        del concert['url']
        
    
    # FIFTH AND THOMAS
    try:
        with open('output/fifththomasoutput.json') as f:
            fifththomas_data = json.load(f)
    except IOError:
        fifththomas_data = []
  
    for concert in fifththomas_data:

        # Parse the date and time
        date_time = concert['date_time'].split(" @ ")
        concert['date'] = date_time[0]
        concert['time'] = date_time[1]
        parsed_date = dateparser.parse(concert['date'])
        concert['date'] = str(parsed_date.date())
        del concert['date_time']

        # Parse the price, age, and start time if available
        for item in concert['cover_age']:
            if "cover" in item.lower() or "$" in item:
                if "|" in item and "doors" not in item.lower():
                    concert['price'] = item.split(" | ")[0]
                else:
                    concert['price'] = item
                
            if "ages" in item.lower():
                if "|" in item and "doors" not in item.lower():
                    try:
                        concert['age'] = item.split(" | ")[1]
                    except IndexError:
                        pass
                else:
                    concert['age'] = item
                
            if "pm" in item.lower() and "until" not in item.lower():
                concert['time'] = item
                
            try:
                concert['price']
            except KeyError:     
                concert['price'] = ""
            try:
                concert['age']
            except KeyError:
                concert['age'] = ""
            try:
                concert['time']
            except KeyError:
                concert['time'] = ""

        del concert['cover_age']

        # Parse the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])


    # OPENING NIGHTS
    try:
        with open("output/openingnightsoutput.json") as f:
            openingnights_data = json.load(f)

    except IOError:
        openingnights_data = []

    for concert in openingnights_data:
        # Parse the date
        parsed_date = dateparser.parse(concert['info_dump'][0])
        concert['date'] = str(parsed_date.date())

        # Parse the time
        concert['time'] = concert['info_dump'][1].strip()

         # Parse the price(s)
        concert['price'] = []
        for item in concert['info_dump']:    
            if "$" in item:
                concert['price'].append(item.strip())
                
        # The price is now in a list; stringify it!
        string_price = ""
        for price in concert['price']:
            string_price += price + ", "
        concert['price'] = string_price.strip()[:-1]

        # Lowercase all genres
        for index, genre in enumerate(concert['genres']):
            concert['genres'][index] = genre.lower()

        del concert['info_dump']

        # Parse the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])

        # Parse unicode characters out of the venue
        concert['venue'] = concert['venue'].replace(u"’", "'")


    # THE JUNCTION AT MONROE
    try:
        with open('output/junctionoutput.json') as f:
            junction_data = json.load(f)
    except IOError:
        junction_data = []

    for concert in junction_data:
        
        #  Parse the date and time
        parsed_date = dateparser.parse(concert['date_time'])
        concert['date'] = str(parsed_date.date())
        time = str(parsed_date.time())
        time = datetime.datetime.strptime(time, "%H:%M:%S")
        time = time.replace(second=0, microsecond=0)
        concert['time'] = time.strftime("%#I:%M %p")
        del concert['date_time']
        
        # Parse the cover or ticket price
        if concert['cover']:
            if "cover" in concert['cover'] or "$" in concert['cover']:
                concert['price'] = concert['cover']
        elif concert['ticket_prices']:
            string_prices = ""
            for price in concert['ticket_prices']:
                string_prices += price + ", "
            concert['price'] = string_prices.strip()[:-1] 
        del concert['cover']
        del concert['ticket_prices']

        # Parse the slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])


    # COCA
    try:
        with open('output/cocaoutput.json') as f:
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
  
        # Parse the date and time
        date = concert['date_time'].split(" at ")[0]
        time = concert['date_time'].split(" at ")[1]
        parsed_date = dateparser.parse(date)
        concert['date'] = str(parsed_date.date())
        concert['time'] = time.split(" - ")[0]
        if concert['time'][0] == "0": # strip leading zeros from time
            concert['time'] = concert['time'][1:]
        del concert['date_time']

        # Parse event website; select official first, COCA as a fallback
        if concert['event_url'] is not None:
            concert['website'] = concert['event_url']      
        elif concert['event_coca_url'] is not None:
            concert['website'] = concert['event_coca_url']
        del concert['event_url']
        del concert['event_coca_url']

        # Parse the venue website
        if 'venue_website' in concert:
            if concert['venue_website'] is None and concert['venue_coca_url']:
                concert['venue_website'] = concert['venue_coca_url']
                del concert['venue_coca_url']
        if 'venue_coca_url' in concert and concert['venue_coca_url'] is None:
            del concert['venue_coca_url']
        if 'venue_coca_url' in concert and 'venue_website' in concert:
            del concert['venue_coca_url']
        if 'venue_coca_url' not in concert and 'venue_website' not in concert:
            concert['venue_website'] = ""
        

        # Parse the price, mainly removing null values
        if concert['price']:
            concert['price'] = concert['price'].strip()
        if not concert['price']:
            del concert['price']

        # Parse the venue slug
        concert['venue_slug'] = slugify(concert['venue'])

        # Special case fix:
        if concert['venue'] == "Fifth & Thomas":
            concert['venue'] = "Fifth and Thomas"

        # Parse the concert slug
        concert['slug'] = slugify(concert['headliner'], concert['date'])    


    # BLUE TAVERN
    try:
        with open('output/bluetavernoutput.json') as f:
            blue_data = json.load(f)
    except IOError:
        blue_data = []

    # Filter out dates without shows
    to_remove = []
    for i in xrange(len(blue_data)):
        if blue_data[i]['headliner'] == []:
            to_remove.insert(0, i)
    for integer in to_remove:
        blue_data.pop(integer)             

    for concert in blue_data:

        # This data has a ton of junk, so we'll start by filtering that out
        escapes = ''.join([chr(char) for char in range(1, 32)])
        table = {ord(char): None for char in escapes}
        for i, item in enumerate(concert['data']): # Remove escape chars
            concert['data'][i] = item.translate(table)
            concert['data'][i] = concert['data'][i].replace(u'\xa0', u' ')
            concert['data'][i] = concert['data'][i].strip()
        concert['data'] = filter(None, concert['data']) # Remove empty strings
        
        # Get the date from the querystring in the website and format 
        date = concert['website'].split("?")[1]
        date = date.replace("&year=", "")\
                   .replace("&month=", "-")\
                   .replace("&day=", "-")
        date = date.split("-")
        date[1] = date[1].zfill(2)
        date[2] = date[2].zfill(2)
        concert['date'] = '-'.join(date)

    # Now filter out dates that have two shows and create separate objects
    new_concerts = []
    for concert in blue_data:
        
        if len(concert['headliner']) == 2:
            new_concert = concert.copy()
            new_concert['headliner'] = str(new_concert['headliner'][1])
            concert['headliner'] = str(concert['headliner'][0])
            mid = len(concert['data']) / 2
            new_concert['data'] = new_concert['data'][mid:]
            concert['data'] = concert['data'][0:mid]
            new_concerts.append(new_concert)

    blue_data = blue_data + new_concerts

    for concert in blue_data:
        
        # Now that all dates have one show, let's extract the data
        concert['headliner'] = str(concert['headliner'])\
                                        .replace("\r", "")\
                                        .replace("\n", " ")\
                                        .replace("[u'", "")\
                                        .replace("']", "")\
                                        .replace("\\r", "")\
                                        .replace("\\n", " ")


        # Get the time
        if "PM" in concert['data'][0].upper():
             concert['time'] = concert['data'][0]
        # Get the price
        if "$" in concert['data'][1]:
            concert['price'] = concert['data'][1].replace("FEE:", "").strip()
        # Genres are going to be intense
        if len(concert['data']) == 3:
            concert['genres'] = [""]
            concert['genres'][0] = concert['data'][2].lower()
        else:
            concert['genres'] = []
        del concert['data']

        if " - " in concert['headliner']:
            genre = concert['headliner'].split(" - ")[1]
            concert['genres'].append(genre)
            concert['headliner'] = concert['headliner'].split(" - ")[0]

        # Details for specific, regular, repeating concerts
        if "belmont & jones" in concert['headliner'].lower():
            concert['headliner'] = "Belmont & Jones"
            concert['genres'][0] = "country"
            concert['genres'].append("blues")
            concert['genres'].append("traditional")

        if "roda vibe" in concert['headliner'].lower():
            concert['genres'][0] = "brazilian"

        for i, genre in enumerate(concert['genres']):
            if "acoustic" in genre.lower():
                concert['genres'][i] = "acoustic"
            if "songster" in genre.lower():
                concert['genres'][i] = "songster"
            if "storytelling" in genre.lower():
                concert['genres'][i] = "storytelling"
                concert['genres'].append("spoken word")
            if "songwriters" in genre.lower():
                concert['genres'][i] = "singer-songwriter"
            if len(genre) > 25 and ", " in genre:
                genres = concert['genres'][i].split(", ")
                concert['genres'] = []
                for item in genres:
                    concert['genres'].append(item)
            if "funky time piano" in genre.lower():
                concert['genres'] = ["funky time piano"]
            if "fee:" in genre.lower() or "$" in genre:
                concert['price'] = genre.replace("fee:", "").strip()
                concert['genres'].pop(i)
            if "blues" in genre.lower():
                concert['genres'][i] = "blues"
            if "bluegrass" in genre.lower():
                concert['genres'][i] = "bluegrass"
            if "jazz" in genre.lower():
                concert['genres'][i] = "jazz"
            if "roots" in genre.lower():
                concert['genres'][i] = "roots"
            if " & " in genre.lower():
                genres = concert['genres'][i].split(" & ")
                concert['genres'] = []
                for item in genres:
                    concert['genres'].append(item)
            if " - " in genre:
                concert['genres'][i] = ""


        # This is just stubborness to do this via programming at this point
        # These are one-off concerts that are just giving the above trouble
        for i in range(len(concert['genres'])):
            if concert['genres'][i].lower() == "blues and jazz":
                concert['genres'][i] = "blues"
            if "banjo" in concert['genres'][i].lower():
                concert['genres'][i] = "banjo"
            if "grandfather" in concert['genres'][i].lower():
                concert['genres'][i] = ""
            if "mississippi sharecropper" in concert['genres'][i].lower():
                concert['genres'][i] = ""
            if "lyrical" in concert['genres'][i].lower():
                concert['genres'][i] = "lyrical"

        # Add the venue; should have done this in my spider.
        concert['venue'] = "Blue Tavern"

        # Remove emptry strings for value?
        emptys = []
        for i in range(len(concert['genres'])):
            if concert['genres'][i] == "":
                emptys.insert(0, i)
        for index in emptys:
            concert['genres'].pop(index)
       
        # Parse the slug
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

    master = []
    for sub_data in data:
        for item in sub_data:
            master.append(item)
        

    date = datetime.datetime.now()
    # Output formatted data into new JSON file
    with open('concerts-' + str(date.date()) + '.json', 'w') as f:
        json.dump(master, f, indent=2)

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
    combine_json_files()
>>>>>>> 3f3467f5b5471529dfc1aa4524d39fad5b2e3df6
