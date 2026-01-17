import time
import requests

from . import config
from .logger import log_event


class ApiError(Exception):
    pass


def _request_json(url, params, retries=2, timeout=10):
    attempt = 0
    while True:
        attempt += 1
        try:
            resp = requests.get(url, params=params, timeout=timeout)
            if resp.status_code != 200:
                raise ApiError(f"HTTP {resp.status_code}")
            return resp.json()
        except Exception as exc:
            log_event("ERROR", "api_request_failed", url=url, attempt=attempt, error=str(exc))
            if attempt > retries:
                raise
            time.sleep(2)


def get_categories():
    params = {
        "appid": config.APP_ID,
        "output": "json",
    }
    return _request_json(config.CATEGORY_LIST_ENDPOINT, params)


def search_items(query, category_id, results=config.RESULTS_LIMIT, start=1, sort=None):
    params = {
        "appid": config.APP_ID,
        "query": query,
        "category_id": category_id,
        "results": results,
        "start": start,
    }
    if sort:
        params["sort"] = sort
    return _request_json(config.ITEM_SEARCH_ENDPOINT, params)
