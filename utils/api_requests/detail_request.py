import json
import jmespath
from typing import Any
from .api_request import api_request


def post_detail_request(hotel: str, photo_amt: int = None) -> Any:

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

            if photo_amt is not None:

                details = dict()
                parsed_name = jmespath.search('data.propertyInfo.summary.name', response)
                details[parsed_name] = []

                for i_photo in range(photo_amt):

                    parsed_photo = jmespath.search(
                        f'data.propertyInfo.propertyGallery.images[{i_photo}].image.url', response)
                    parsed_desc = jmespath.search(
                        f'data.propertyInfo.propertyGallery.images[{i_photo}].image.description', response)
                    details[parsed_name].append({parsed_photo: parsed_desc})

                return details

            else:
                details = dict()
                parsed_name = jmespath.search('data.propertyInfo.summary.name', response)
                parsed_address = jmespath.search('data.propertyInfo.'
                                                 'summary.location.'
                                                 'address.addressLine', response)
                parsed_static_img = jmespath.search('data.propertyInfo.'
                                                    'summary.location.'
                                                    'staticImage.url', response)
                details['name'] = parsed_name
                details['address'] = parsed_address
                details['static_img'] = parsed_static_img

                return details

        return False


# print(post_detail_request('31702975', 2))
