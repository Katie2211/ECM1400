import time
import datetime

def get_day_print(day_index):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday" , "Friday", "Saturday" , "Sunday"]
    day = days[day_index]
    return day
def get_date_print():
    localtime = time.localtime(time.time()) ## local time is now a tuple of year month day hour miute second day of week day of year daylights savings
    day = get_day_print(localtime[6])
    date = day + " " + str(localtime[2]) + "/" + str(localtime[1]) + "/" + str(localtime[0]) ## mon 20 nov 2020
    return date

def get_time_calculate():
    localtime = time.localtime(time.time()) ## local time is now a tuple of year month day hour miute second day of week day of year daylights savings

    current_time = str(localtime[3]) + "." + str(localtime[4])  + "." + str(localtime[5])
    return current_time

def convert_to_seconds(alarm_time :str):
    pm_true = False
    hours = 0
    minutes = 0
    seconds = 0
    if alarm_time.endswith("am"):
        alarm_time[:-2]
    elif alarm_time.endswith("pm"):
        alarm_time[:-2]
        pm_true = True
    string_time = str(alarm_time)
    number_of_dots = string_time.count(".")
    if number_of_dots == 2:
        hours, minutes, seconds = alarm_time.split(".")
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)
    elif number_of_dots == 1:
        hours, minutes = alarm_time.split(".")
        hours = int(hours)
        minutes = int(minutes)
    elif number_of_dots == 0:
        hours = int(alarm_time)
    minutes = minutes + (hours *60)
    seconds = seconds + (minutes*60)
    seconds = int(seconds)
    if pm_true:
        seconds = seconds + 43200 # or 12 hrs
    return seconds
