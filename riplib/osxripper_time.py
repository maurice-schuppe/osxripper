import datetime


COCOA_EPOCH = datetime.datetime(2001, 1, 1)


def get_cocoa_millis(delta_date):
    """
    Get the date time with a millisecond delta
    """
    if delta_date is None:
        return
    else:
        return COCOA_EPOCH + datetime.timedelta(milliseconds=delta_date)


def get_cocoa_seconds(delta_date):
    """
    Get the date time with a millisecond delta
    """
    if delta_date is None:
        return
    else:
        return COCOA_EPOCH + datetime.timedelta(seconds=delta_date)
