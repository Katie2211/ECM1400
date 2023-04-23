import json
import requests
from Time_Handling import get_date_print
def get_news(filter = "BBC News"):
    with open('config.json', 'r') as f:
        end_result = dict()
        api_dict = json.load(f)
        api_key = api_dict["news_api"]
        base_url = "https://newsapi.org/v2/top-headlines?"
        ##api_key = "de6df29d278a48378d35789447cd8f14"
        country = "gb"
        complete_url = base_url + "country=" + country + "&apiKey=" + api_key
        # print response object
        response = requests.get(complete_url)

        news_dict = response.json()
        articles = news_dict["articles"]
        ##print(articles)
        if filter == "BBC News":
            for article in articles:
                if article["source"]["name"] == "BBC News":

                    title = article["title"]
                    description = article["description"]
                    end_result[title] = description
        else:
            for article in articles:
                title = article["title"]
                description = article["description"]
                end_result[title] = description

    return end_result

def get_daily_information():
    all_news = get_news("none")
    top_news = dict()
    for i in all_news:
        if "Covid-19" in i or "coronavirus" in i:
            print(i)
            new_title = i
            new_description = all_news[i]
            top_news[new_title] = new_description
    top_news["date"] = "The current date is " + get_date_print()
    return top_news
news = get_daily_information()
