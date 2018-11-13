import dateparser


def military_time_to_standard(time):
    time = time.split(":")
    if int(time[0]) > 12:
        time[0] = str(int(time[0]) - 12)
        time = ':'.join(time) + "pm"
    elif int(time[0]) == 12:
        time = ':'.join(time) + "pm"
    else:
        time = ':'.join(time) + "am"
    return time

def parse_date_and_time(date_time, split_at):
    date_time = date_time.split(split_at)
    if len(date_time) == 1:
        date_time.append("")
    date = date_time[0].strip()
    parsed_date = dateparser.parse(date)
    date_and_time_to_return = []
    date_and_time_to_return.append(str(parsed_date.date()))
    date_and_time_to_return.append(date_time[1].strip())
    if date_and_time_to_return[1][0] == "0": # strip leading zeros from time
        date_and_time_to_return[1] = date_and_time_to_return[1][1:]
    return date_and_time_to_return
