import requests
import os
from dotenv import load_dotenv
from typing import Any, Dict, Union, List
from loguru import logger


load_dotenv()


@logger.catch
def api_request(method_endswith: str,
                params: Dict[str, Union[str, int, List, Dict]],
                method_type: str) -> Any:

    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    if method_type == 'GET':
        return get_request(
            url=url,
            params=params,
            headers=headers)
    else:
        return post_request(
            url=url,
            params=params,
            headers=headers)


@logger.catch
def get_request(url, params, headers):
    try:
        response = requests.get(
            url=url,
            headers=headers,
            params=params,
            timeout=15)
        if response.status_code == requests.codes.ok:
            return response.text

        raise PermissionError

    except PermissionError as exc:
        logger.exception(exc)
        return False


@logger.catch
def post_request(url, params, headers):
    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=params,
            timeout=15)
        if response.status_code == requests.codes.ok:
            return response.text

        raise PermissionError

    except PermissionError as exc:
        logger.exception(exc)
        return False
