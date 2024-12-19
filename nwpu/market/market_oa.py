from aiohttp import ClientSession

from nwpu.utils.common import DEFAULT_HEADER


class MarketOaUrl:
    OA_URL = "https://uis.nwpu.edu.cn/cas/login?service=https%3A%2F%2Fsecondhand-market.nwpu.edu.cn%2Flogin%2Fcas%3Fredirect_uri%3Dhttps%3A%2F%2Fsecondhand-market.nwpu.edu.cn%2Fui%2F"

class MarketOaRequest:
    @staticmethod
    def get_redirect_url() -> str:
        return MarketOaUrl.OA_URL.split('?', 1)[1].removeprefix('service=')

    @staticmethod
    async def authorize(sess: ClientSession) -> str:
        resp = await sess.get(MarketOaUrl.OA_URL, allow_redirects=True, headers=DEFAULT_HEADER)
        redirects = [x.url for x in resp.history]
        redirects.append(resp.url)
        print(redirects)
        if 'secondhand-market.nwpu.edu.cn' in redirects[-1].host:
            return redirects[-1].query['token']