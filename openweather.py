# Write your code here :-)

import time
import os
import ssl
import microcontroller
import adafruit_requests

class openweather:
    # location - Use cityname, country code where countrycode is ISO3166 format.
    def __init__(self,
      location="Atlanta, US",
      openweather_token=os.getenv('openweather_token'),
      **kwargs):
        self.location=location
        self.openweather_token=openweather_token
        print ("Openweather token is " + self.openweather_token)

    def fetch(self, requests):
        # openweathermap URL, brings in your location & your token
        url = "http://api.openweathermap.org/data/2.5/weather?q="+self.location
        url += "&appid="+self.openweather_token
        try:
            #  pings openweather
            response = requests.get(url)
            #  packs the response into a JSON
            response_as_json = response.json()
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
            #  gets temp in kelvin
            temperature = response_as_json['main']['temp']
            #  converts temp from kelvin to F
            converted_temp = (temperature - 273.15) * 9/5 + 32
            #  converts temp from kelvin to C
            #  converted_temp = temperature - 273.15

            #  prints out weather data formatted nicely as pulled from JSON
            print()
            print("The current weather in %s is:" % place)
            print(weather)
            print("%s°F" % converted_temp)
            print("%s%% Humidity" % humidity)
            print("%s hPa" % pressure)

        # pylint: disable=broad-except
        except Exception as e:
            print("Error:\n", str(e))
            print("Resetting microcontroller in 10 seconds")
            time.sleep(10)
            microcontroller.reset()
