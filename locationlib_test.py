import requests
import os
import pandas as pd
import pprint as pp
import json

def get_coords(api_key, **kwargs):
    #User inputs a location and API key
    #Location can be zip code or street, city, state
    #Will default to zip if other data does not make sense (internally to API)
    #loc_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={street},+{city},+{state}&key={location_api_key}"
    location_params = ['street', 'city', 'state', 'zip']
    location = ""

    #Combine location data into single string
    for param in location_params:
        if param in kwargs:
            location += f",+{kwargs[param]}"

    #Remove leading ,+ of location string
    location = location[2:]

    #Make request to Google API and extract lat and lng
    loc_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
    output = requests.get(loc_url).json()
    lat = output['results'][0]['geometry']['location']['lat']
    lng = output['results'][0]['geometry']['location']['lng']
    
    return((lat, lng))

# coordinates = get_coords(location_api_key, zip = "92093")
# print(coordinates)

#https://api.weather.gov/points/38.8894,-77.0352
geocode_out = requests.get("https://api.weather.gov/points/32.88435520000001,-117.2338066").json()
pp.pprint(geocode_out)

with open('geocode.json', 'w') as g:
    json.dump(geocode_out, g)

print("+++++++")
forcast_out = requests.get("https://api.weather.gov/gridpoints/SGX/55,22/forecast").json()
pp.pprint(forcast_out)

with open('forcast.json', 'w') as f:
    json.dump(forcast_out, f)

# print("+++++++")
# forcast_hourly = requests.get("https://api.weather.gov/gridpoints/SGX/55,22/forecast/hourly").json()
# pp.pprint(forcast_hourly)

print("located")

class Event:

    def __init__(self, event_label, event_prob):
        self.event_label = event_label
        self.event_prob = event_prob
        self.event_time = []
        self.event_location = []

    def add_event_notification(self, time, **kwargs):
        location_params = ['street', 'city', 'state', 'zip']

        # event_lat, event_lng = get_coords(self.api_key, **kwargs = kwargs)

class User():

    def capture_event():
        print("Event captured")

    # def evaluate_event(event_d):
