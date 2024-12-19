import datetime

def expiry_datetime_to_timerec(date)->str:
    timerec = f"19700101T000000|{date.strftime('%Y%m%d')}T{date.strftime('%H%M%S')}"
    return timerec

def timerec_to_expiry_datetime(timerec):
    date = timerec.replace("19700101T000000|","")
    date = datetime.datetime.strptime(date, '%Y%m%dT%H%M%S')
    return date



