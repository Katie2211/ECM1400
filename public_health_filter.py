from uk_covid19 import Cov19API

from flask import Flask
import json
import requests

def get_local_infection_rate():
    south_west_only = [
        'areaType=region',
        'areaName=South West',
        'date=2020-12-01'
    ]
    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeathsByDeathDate": "newDeathsByDeathDate",
        "cumDeathsByDeathDate": "cumDeathsByDeathDate",
        "hospitalCases": "hospitalCases",
        "covidOccupiedMVBeds": "covidOccupiedMVBeds",
        "cumCasesBySpecimenDateRate" :"cumCasesBySpecimenDateRate"
    }
    api = Cov19API(filters=south_west_only, structure=cases_and_deaths)
    data = api.get_json();
    infections = data['data'][0]['cumCasesBySpecimenDateRate']
    number_of_ppl = 5616000 #ppl in the south west region
    infection_rate = 100*(infections/number_of_ppl)
    return str(infection_rate)
def get_england_rates():
    england_only = [
        'areaType=region',
        'areaName=South West',
        'date=2020-12-01'
    ]
    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeathsByDeathDate": "newDeathsByDeathDate",
        "cumDeathsByDeathDate": "cumDeathsByDeathDate",
        "hospitalCases": "hospitalCases",
        "covidOccupiedMVBeds": "covidOccupiedMVBeds",
        "cumCasesBySpecimenDateRate" :"cumCasesBySpecimenDateRate"
    }
    api = Cov19API(filters=england_only, structure=cases_and_deaths)
    data = api.get_json();
    return data



# print(data['data'][0]['date'])
# print(data['data'][0]['newCasesByPublishDate'])
# print(data['data'][0]['hospitalCases'])
# print(data['data'][0]["covidOccupiedMVBeds"])
# print(data['data'][0]["cumCasesByPublishDateRate"])
# print(get_local_infection_rate())
