import requests
import os
import pandas as pd
import pprint as pp
import json
import config 

#Bing location API:
location_api_key = config.location_api_key

# weather_keys = {'probabilityOfPrecipitation' : 'precipitation', 
#                 'temperature' : 'temperature', 
#                 'dewpoint' : 'dewpoint', 
#                 'relativeHumidity' : 'humidity', 
#                 'windSpeed' : 'wind_speed', 
#                 'windDirection' : 'wind_direction'}

weather_keys_2 = {'precipitation' : ('probabilityOfPrecipitation', 'value'), 
                'temperature' : ('temperature', None), 
                'dewpoint' : ('dewpoint', 'value'), 
                'humidity' : ('relativeHumidity', 'value'), 
                'wind_speed' : ('windSpeed', None), 
                'wind_direction' : ('windDirection', None)}

def get_key_value(weather_type, period_dict, weather_keys):
    if weather_keys[weather_type][1] == None:
        return(period_dict[weather_keys[weather_type][0]])
    if weather_keys[weather_type][1] == 'value':
        return(period_dict[weather_keys[weather_type][0]][weather_keys[weather_type][1]])

weather_keys = {'precipitation' : 'probabilityOfPrecipitation', 
                'temperature' : 'temperature', 
                'dewpoint' : 'dewpoint', 
                'humidity' : 'relativeHumidity', 
                'wind_speed' : 'windSpeed', 
                'wind_direction' : 'windDirection'}

class User:
    def __init__(self):
        self.lat = None
        self.lng = None
        self.notifications = dict()


    def add_location(self, street=None, region=None, country=None, zip=None):
        self.street = None #TODO: make this work
        self.region = region #state if in US
        self.country = country #ISO country code
        self.zip = zip #tested in US only

        self.url_key_dict = {
            'street' : {'value' : street, 'key' : 'addressLine'}, #TODO: make this work
            'region' : {'value' : region, 'key' : 'adminDistrict'},
            'country' : {'value' : country, 'key' : 'countryRegion'},
            'zip' : {'value' : zip, 'key' : 'postalCode'}
        }

    def get_coords(self, api_key):
        #User inputs a location and API key
        #Location can be zip code or street (not functional), state, ISO country code
        #Example URL:
        #http://dev.virtualearth.net/REST/v1/Locations?countryRegion={countryRegion}&adminDistrict={adminDistrict}&locality={locality}&postalCode={postalCode}&addressLine={addressLine}&userLocation={userLocation}&userIp={userIp}&usermapView={usermapView}&includeNeighborhood={includeNeighborhood}&maxResults={maxResults}&key={BingMapsKey}

        #Combine location data into single string
        location_list = []
        for line, values in self.url_key_dict.items():
            if values['value']:
                location_list += [f"{values['key']}={values['value']}"]

        #Make request to Bing API and extract lat and lng
        location_string = "&".join(location_list)
        loc_url = f"http://dev.virtualearth.net/REST/v1/Locations?{location_string}&key={api_key}"
        output = requests.get(loc_url).json()

        self.lat = output['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
        self.lng = output['resourceSets'][0]['resources'][0]['point']['coordinates'][1]

    def get_gridpoint_url(self):
        self.gridpoint = requests.get(f"https://api.weather.gov/points/{self.lat},{self.lng}").json()
        
    def get_forecast(self):
        self.forecast = requests.get(self.gridpoint['properties']['forecast']).json()

    def add_notification(self, type, value, relationship, lead_time):
        for lead in lead_time:
            if lead in self.notifications.keys():
                self.notifications[lead].append({'weather_type' : type,
                                                'weather_value' : value})
            if lead not in self.notifications.keys():
                self.notifications[lead] = [{'weather_type' : type,
                                            'weather_value' : value}]
    
    def print_info(self):
        # pp.pprint(self.gridpoint['properties']['forecast'])
        pp.pprint(self.forecast)
        print("test")

    def check_occurrence(self):
        for period in self.forecast['properties']['periods']:
            if period['number'] in self.notifications.keys():
                print(period['number'])
                for threshold in self.notifications[period['number']]:
                    predicted_value = get_key_value(weather_type=threshold['weather_type'], 
                                                    period_dict=period, 
                                                    weather_keys=weather_keys_2)
                    print(threshold['weather_type'])
                    print(threshold['weather_value'])
                    print(predicted_value)
                    print("++++++")
    
def main():
    # forcast_out = requests.get("http://dev.virtualearth.net/REST/v1/Locations?&postalCode={92109}&key={}")
    # test = requests.get("http://dev.virtualearth.net/REST/v1/Locations/US/WA/98052/Redmond/1%20Microsoft%20Way?&key=").json()
    # http://dev.virtualearth.net/REST/v1/Locations?countryRegion={countryRegion}&adminDistrict={adminDistrict}&locality={locality}&postalCode={postalCode}&addressLine={addressLine}&userLocation={userLocation}&userIp={userIp}&usermapView={usermapView}&includeNeighborhood={includeNeighborhood}&maxResults={maxResults}&key={BingMapsKey}
    # test_two = requests.get("http://dev.virtualearth.net/REST/v1/Locations?countryRegion=US&postalCode=92109&key=").json()
    # pp.pprint(test)

    test_user = User()
    test_user.add_location(zip = "92101", country="US", region="CA")
    test_user.get_coords(api_key=location_api_key)
    test_user.get_gridpoint_url()
    test_user.get_forecast()
    # test_user.print_info()
    test_user.add_notification(type="precipitation", value=20, relationship='>', lead_time=[3,2])
    test_user.add_notification(type="precipitation", value=40, relationship='<', lead_time=[4,3])
    test_user.check_occurrence()
    print("+++++++++++")
    print("located")


if __name__ == "__main__":
    main()
