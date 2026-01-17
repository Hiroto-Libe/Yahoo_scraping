import json
import os
from datetime import datetime

from . import config


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def _log_path():
    today = datetime.now().strftime("%Y%m%d")
    return os.path.join(config.LOG_DIR, f"{today}.log")


def log_event(level, message, **fields):
    ensure_dir(config.LOG_DIR)
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "level": level,
        "message": message,
    }
    if fields:
        payload.update(fields)
    with open(_log_path(), "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=True) + "\n")
