import time
import datetime
from KloockyDE.numberstuff import cap_float


def timestamp():
    '''
    Returns timestamp of current time in this Syntax:
        dd-mm-yyyy_hh-mm-ss
        ~> day-month-year_hour-minute-second
    Good for filenaming
    :return: str    : as above
    '''
    return time.strftime('%d-%m-%Y_%H-%M-%S')


def calc_time(before, now, decimals=0):
    '''
    Calculate the time between before and now in seconds
        before and now are ints gathered by time.perf_counter_ns()
    :param before: int
    :param now: int
    :param decimals: int    : How many decimals do you want?
        default:    0
    :return: int or float
    '''
    return cap_float(number=(now - before) / (10 ** 9), decimals=decimals)


def t_print(before, now, decimals=0):
    '''
    Calculate the time between before and now in seconds
        before and now are ints gathered by time.perf_counter_ns()
        prints that time
    :param before: int
    :param now: int
    :param decimals: int    : How many decimals do you want?
        default:    0
    :return: int or float
    '''
    x = calc_time(before, now, decimals)
    print("Dauer:", x, "Sekunden")
    return x


def how_much_time_until(deadline='27.02.2024 09:00:00'):    # Format: 'DD.MM.YYYY hh:mm:ss'
    today = datetime.datetime.fromtimestamp(time.mktime(time.localtime()))
    deadline = datetime.datetime.fromtimestamp(time.mktime(time.strptime(deadline, '%d.%m.%Y %H:%M:%S')))
    difference = deadline - today
    return difference


def how_many_days_until(deadline_date='27.02.2024', latenight=True):  # Format: DD.MM.YYYY
    today = time.localtime()
    if latenight:
        cutoff = 6  # everything before cutoff o'clock is the previous day
        if int(time.strftime('%H', today)) < cutoff:
            today = time.localtime(time.mktime(today) - (cutoff * 3600))
    today = datetime.datetime.fromtimestamp(time.mktime(time.strptime(time.strftime('%d.%m.%Y', today), '%d.%m.%Y')))
    deadline = datetime.datetime.fromtimestamp(time.mktime(time.strptime(deadline_date, '%d.%m.%Y')))
    difference = deadline - today
    return difference.days
