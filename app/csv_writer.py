import csv
import os
from datetime import datetime

from . import config


DEFAULT_COLUMNS = [
    "fetched_at",
    "name",
    "price",
    "url",
    "store_name",
    "image_url",
    "availability",
    "review_count",
    "review_rate",
]


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def _get(obj, *keys, default=""):
    cur = obj
    for key in keys:
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return default
    return cur


def _map_item(item):
    return {
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
        "name": _get(item, "name"),
        "price": _get(item, "price"),
        "url": _get(item, "url"),
        "store_name": _get(item, "seller", "name"),
        "image_url": _get(item, "image", "medium"),
        "availability": _get(item, "availability"),
        "review_count": _get(item, "review", "count"),
        "review_rate": _get(item, "review", "rate"),
    }


def write_csv(items, columns=None):
    ensure_dir(config.OUTPUT_DIR)
    cols = columns or DEFAULT_COLUMNS
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_itemsearch.csv"
    path = os.path.join(config.OUTPUT_DIR, filename)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for item in items:
            row = _map_item(item)
            writer.writerow({k: row.get(k, "") for k in cols})

    return path
