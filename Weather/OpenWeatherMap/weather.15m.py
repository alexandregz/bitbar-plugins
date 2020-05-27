#!/usr/bin/env python
# -*- coding: utf-8 -*-

# <bitbar.title>Weather - OpenWeatherMap</bitbar.title>
# <bitbar.version>v1.0.2</bitbar.version>
# <bitbar.author>Daniel Seripap</bitbar.author>
# <bitbar.author.github>seripap</bitbar.author.github>
# <bitbar.desc>Grabs simple weather information from openweathermap. Needs configuration for location and API key.</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>

import json
import urllib2
from random import randint

import base64


location = '3109642'
api_key = '1fd74134f9e54be64a3db6f419aba99f'
units = 'metric' # kelvin, metric, imperial
lang = 'en'

def get_wx():

  if api_key == "":
    return False

  try:
    wx = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?id=' + location + '&units=' + units + '&lang=' + lang + '&appid=' + api_key + "&v=" + str(randint(0,100))))
  except urllib2.URLError:
    return False

  if units == 'metric':
    unit = 'C'
  elif units == 'imperial':
    unit = 'F'
  else:
    unit = 'K' # Default is kelvin

  try:
    weather_data = {
      'temperature': str(int(round(wx['main']['temp']))),
      'condition': str(wx['weather'][0]['description'].encode('utf-8')),
      'city': wx['name'],
      'unit': '°' + unit,
      'icon': str(wx['weather'][0]['icon']),
    }
  except KeyError:
    return False

  return weather_data

def render_wx():
  weather_data = get_wx()

  if weather_data is False:
    return 'Could not get weather'

  img = save_icon_and_get_encoded(weather_data['icon'])

  # test com imagem real
  #img = save_icon_and_get_encoded("10d")

  #return weather_data['icon'] + weather_data['condition'] + ' ' + weather_data['temperature'] + weather_data['unit']
  return weather_data['condition'] + ' ' + weather_data['temperature'] + weather_data['unit'] + "| templateImage="+ img



def save_icon_and_get_encoded(icon):
  url = "http://openweathermap.org/img/wn/" + icon + ".png"

  imgRequest = urllib2.Request(url)
  imgData = urllib2.urlopen(imgRequest).read()

  output = open("/tmp/icon2.png",'wb')
  output.write(imgData)
  output.close()

  with open("/tmp/icon2.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

  return encoded_string


print render_wx()
