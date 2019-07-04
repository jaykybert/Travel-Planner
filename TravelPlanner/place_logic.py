import requests
import json

"""This module is responsible for requesting the JSON from
the Google Places API. The places information is saved as
a list of dictionaries, which is then returned.
"""


def get_places(location, keyword):
    """Use requests to get places relevant to the location provided.

    :param location: Location where places will be searched for.
    :param keyword: The type of location being searched for.
    :return places_list: A list of relevant places in location.
    """
    if location is None or keyword is None:
        return None

    api_key = 'AIzaSyCZJeSoQak3iDIK0STpnSirmoLrbLudoL8'

    search_term = '%s %s' % (location, keyword)
    places_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?' \
                 'query=%s&key=%s' % (search_term, api_key)

    places_response = requests.get(places_url)
    if not places_response.ok:
        return None

    else:
        data = json.loads(places_response.text)
        if data['status'] != 'OK':
            return None

        else:
            # Store all place information as a list of dictionaries.
            places_list = []
            for place in data['results']:
                address = place['formatted_address']
                name = place['name']
                try:
                    open_bool = place['opening_hours']['open_now']
                except KeyError:
                    open_bool = 'n/a'
                try:
                    rating = place['rating']
                    rating_total = place['user_ratings_total']
                except KeyError:
                    rating = 'n/a'
                    rating_total = 'n/a'

                p_dict = {'address': address, 'name': name, 'open': open_bool,
                          'rating': rating, 'total': rating_total}

                places_list.append(p_dict)

            return places_list
