import json
import jmespath
from typing import Any
from .api_request import api_request


def post_address_request(hotel: str) -> Any:

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

            parsed_address = jmespath.search('data.propertyInfo.summary.location.address.addressLine', response)

            return parsed_address
    return False


# print(address_request('69483'))
