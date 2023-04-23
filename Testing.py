from Time_Handling import get_day_print
from Time_Handling import get_date_print
from Time_Handling import get_time_calculate
from Time_Handling import convert_to_seconds
from weather_update import get_weather
from news_filter import get_news
from news_filter import get_daily_information
from public_health_filter import get_local_infection_rate
from public_health_filter import get_england_rates
import sched
import time
import pyttsx3
import logging
from flask import Flask
from flask import render_template
from flask import request

s = sched.scheduler(time.time, time.sleep)
app = Flask(__name__)

logging.basicConfig(filename='sys.log', level=logging.DEBUG)
notification_list = []
scheduled_list = []
notifications_dict = dict()
engine = pyttsx3.init()
"""these are the altered functions to test with"""
def daily_notifications_tests():
    notification_list = []
    list_of_time = ["6","12","18","24"]
    for i in range(len(list_of_time)):
        time = convert_to_seconds(list_of_time[i]) - convert_to_seconds(get_time_calculate())
        if time > 0:
            name = str(6*(i+1))+ ".00 Update"
            news_dict = get_daily_information()
            current_time = get_time_calculate()
            sched_notification_test(name, time, True, True, False, True, news_dict)
    return news_dict

def notification_test(name:str, output:str)-> str:
    notification_out = { 'title': name, 'content':output }
    notification_list.append(notification_out)
    for i in scheduled_list:
        if i['title'] == name:
            scheduled_list.remove(i)
    ##logging.info('I told you so')
    return notification_list

def annoncements_test(name:str, output:str):
    notification_test(name, output)
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
    return output

def sched_notification_test(name :str,time :int, news_bool :bool, weather_bool :bool, annonce:bool, infection_bool:bool, news_dict:dict):
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
        s.enter(time , 1, annoncements_test,(name, output))
    elif annonce == False:
        s.enter(time , 1, notification_test,(name, output))
    s.run(blocking=False)


    return scheduled_list

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
        sched_notification_test(alarm_name, sched_time, news_bool, weather_bool, True, False, news_dict)

"""these functions provide the testing for all functions which have straight outputs,
they are imported without modification from there respective files and the responses
are monitored and logged"""
def test_get_time():
    """this functions tests the funtion get_time_calculate to make sure it is getting the right output"""
    logging.info("this functions tests the funtion get_time_calculate to make sure it is getting the right output")
    current_time_calculate = get_time_calculate() ##returns time in hours.minutes.seconds, a form which the user will most liekly use
    dots = current_time_calculate.split('.')
    logging.info(current_time_calculate)
    if len(dots) == 3:
        logging.info("the output for get_time_calculate is in the right format")
    else:
        logging.warning("Something has gone wrong")

def test_get_date():
    """here we will be testing all the funtions relating to retrival of the current date"""
    logging.info("here we will be testing all the funtions relating to retrival of the current date")
    date = get_date_print()
    if date == "Thursday 3/12/2020": ##bare in mind you might need to change this to get the right day
        logging.info("The get_date_print funtion works as expected")
    else:
        logging.info("The get_data_print funtion has not worked as expected")

    day = get_day_print(3)
    if day == "Thursday":
        logging.info("get_day has returned the right day")

def test_convert_to_seconds():
    """Here we test the convert to seconds funtion which will take a time in many forms,
    all which will be tested"""
    logging.info("Here we test the convert to seconds funtion which will take a time in many forms, all which will be tested")
    test_times = [{'time' : "9", 'output': 32400}, {'time':"99",'output':356400}, {'time':"9.9", 'output':32940}, {'time':"9.99", 'output':38340}
     ,{'time':"99.99",'output': 362340}, {'time':"99.9", 'output' :356940},{'time': "99.99.99",'output':362439}, {'time':"9.9.9", 'output':32949}
     , {'time':"9.9.99", 'output':33039}, {'time':"9.99.9", 'output':38349}, {'time':"9.99.99", 'output':38439}, {'time': "99.9.9", 'output':356949}
     ,{'time':"99.99.9", 'output':362349}, {'time':"99.9.99", 'output': 357039}]
    counter = 0
    false_counter = 0
    for i in test_times:
        testing_time = i['time']
        testing_output = i['output']
        if int(convert_to_seconds(testing_time)) == int(testing_output):
            counter = counter + 1

    if counter == len(test_times):
        logging.info("Convert_to_seconds works for every format")

def test_thrid_parties():
    """this test will be seeing if all of the third parties are still working"""
    logging.info("this test will be seeing if all of the third parties are still working")
    weather_bool = True
    try:
        weather = get_weather()
    except:
        weather_bool = False
    if weather_bool:
        logging.info("The get_weather function seems to be working fine")
        logging.info(weather)
    else:
        logging.info("There is an issue with get_weather function")
    news_bool = True
    try:
        news = get_news()
    except:
        news_bool = False
    if news_bool:
        logging.info("The get_news function seems to be working fine")
        logging.info(news)
    else:
        logging.info("There is an issue with get_news function")
    daily_bool = True
    try:
        daily_info = get_daily_information()
    except:
        daily_bool = False
    if daily_bool:
        logging.info("The get_daily_information function seems to be working fine")
        logging.info(daily_info)
    else:
        logging.info("There is an issue with get_daily_information function")

    infection_bool = True
    try:
        local_infection_rate = get_local_infection_rate()
    except:
        infection_bool = False
    if infection_bool:
        logging.info("The local_infection_rate function seems to be working fine")
        logging.info(local_infection_rate)
    else:
        logging.info("There is an issue with local_infection_rate function")

    england_bool = True
    try:
        england_rates = get_england_rates()
    except:
        england_bool = False
    if england_bool:
        logging.info("The get_england_rates function seems to be working fine")
        logging.info(england_rates)
    else:
        logging.info("There is an issue with get_england_rates function")

def alarm_tests():
    """these tests consit of the same funtions as in the alarm system however
    they have been changed to return there values instead of rendering the render_template
    which will be tested seperately"""
    logging.info("these tests consit of the same funtions as in the alarm system however they have been changed to return there values instead of rendering the render_template which will be tested seperately")
    logging.info("This is the output of the daily_notifications_test")
    daily_notification_result = daily_notifications_tests()
    logging.info(daily_notification_result)
    logging.info("this is the output of the notification_test")
    notification_result = notification_test("alarm", "hello")
    logging.info(notification_result)
    ##logging.info("this is to test the output of the annoncements")
    ##annoncement_result = annoncements_test("alarm", "hello")
    ##logging.info(annoncement_result)
    logging.info("here is the scheduled list after the sched_notfications test")
    scheduled_notification_test = sched_notification_test("alarm", 20, True, True, True, True, notifications_dict)
    logging.info(scheduled_notification_test)

def run_web():
    """these will be all the test for routing to the web page which can be accssed from http://127.0.0.1:5000/"""
    logging.info("these will be all the test for routing to the web page which can be accssed from http://127.0.0.1:5000/")
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


test_get_time()
test_get_date()
test_convert_to_seconds()
test_thrid_parties()
alarm_tests()
