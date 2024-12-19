import random

from aiohttp import ClientSession

from nwpu.ecampus.ec_oa import ECampusOaRequest
from nwpu.ecampus.ec_struct import *
from nwpu.utils.common import DEFAULT_HEADER


class ECampusUrl:
    HAS_NEW_EMAIL = "https://portal-service.nwpu.edu.cn/portalCenter/v2/personalData/getEmailDataNew"
    USER_INFO = "https://authx-service.nwpu.edu.cn/personal/api/v1/personal/me/user"
    USER_INFO_ACCURATE = "https://authx-service.nwpu.edu.cn/personal/api/v1/personal/user/info"
    USER_PORTRAIT = "https://authx-service.nwpu.edu.cn/personal/api/v1/me/portrait"
    USER_PAPER = "https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getPaper"
    USER_CARD = "https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getMyECard"
    USER_CONSUMPTION_HISTORY = "https://portal-service.nwpu.edu.cn/portalCenter/api/rest/center/personalData/getMyCost"
    USER_NETWORK_FEE = "https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getNetworkFeeInfo"
    USER_BORROW_BOOKS = "https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getMyBooks"
    USER_PROPERTY = "https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getPropertyInfo"
    USER_EVENTS = "https://ecampus.nwpu.edu.cn/portal-api/v1/calendar/share/schedule/getEvents"
    NEWS_FEED_COLUMN_LIST = "https://ecampus.nwpu.edu.cn/portal-api/v1/cms/Column/getColumnList"
    NEWS_FEED_CONTENT = "https://ecampus.nwpu.edu.cn/portal-api/v3/cms/content/getColumncontents"
    USER_EVENT_CALENDAR = "https://ecampus.nwpu.edu.cn/portal-api/v1/calendar/share/schedule/getPersonlCalendar"
    USER_EVENT_CREATE = "https://ecampus.nwpu.edu.cn/portal-api/v1/calendar/share/schedule/save"
    USER_EVENT_DELETE = "https://ecampus.nwpu.edu.cn/portal-api/v1/calendar/share/schedule/deleteSchedule"

class ECampusRequest:
    sess: ClientSession
    headers: dict = DEFAULT_HEADER.copy()

    def __init__(self, sess: ClientSession, x_token: str):
        self.sess: ClientSession = sess

        if x_token:
            self.sess.headers['X-Id-Token'] = x_token
        else:
            raise ValueError("X-Id-Token is required.")

    async def get_token(self) -> str:
        """
        Get ecampus token.
        Call this method if the x-token is not provided at initialization.
        :param sess:
        :return:
        """
        token = await ECampusOaRequest.authorize(self.sess)
        self.sess.headers['X-Id-Token'] = token
        return token
    
    async def get_new_email(self) -> ECampusHasNewEmailResponse:
        """
        Get new email status.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.HAS_NEW_EMAIL, headers=self.headers)
        return ECampusHasNewEmailResponse(**await resp.json())
    
    async def get_user_info(self) -> ECampusUserInfoResponse:
        """
        Get user info.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_INFO, headers=self.headers)
        return ECampusUserInfoResponse(**await resp.json())

    async def get_user_info_accurate(self) -> ECampusUserInfoAccurateResponse:
        """
        Get user info accurate.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_INFO_ACCURATE, headers=self.headers)
        return ECampusUserInfoAccurateResponse(**await resp.json())
    
    async def get_user_portrait(self) -> bytes:
        """
        Get user portrait.
        :return:
        """
        req = ECampusUserPortraitRequest(x_token=self.sess.headers['X-Id-Token'],
            random_number=random.randint(100, 999))
        resp = await self.sess.get(ECampusUrl.USER_PORTRAIT, 
                                   headers=self.headers, 
                                   params=req.model_dump(by_alias=True))
        
        return await resp.read()
    
    async def get_user_papers(self) -> ECampusUserPapersResponse:
        """
        Get user papers.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_PAPER, headers=self.headers)
        return ECampusUserPapersResponse(**await resp.json())
    
    async def get_user_card(self) -> ECampusUserCardResponse:
        """
        Get user card.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_CARD, headers=self.headers)
        return ECampusUserCardResponse(**await resp.json())

    async def get_user_consumption_history(self, req: ECampusUserConsumptionHistoryRequest) -> ECampusUserConsumptionHistoryResponse:
        """
        Get user consumption history.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_CONSUMPTION_HISTORY,
                                   headers=self.headers,
                                   params=req.model_dump(by_alias=True))
        return ECampusUserConsumptionHistoryResponse(**await resp.json())
    
    async def get_user_network_fee(self) -> ECampusUserNetworkFeeResponse:
        """
        Get user network fee.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_NETWORK_FEE, headers=self.headers)
        return ECampusUserNetworkFeeResponse(**await resp.json())
    
    async def get_user_borrow_books(self) -> ECampusUserBorrowBooksResponse:
        """
        Get user borrow books.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_BORROW_BOOKS, headers=self.headers)
        return ECampusUserBorrowBooksResponse(**await resp.json())
    
    async def get_user_property(self) -> ECampusUserPropertyResponse:
        """
        Get user property.
        needs further testing
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_PROPERTY, headers=self.headers)
        return ECampusUserPropertyResponse(**await resp.json())
    
    async def get_user_events(self, request: ECampusUserEventsRequest) -> ECampusUserEventsResponse:
        """
        Get user events.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_EVENTS,
                                   headers=self.headers,
                                   params=request.model_dump(by_alias=True)) # temporary hack
        return ECampusUserEventsResponse(**await resp.json())

    async def get_user_event_calendars(self) -> ECampusUserEventCalendarResponse:
        """
        Get user events.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_EVENT_CALENDAR,
                                   headers=self.headers,)
        return ECampusUserEventCalendarResponse(**await resp.json())

    async def add_user_event(self, request: ECampusAddUserEventRequest) -> ECampusAddUserEventResponse:
        """
        Add user event.
        :return:
        """
        resp = await self.sess.post(ECampusUrl.USER_EVENT_CREATE,
                                   headers=self.headers,
                                   json=request.model_dump(by_alias=True))
        return ECampusAddUserEventResponse(**await resp.json())

    async def delete_user_event(self, request: ECampusDeleteUserEventRequest) -> ECampusDeleteUserEventResponse:
        """
        Delete user event.
        :return:
        """
        resp = await self.sess.post(ECampusUrl.USER_EVENT_DELETE,
                                   headers=self.headers,
                                   data=request.model_dump(by_alias=True))
        return ECampusDeleteUserEventResponse(**await resp.json())

    async def get_news_feed_columns(self) -> ECampusNewsFeedColumnListResponse:
        """
        Get user news feed columns.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.NEWS_FEED_COLUMN_LIST,
                                   headers=self.headers,)
        return ECampusNewsFeedColumnListResponse(**await resp.json())

    async def get_news_feed_content(self, request: ECampusNewsFeedContentRequest) -> ECampusNewsFeedContentResponse:
        """
        Get user news feed content.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.NEWS_FEED_CONTENT,
                                   headers=self.headers,
                                   params=request.model_dump(by_alias=True))
        return ECampusNewsFeedContentResponse(**await resp.json())
