import datetime

def timerec_item_to_datatime(date):
    date = datetime.datetime.strptime(date, '%Y%m%dT%H%M%S')
    return date

def timerec_to_start_and_end_date(timerec):
    array = []
    date_array = timerec.split("|")
    for x in date_array:
        array.append(timerec_item_to_datatime(x))
    return array

def start_end_date_to_timerec(start_date, end_date):
    start_date = start_date.strftime('%Y%m%dT%H%M%S')
    end_date = end_date.strftime('%Y%m%dT%H%M%S')
    timerec = f"{start_date}|{end_date}"
    return timerec
