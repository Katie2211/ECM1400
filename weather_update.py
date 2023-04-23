import json
import requests

def get_weather():
    #Getting data from weather API
    with open('config.json', 'r') as f:
        api_dict = json.load(f)
        api_key = api_dict["weather_api"]
        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        ##city_name = input("Enter city name : ")
        city_name = "Exeter"
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)

        x = response.json()
        y = x["main"]
        z = x["weather"]
        celsius = y["temp"] - 272.15
        feel = y["feels_like"] - 272.15
        location = x["name"]
        weather_description = z[0]["description"]
        print_celsius = str(round(celsius, 2))
        print_feel = str(round(feel, 2))


        # print following values
        output = "Air Temperture = " + print_celsius + " Feels like Temperture = " + print_feel +" Weather Description: " + weather_description + " Location name: Exeter"
        return output
