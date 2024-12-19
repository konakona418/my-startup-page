import base64
import json
import urllib.parse

from aiohttp import ClientSession

from nwpu.utils.common import DEFAULT_HEADER


class ECampusOaUrl:
    REDIRECT = 'https://uis.nwpu.edu.cn/cas/login?service=https%3A%2F%2Fecampus.nwpu.edu.cn%2F%3Fpath%3Dhttps%253A%252F%252Fecampus.nwpu.edu.cn%252Fmain.html%2523%252F'


class ECampusOaRequest:
    @staticmethod
    def get_redirect_url() -> str:
        return ECampusOaUrl.REDIRECT.split('?', 1)[1].removeprefix('service=')

    @staticmethod
    def parse_token_from_ticket(ticket: str) -> str:
        """
        see: https://ecampus.nwpu.edu.cn//js/8451.e5865a44.js
         -1 !== window.location.href.indexOf("ticket=") && (t = location.href,
                            a = t.indexOf("ticket="),
                            -1 === t.indexOf("path=") ? m = window.location.origin : (i = t.indexOf("path=") + 5,
                            o = -1 === t.indexOf("&redirect=true") ? a - 1 : t.indexOf("&redirect=true"),
                            p = t.substring(i, o),
                            m = decodeURIComponent(p),
                            -1 !== m.indexOf("/AccessDenied") && (m = window.location.origin)),
                            f = -1 !== t.indexOf("#/") ? t.indexOf("#/") : t.length,
                            -1 !== a)) {
                                S = t.substring(a + 7, f);
                                try {
                                    A = JSON.parse(decodeURIComponent(escape(window.atob(decodeURIComponent(S).split(".")[1])))),
                                    b = A.identityTypeCode.trim().charAt(0).toUpperCase() + A.identityTypeCode.trim().slice(1),
                                    w = A.organizationName,
                                    v(S, A.idToken, b, w)
                                } catch (r) {
                                    console.log("err", r, r.message),
                                    (0,
                                    d.Message)({
                                        message: "登陆错误！",
                                        type: "error",
                                        duration: 2e3
                                    })
                                }
                            }
        :param ticket:
        :return:
        """
        b64 = ticket.split('.')[1]
        b64_decoded = base64.b64decode(b64).decode(encoding='utf-8')
        json_data = json.loads(b64_decoded)
        return json_data['idToken']

    @staticmethod
    async def authorize(sess: ClientSession) -> str:
        resp = await sess.get(ECampusOaUrl.REDIRECT, headers=DEFAULT_HEADER, allow_redirects=False)
        redirected: str = resp.headers['Location']
        if 'https://ecampus.nwpu.edu.cn' in redirected:
            parsed = urllib.parse.parse_qs(redirected)
            return ECampusOaRequest.parse_token_from_ticket(parsed['ticket'][0])