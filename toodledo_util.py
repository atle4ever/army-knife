from datetime import datetime, timedelta 

def strOfDate(ts):
    dt = datetime.fromtimestamp(ts) - timedelta(hours=9)
    return dt.strftime('%Y-%m-%d')
