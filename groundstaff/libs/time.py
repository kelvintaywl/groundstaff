from pytz import timezone
import iso8601


def datetime_from_jst_date_string(dt):
    # assumes dt is of YYYY-MM-DD format w/o time
    return iso8601.parse_date(f'{dt}T00:00:00+0900')

def datetime_from_iso8601(dt):
    return iso8601.parse_date(dt)

def to_jst(dt):
    return dt.astimezone(timezone('Asia/Tokyo'))
