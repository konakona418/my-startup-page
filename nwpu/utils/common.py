import pickle
import time
from enum import Enum

from aiohttp import ClientSession

DEFAULT_HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54"}


def timestamp_sec() -> int:
    return int(time.time())

def timestamp_mill() -> int:
    return int(round(time.time() * 1000))

def timestamp_micro() -> int:
    return int(round(time.time() * 1000000))

class BoolString(str, Enum):
    true = "true"
    false = "false"

def dump_session(session: ClientSession) -> bytes:
    return pickle.dumps(session.cookie_jar)

