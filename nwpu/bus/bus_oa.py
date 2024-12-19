from typing import List

from aiohttp import ClientSession
from yarl import URL

from nwpu.utils.common import DEFAULT_HEADER


class BusOaUrls:
    OA_URL = "https://uis.nwpu.edu.cn/cas/login?service=https%3a%2f%2fhq-bus.nwpu.edu.cn%2fbs%2f%3ftargetUrl%3dbase64aHR0cHM6Ly9ocS1idXMubndwdS5lZHUuY24vaDUvIy9zY2hvb2xCdXNCb29raW5nSG9tZQ%3d%3d"

class BusOaRequest:
    @staticmethod
    def get_redirect_url() -> str:
        return BusOaUrls.OA_URL.split('?', 1)[1].removeprefix('service=')

    @staticmethod
    async def authorize(sess: ClientSession) -> List[URL]:
        resp = await sess.get(BusOaUrls.OA_URL, headers=DEFAULT_HEADER, allow_redirects=True)
        redirects = [x.url for x in resp.history]
        redirects.append(resp.url)
        await sess.get(redirects[-1], headers=DEFAULT_HEADER, allow_redirects=True)
        sess.cookie_jar.update_cookies(resp.cookies)
        return redirects