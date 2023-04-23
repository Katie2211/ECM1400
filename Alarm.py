from Time_Handling import get_time_calculate
from Time_Handling import convert_to_seconds
from news_filter import get_news
from news_filter import get_daily_information
from weather_update import get_weather
from public_health_filter import get_local_infection_rate
from flask import Flask
from flask import render_template
from flask import request
import sched
import time
import pyttsx3
import logging
s = sched.scheduler(time.time, time.sleep)
app = Flask(__name__)
notifications_dict = dict()
notification_list = []
scheduled_list = []
engine = pyttsx3.init()
def daily_notifications():
    """The daily notifications function sets up notifications for each 6 hour interval of the day,
    if one or more of those intervals has already occured it will just set up the rest, these annoncements
    will display on the alarms list and move over to the notfications list once the time has been reached, they
    do not say the notfication"""
    notification_list = []
    list_of_time = ["6","12","18","24"]
    for i in range(len(list_of_time)):
        time = convert_to_seconds(list_of_time[i]) - convert_to_seconds(get_time_calculate())
        if time > 0:
            name = str(6*(i+1))+ ".00 Update"
            news_dict = get_daily_information()
            current_time = get_time_calculate()
            sched_notification(name, time, True, True, False, True, news_dict)
    return

def notification(name:str, output:str)-> str:
    """here the notification function will perform the output of the notification, this is triggered by the schedular
    or through the annonce functiin which is also triggered by the sched"""
    notification_out = { 'title': name, 'content':output }
    notification_list.append(notification_out)
    for i in scheduled_list:
        if i['title'] == name:
            scheduled_list.remove(i)
    ##logging.info('I told you so')
    return render_template('template.html', title ='Smart Alarm', notifications = notification_list, image = 'Clock.jpg')

def annoncements(name:str, output:str):
    """The purpose if the annoncments function is to perfrom the text to speech of the notfication, it also triggers the notifications
    to occur as to prevent the annoncements occuring without the notification """
    notification(name, output)
    engine.say(output)
    engine.runAndWait()
    try: # the fix to the earlierDate problem
        while stopper.shouldRun():
            nextfire = runLoop.limitDateForMode_(mode)
            if not stopper.shouldRun():
                break

            soon = NSDate.dateWithTimeIntervalSinceNow_(maxTimeout)
            nextfire = soon.earlierDate_(nextfire)
            if not runLoop.runMode_beforeDate_(mode, nextfire):
                stopper.stop()

    finally:
        PyObjCAppHelperRunLoopStopper.removeRunLoopStopperFromRunLoop_(runLoop)
    return
def sched_notification(name :str,time :int, news_bool :bool, weather_bool :bool, annonce:bool, infection_bool:bool, news_dict:dict):
    """The sched_notfications is a crutial part of the functionality of my alarm, it takes a number of inputs that decide
    the different parts of the notfication and get a series of information from different places to output for the notification
    and then schedule a notificaiton or annoncement depending on the annonce bool"""
    output = ""
    if news_bool:

        news = ""
        for key in news_dict:
            news = news + " " + key + " " + news_dict[key]
        output = output + " " + news
        if weather_bool:
            output = output + " " + get_weather()
        if infection_bool:
            output = output + " " + get_local_infection_rate()
    elif weather_bool:
        output = output + " " + get_weather()
    scheduled_title = name
    content_output = "The alarm is scheduled for: " + str(time) + " seconds time"
    scheduled_list.append( { 'title': scheduled_title, 'content':str(time) })
    if annonce:
        s.enter(time , 1, annoncements,(name, output))
    elif annonce == False:
        s.enter(time , 1, notification,(name, output))
    s.run(blocking=False)


    return render_template('template.html', title ='Smart Alarm', notifications = notification_list, image = 'Clock.jpg', alarms = scheduled_list)

def Handle_inputs():
    """The handle inputs function does exactly that, it handles all the user inputs from the html, it makes sure that the names are
    unique and everything is in the right format, if 2 alarms are enetered with the same name the second alarm should be renamed with a added string of 2
    numbers which is choosen from the list, up to 101 names can be entered in as the same, this function will also trigger the sched_notification function"""
    add_on_list = ["00", "01", "02", "03", "04", "05",
    "06", "07", "08", "09", "10", "11", "12", "13",
    "14", "15", "16", "17", "18", "19", "20", "21",
    "22", "23", "24", "25", "26", '27', '28', '29',
    '30', '31', '32', '33', '34', '35', '36','37', '38', '39',
    '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
    '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '62',
    '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72',
    '73', '74', '75', '76', '77', '78', '79','80', '81','82', '83',
    '84', '85', '86', '87', '89', '90', '91', '92', '93', '94', '95',
    '96', '97', '98', '99']
    weather_bool = False
    news_bool = False
    alarm_name = request.args.get("alarm")
    alarm_time = request.args.get("two")
    news = request.args.get("news")
    weather = request.args.get("weather")
    hours = 0
    minutes = 0
    seconds = 0
    annonce = False

    if alarm_time:

        if weather == "weather":
            weather_bool = True
        if news == "news":
            news_bool = True
        alarm_time = str(alarm_time)
        current_time = get_time_calculate()
        try:
            alarm_seconds = convert_to_seconds(alarm_time)
        except:
            alarm_seconds = 0
        current_seconds = convert_to_seconds(current_time)
        sched_time = alarm_seconds - current_seconds
        bool = True

        for i in range(len(notification_list)):
            notif_dict = notification_list[i]
            notfi_title = notid_dict['title']
            if notif_dict == alarm_name:
                add_on = add_on_list.pop(0)
                alarm_name = alarm_name + add_on
                s.enter(sched_time + 86400, 1, add_on_list.add(add_on))
            #give unique number and add to the name then sched that number to go back on the list once it has been done
        news_dict = get_news()
        sched_notification(alarm_name, sched_time, news_bool, weather_bool, True, False, news_dict)

@app.route('/index')
def new_alarm():
    """here we have the function all index requests are routed to, the new_alarm function, here any inputs will be sent off into the right function
    for there desired outcome and the new lists of scheduled alarms or notifications will be displayed, this handles most of the
    user performed routes"""
    if request.args.get("notif"):
        alarm_name = request.args.get("notif")
        for i in range(len(notification_list)):
            if notification_list[i]['title'] == alarm_name:
                del notification_list[i]
                break
        return render_template('template.html', title ='Smart Alarm', notifications = notification_list, image = 'Clock.jpg', alarms = scheduled_list)
    elif request.args.get("alarm"):
        Handle_inputs()
        return render_template('template.html', title ='Smart Alarm', notifications = notification_list, image = 'Clock.jpg', alarms = scheduled_list)
    elif request.args.get("alarm_item"):
        alarm_name = request.args.get("alarm_item")
        for i in range(len(scheduled_list)):
            if scheduled_list[i]['title'] == alarm_name:
                del scheduled_list[i]
                break
        return render_template('template.html', title ='Smart Alarm', notifications = notification_list, image = 'Clock.jpg', alarms = scheduled_list)

    else:
        return render_template('template.html', title ='Smart Alarm', notifications = notification_list, image = 'Clock.jpg', alarms = scheduled_list)
@app.route('/')
def HTML():
    """the HTML function is the first call when the website is first accessed, it sets up the passive notification for every six hours by calling the
    daily_notifications function and renders the template with these new notifications set"""
    if len(scheduled_list) == 0:
        daily_notifications()

    return render_template('template.html', title ='Smart Alarm', notifications = notification_list, image = 'Clock.jpg', alarms = scheduled_list)
if __name__ == "__main__":
    app.run()
