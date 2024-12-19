from aiohttp import ClientSession

from nwpu.edu.edu_oa import EduOaRequest
from nwpu.edu.edu_struct import EduNotificationResponse
from nwpu.utils.common import DEFAULT_HEADER

class EduUrls:
    NOTIFICATION = "https://jwxt.nwpu.edu.cn/student/my-notification/get-notifications"


class EduRequest:
    headers: dict = DEFAULT_HEADER.copy()
    def __init__(self, sess: ClientSession, force_auth: bool = False):
        self.sess = sess

        if force_auth:
            EduOaRequest.authorize(sess)

    async def get_notification(self) -> EduNotificationResponse:
        resp = await self.sess.get(EduUrls.NOTIFICATION, headers=self.headers)
        return EduNotificationResponse(**await resp.json())
