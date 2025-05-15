import datetime


def parse_expiry_time_service(expiry_string: str) -> datetime.timedelta:
    unit = expiry_string[-1]
    value = int(expiry_string[:-1])

    if unit == "d":
        return datetime.timedelta(days=value)
    elif unit == "h":
        return datetime.timedelta(hours=value)
    elif unit == "m":
        return datetime.timedelta(minutes=value)
    else:
        return datetime.timedelta(minutes=value)
