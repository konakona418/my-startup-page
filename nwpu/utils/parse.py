import base64
import datetime
import hashlib
import json
import random
import re
from typing import Dict, List, Any
from urllib.parse import urlencode
import uuid


class StringArgsBuilder:
    base_url: str
    parameters: dict

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.parameters = dict()

    def add_param(self, key: str, value: str):
        self.parameters[key] = value
        return self

    def add_params(self, **kwargs):
        self.parameters.update(kwargs)
        return self

    def build(self) -> str:
        return f"{self.base_url}?{urlencode(self.parameters)}"

    def build_raw(self) -> str:
        first = True
        result = self.base_url
        for key, value in self.parameters.items():
            if first:
                first = False
                result += "?"
            else:
                result += "&"
            result += f"{key}={value}"
        return result

def concat_url(url1: str, url2: str) -> str:
    if url1.endswith('/'):
        url1 = url1[:-1]
    if url2.startswith('/'):
        url2 = url2[1:]
    return f"{url1}/{url2}"

def datetime_from_timestamp(ts_mills: int) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(ts_mills / 1000)

def date_from_timestamp(ts_mills: int) -> datetime.date:
    return datetime.date.fromtimestamp(ts_mills / 1000)

def generate_fake_browser_fingerprint() -> tuple[str, Dict[str, str]]:
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/116.0",
    ]
    user_agent = random.choice(user_agents)

    screen_resolutions = [
        (1920, 1080), (1366, 768), (1280, 720), (1536, 864), (1440, 900)
    ]
    screen_resolution = random.choice(screen_resolutions)

    timezone_offset = 8 # UTC+8:00

    webgl_renderers = [
        "WebKit WebGL", "Mozilla WebGL", "ANGLE (NVIDIA GTX 1660 Ti Direct3D11 vs_5_0 ps_5_0)",
        "Google Inc. (NVIDIA)", "Intel Iris OpenGL Engine"
    ]
    webgl_renderer = random.choice(webgl_renderers)

    fingerprint_data = {
        "user_agent": user_agent,
        "screen_resolution": screen_resolution,
        "timezone_offset": timezone_offset,
        "webgl_renderer": webgl_renderer,
    }

    fingerprint_json = json.dumps(fingerprint_data, sort_keys=True)
    fingerprint_hash = hashlib.md5(fingerprint_json.encode()).hexdigest()

    short_fingerprint = fingerprint_hash[:16]

    return short_fingerprint, fingerprint_data

def generate_fake_tracer_id() -> str:
    fake_uuid = uuid.uuid4()
    random_string = base64.b64encode(''.join(random.choices('0123456789abcdef', k=10)).encode()).decode('utf-8')
    print(f"{fake_uuid}_{random_string}")
    return f"{fake_uuid}_{random_string}"


def find_tracer_id(html: str) -> list[str]:
    regex = re.compile(r'<input\s+[^>]*name=["\']execution["\'][^>]*value=["\']([^"\']+)["\']')
    return regex.findall(html)
