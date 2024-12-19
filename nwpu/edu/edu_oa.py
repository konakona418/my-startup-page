from typing import List

from aiohttp import ClientSession
from yarl import URL

from nwpu.utils.common import DEFAULT_HEADER


class EduOaUrl:
    REDIRECT = 'https://uis.nwpu.edu.cn/cas/login?service=https%3A%2F%2Fjwxt.nwpu.edu.cn%2Fstudent%2Fsso-login'

class EduOaRequest:
    @staticmethod
    def get_redirect_url() -> str:
        return EduOaUrl.REDIRECT.split('?', 1)[1].removeprefix('service=')

    @staticmethod
    async def authorize(sess: ClientSession) -> List[URL]:
        resp = await sess.get(EduOaUrl.REDIRECT, headers=DEFAULT_HEADER, allow_redirects=True)
        return [x.url for x in resp.history]