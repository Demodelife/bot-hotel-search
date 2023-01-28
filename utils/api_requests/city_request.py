import json
import jmespath
from typing import Any
from .api_request import api_request


def city_request(city: str) -> Any:

    querystring = {"q": city, "locale": "ru_RU"}

    response = api_request("locations/v3/search", querystring, "GET")

    if response:
        response = json.loads(response)
        check_rc = jmespath.search('rc', response)

        if check_rc == 'OK':

            parsed_type = jmespath.search('sr[0].type', response)
            parsed_name = jmespath.search('sr[0].regionNames.shortName', response)
            parsed_city_id = jmespath.search('sr[0].gaiaId', response)

            if parsed_type == 'CITY' and parsed_name == city:
                return parsed_name, parsed_city_id
            return False
    return False


# print(city_request('Берлин'))
