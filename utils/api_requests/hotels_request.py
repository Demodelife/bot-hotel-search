import json
import jmespath
from typing import Any
from .api_request import api_request
from loguru import logger


@logger.catch
def post_hotels_request(citi_id: str,
                        hotels_amt: int,
                        sort: str,
                        price_min: int = 50,
                        price_max: int = 300,
                        distance: int = 0) -> Any:

    """Функция, обрабатывающая списки отелей по заданному городу"""

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

    try:
        response = api_request("properties/v2/list", payload, "POST")

        if response:
            response = json.loads(response)
            check_errors = jmespath.search('errors', response)

            if check_errors is None:

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
                    parsed_distance_ftd = list(filter(lambda x: x <= distance, parsed_distance))

                    result = dict()
                    list(map(lambda hotel_id, name, price, dist: result.update({hotel_id: [name, price, dist]}),
                             parsed_hotel_id, parsed_name, parsed_price_rep, parsed_distance_ftd))
                    if result:
                        return result

                    raise PermissionError

                else:
                    if len(length_match) > 0:
                        result = dict()
                        list(map(lambda hotel_id, name, price: result.update({hotel_id: [name, price]}),
                                 parsed_hotel_id, parsed_name, parsed_price_rep))
                        return result

                    raise PermissionError
            raise PermissionError
        raise PermissionError

    except PermissionError as exc:
        logger.exception(exc)
        return False
