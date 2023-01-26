import os
import requests
import json
from dotenv import load_dotenv
import jmespath
from typing import Any

load_dotenv()


def city_request(city: str) -> Any:
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {"q": city, "locale": 'ru_RU'}

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)
    parsed_type = jmespath.search('sr[0].type', response)
    parsed_name = jmespath.search('sr[0].regionNames.shortName', response)
    parsed_city_id = jmespath.search('sr[0].gaiaId', response)

    if parsed_type == 'CITY' and parsed_name == city:
        return parsed_name, parsed_city_id
    else:
        return False


def hotels_request(citi_id: str,
                   hotels_amt: int,
                   sort: str,
                   price_min: int = 50,
                   price_max: int = 300,
                   distance: int = 0) -> Any:
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": citi_id},
        "checkInDate": {
            "day": 10,
            "month": 10,
            "year": 2022
        },
        "checkOutDate": {
            "day": 15,
            "month": 10,
            "year": 2022
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": hotels_amt,
        "sort": sort,
        "filters": {"price": {
            "max": price_max,
            "min": price_min
        }}
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = json.loads(requests.request("POST", url, json=payload, headers=headers).text)
    parsed_name = jmespath.search('data.propertySearch.properties[].name', response)
    parsed_hotel_id = jmespath.search('data.propertySearch.properties[].id', response)
    parsed_price = jmespath.search('data.propertySearch.properties[].price.lead.formatted', response)

    parsed_price_rep = [i_price.replace(',', '')
                        if ',' in i_price
                        else i_price
                        for i_price in parsed_price]

    length_match = jmespath.search('data.propertySearch.properties', response)

    if sort == 'DISTANCE':
        parsed_distance = jmespath.search('data.propertySearch.properties[].'
                                          'destinationInfo.distanceFromDestination.value', response)
        if parsed_distance[0] <= distance:
            result = dict()
            list(map(lambda hotel_id, name, price, dist: result.update({hotel_id: [name, price, dist]}),
                     parsed_hotel_id, parsed_name, parsed_price_rep, parsed_distance))
            return result
        else:
            return False
    else:
        if len(length_match) > 0:
            result = dict()
            list(map(lambda hotel_id, name, price: result.update({hotel_id: [name, price]}),
                     parsed_hotel_id, parsed_name, parsed_price_rep))
            return result
        else:
            return False


def photo_request(hotel: str, photo_amt: int) -> Any:

    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": hotel
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = json.loads(requests.request("POST", url, json=payload, headers=headers).text)
    parsed_name = jmespath.search('data.propertyInfo.summary.name', response)
    photo_url = dict()
    photo_url[parsed_name] = []

    for i_photo in range(photo_amt):
        parsed_photo = jmespath.search(f'data.propertyInfo.propertyGallery.images[{i_photo}].image.url', response)
        parsed_desc = jmespath.search(f'data.propertyInfo.propertyGallery.images[{i_photo}].image.description', response)
        photo_url[parsed_name].append({parsed_photo: parsed_desc})

    result = photo_url
    return result


# print(photo_request('69483', 5))
# city_request('Берлин')
# print(hotels_request('2734', 10, "PRICE_LOW_TO_HIGH"))
# print(hotels_request('536', 5, "DISTANCE", price_min=50, price_max=300, distance=5))
# "PRICE_HIGH_TO_LOW" "PRICE_LOW_TO_HIGH" "DISTANCE"
