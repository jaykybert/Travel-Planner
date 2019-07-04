import requests
import json

"""This module is responsible for requesting the JSON from
the Google Routes API. The data is converted to other units,
formatted correctly, and then returned.
"""


def metres_to_miles(metres):
    """Convert metre distances to miles.

    :param metres: Distance in metres.
    :return: Distance in miles.
    """
    return round((metres / 1000) * 0.6214, 2)


def format_metres(metres):
    """Format the metric distance depending on its value.

    :param metres: Value in metres.
    :return metric: Formatted metric value.
    """
    if metres >= 1000:
        metric = round(metres / 1000, 2)
        metric = '%s kilometres' % (str(metric))
    else:
        metric = '%s metres' % str(metres)

    return metric


def format_miles(miles):
    """Format the imperial distance depending on its value.

    :param miles: Value in miles.
    :return imperial: Formatted imperial value.
    """
    if miles < 0.5:
        imperial = round(miles * 1760, 2)
        imperial = '%s yards' % (str(imperial))
    else:
        imperial = '%s miles' % str(miles)

    return imperial


def format_time(seconds):
    """Format the time depending on its value.

    :param seconds: Time in seconds.
    :return time: Formatted time value.
    """
    if seconds < 60:
        time = '%s seconds' % (str(seconds))
    elif seconds < 3600:
        time = round(seconds / 60, 2)
        time = '%s minutes' % (str(time))
    else:
        time = round(seconds / 3600, 2)
        time = '%s hours' % (str(time))

    return time


def get_journey(departure, arrival):
    """Use requests to get relevant journey information.

    :param departure: Name/Postcode/Coordinates of departure.
    :param arrival: Name/Postcode/Coordinates of arrival.
    :return journey_list: Overview information of the journey.
    :return journey_step_list: Information about each step of the journey.
    """
    if departure is None or arrival is None:
        return None, None
    api_key = ''

    journey_url = 'https://maps.googleapis.com/maps/api/directions/json?ori' \
                  'gin=%s&destination=%s&key=%s' % (departure, arrival, api_key)

    journey_response = requests.get(journey_url)
    if not journey_response.ok:
        return None, None

    else:
        data = json.loads(journey_response.text)
        if data['status'] != 'OK':
            return None, None

        else:
            # Get information for the journey overview.
            j_start = data['routes'][0]['legs'][0]['start_address']
            j_end = data['routes'][0]['legs'][0]['end_address']

            j_metres = data['routes'][0]['legs'][0]['distance']['value']
            j_metric = format_metres(j_metres)

            j_miles = metres_to_miles(j_metres)
            j_imperial = format_miles(j_miles)

            j_time = data['routes'][0]['legs'][0]['duration']['value']
            j_time = format_time(j_time)

            j_summary = data['routes'][0]['summary']
            j_warnings = data['routes'][0]['warnings']

            j_list = {'start': j_start, 'end': j_end, 'time': j_time,
                      'metric': j_metric, 'imperial': j_imperial,
                      'summary': j_summary, 'warnings': j_warnings}

            all_steps = []

            # Get information for each step of the journey.
            for step in data['routes'][0]['legs'][0]['steps']:
                s_metres = step['distance']['value']
                s_metric = format_metres(s_metres)

                s_miles = metres_to_miles(s_metres)
                s_imperial = format_miles(s_miles)

                s_time = step['duration']['value']
                s_time = format_time(s_time)

                s_route = step['html_instructions']

                s_list = {'route': s_route, 'time': s_time,
                          'metric': s_metric, 'imperial': s_imperial}

                all_steps.append(s_list)

            return j_list, all_steps
