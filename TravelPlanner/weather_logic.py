import requests
import json
from datetime import datetime

"""This module is responsible for requesting the JSON from
the openweathermap API. The temperature is converted from
Kelvin to Celsius and Fahrenheit, and the Wind Speed to
miles-per-hour. The information is then returned.
"""


def kelvin_to_celsius(kelvin_temp):
    """Convert Kelvin temperature to Celsius.

    :param kelvin_temp: Temperature in Kelvin
    :return: Temperature in Celsius
    """
    return round(kelvin_temp - 273.15, 2)


def kelvin_to_fahrenheit(kelvin_temp):
    """Convert Kelvin temperature to Fahrenheit.

    :param kelvin_temp: Temperature in Kelvin
    :return: Temperature in Fahrenheit
    """
    return round(kelvin_temp * 9 / 5 - 459.67, 2)


def ms_to_mph(ms):
    """Convert from metres per second to miles per hour.

    :param ms: Speed in metres per second.
    :return: Speed in miles per hour.
    """
    return round(ms / 0.44704, 2)


def get_current_weather(location):
    """Use requests to get the current weather of the location provided.

    :param location: The location used for the weather.
    :return current_list: A list of relevant weather information.
    """
    if location is None:
        return None

    api_key = ''

    current_weather_url = 'https://api.openweathermap.org/data/2.5' \
                          '/weather?q=%s&APPID=%s' % (location, api_key)
    
    current_weather_response = requests.get(current_weather_url)
    if not current_weather_response.ok:
        return None

    else:
        current_data = json.loads(current_weather_response.text)

        name_1 = current_data['name']
        name_2 = current_data['sys']['country']
        name = '%s, %s' % (name_1, name_2)

        # Suffix: k = Kelvin, c = Celsius, f = Fahrenheit.
        c_temp_k = current_data['main']['temp']
        c_temp_c = kelvin_to_celsius(c_temp_k)
        c_temp_f = kelvin_to_fahrenheit(c_temp_k)

        c_desc_1 = current_data['weather'][0]['main']
        c_desc_2 = current_data['weather'][0]['description']
        c_desc = '%s: %s' % (c_desc_1, c_desc_2)

        c_speed_ms = current_data['wind']['speed']
        c_speed_mph = ms_to_mph(c_speed_ms)

        c_dict = {'temp_k': c_temp_k, 'temp_c': c_temp_c, 'temp_f': c_temp_f,
                  'name': name, 'desc': c_desc, 'speed_ms': c_speed_ms,
                  'speed_mph': c_speed_mph}

        return c_dict


def get_forecast_weather(location):
    """Use requests to get the forecast weather of the location provided.

    :param location: The location used for the weather.
    :return forecast_list: A list of relevant weather information.
    """
    if location is None:
        return None

    api_key = '79712b2beb7ffdde12a83da0c8063723'

    forecast_weather_url = 'https://api.openweathermap.org/data/2.5/' \
                           'forecast?q=%s&APPID=%s' % (location, api_key)

    forecast_weather_response = requests.get(forecast_weather_url)
    if not forecast_weather_response.ok:
        return None

    else:
        forecast_data = json.loads(forecast_weather_response.text)

        all_forecasts = []
        # Store weather information for 12:00 every upcoming day.
        for i in range(len(forecast_data['list'])):
            current_date = datetime.now()
            current_date = datetime.strftime(current_date, '%Y-%m-%d')

            # Ignore today's forecast weather.
            if current_date in forecast_data['list'][i]['dt_txt']:
                continue

            if '12:00:00' in forecast_data['list'][i]['dt_txt']:
                date = datetime.strptime(forecast_data['list'][i]['dt_txt'],
                                         '%Y-%m-%d %H:%M:%S')
                f_date = date.strftime('%A %d %B %Y')

                f_temp_k = forecast_data['list'][i]['main']['temp']
                f_temp_c = kelvin_to_celsius(f_temp_k)
                f_temp_f = kelvin_to_fahrenheit(f_temp_k)

                f_desc_1 = forecast_data['list'][i]['weather'][0]['main']
                f_desc_2 = forecast_data['list'][i]['weather'][0]['description']
                f_desc = '%s: %s' % (f_desc_1, f_desc_2)

                f_speed_ms = forecast_data['list'][i]['wind']['speed']
                f_speed_mph = ms_to_mph(f_speed_ms)

                f_dict = {'date': f_date, 'desc': f_desc, 'temp_k': f_temp_k,
                          'temp_c': f_temp_c, 'temp_f': f_temp_f,
                          'speed_ms': f_speed_ms, 'speed_mph': f_speed_mph}

                all_forecasts.append(f_dict)

        return all_forecasts
