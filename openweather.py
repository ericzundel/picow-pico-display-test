# Write your code here :-)

import time
import os
import ssl
import microcontroller
import adafruit_requests

class openweather:
    # location - Use cityname, country code where countrycode is ISO3166 format.
    def __init__(self,
      openweather_token=os.getenv('openweather_token'),
      **kwargs):
        self.openweather_token=openweather_token
        print ("Openweather token is " + self.openweather_token)

    def fetch(self, requests):
        # openweathermap URL, brings in your location & your token
        #url = "http://api.openweathermap.org/data/3.0/weather?q="+self.location
        #url += "&appid="+self.openweather_token
        url = "http://api.openweathermap.org/data/2.5/weather?"  \
          + "lat=33.7443551&lon=-84.3226479&appid=" + self.openweather_token
        print("Fetching {0}".format(url))
        try:
            response = requests.get(url)
        # pylint: disable=broad-except
        except Exception as e:
            print("Error:\n", str(e))
            print("Resetting microcontroller in 10 seconds")
            time.sleep(10)
            microcontroller.reset()

        #  packs the response into a JSON
        response_as_json = response.json()
        #  store away converted temp from kelvin to F and kelvin to C
        response_as_json['main']['converted_temp_f'] = (response_as_json['main']['temp'] - 273.15) * 9/5 + 32
        response_as_json['main']['converted_temp_c'] = (response_as_json['main']['temp'] - 273.15)
        return response_as_json

    def print(self, response_as_json):
        print()
        #  prints the entire JSON
        print(response_as_json)
        #  gets location name
        place = response_as_json['name']
        #  gets weather type (clouds, sun, etc)
        weather = response_as_json['weather'][0]['main']
        #  gets humidity %
        humidity = response_as_json['main']['humidity']
        #  gets air pressure in hPa
        pressure = response_as_json['main']['pressure']
        temperature = response_as_json['main']['converted_temp_f']

        #  prints out weather data formatted nicely as pulled from JSON
        print()
        print("The current weather in %s is:" % place)
        print(weather)
        print("%s°F" % temperature)
        print("%s%% Humidity" % humidity)
        print("%s hPa" % pressure)
