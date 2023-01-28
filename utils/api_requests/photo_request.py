import json
import jmespath
from typing import Any
from .api_request import api_request


def photo_request(hotel: str, photo_amt: int) -> Any:

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": hotel
    }

    response = api_request("properties/v2/detail", payload, "POST")

    if response:
        response = json.loads(response)
        check_errors = jmespath.search('errors', response)

        if check_errors is None:

            parsed_name = jmespath.search('data.propertyInfo.summary.name', response)
            photo_url = dict()
            photo_url[parsed_name] = []

            for i_photo in range(photo_amt):
                parsed_photo = jmespath.search(
                    f'data.propertyInfo.propertyGallery.images[{i_photo}].image.url', response)
                parsed_desc = jmespath.search(
                    f'data.propertyInfo.propertyGallery.images[{i_photo}].image.description', response)
                photo_url[parsed_name].append({parsed_photo: parsed_desc})

            result = photo_url
            return result
        return False
    return False


# print(photo_request('69483', 5))
