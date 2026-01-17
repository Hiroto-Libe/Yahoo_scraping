import os


def get_env(name, default=None):
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value


APP_ID = get_env("YAHOO_APP_ID")

API_BASE = "https://shopping.yahooapis.jp/ShoppingWebService/V3"
ITEM_SEARCH_ENDPOINT = f"{API_BASE}/itemSearch"
CATEGORY_LIST_ENDPOINT = "https://shopping.yahooapis.jp/ShoppingWebService/V1/categorySearch"

RESULTS_LIMIT = 50
OUTPUT_DIR = get_env("OUTPUT_DIR", "./output")
LOG_DIR = get_env("LOG_DIR", "./logs")
LOG_LEVEL = get_env("LOG_LEVEL", "INFO")
