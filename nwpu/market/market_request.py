from aiohttp import ClientSession

from nwpu.market.market_oa import MarketOaRequest
from nwpu.market.market_struct import *
from nwpu.utils.parse import concat_url
from nwpu.utils.common import DEFAULT_HEADER


class MarketUrls:
    MARKET_SELF_INFO = "https://secondhand-market.nwpu.edu.cn/api/user/noAvatar"
    MARKET_ITEM_CLASSIFICATION = "https://secondhand-market.nwpu.edu.cn/api/dict/tree/item-classificationy"
    MARKET_COMPLAINT_TYPE = "https://secondhand-market.nwpu.edu.cn/api/dict/tree/complain-status"
    MARKET_CAMPUS_INFO = "https://secondhand-market.nwpu.edu.cn/api/dict/children/campus"
    MARKET_UNREAD_MSG_COUNT = "https://secondhand-market.nwpu.edu.cn/api/message/unReadCount"
    MARKET_MSG_LIST = "https://secondhand-market.nwpu.edu.cn/api/message/myMessage"
    MARKET_ITEM_LIST = "https://secondhand-market.nwpu.edu.cn/api/second/page"
    MARKET_ITEM_DETAIL = "https://secondhand-market.nwpu.edu.cn/api/second/detail"

class MarketRequest:
    sess: ClientSession
    headers: dict = DEFAULT_HEADER.copy()
    def __init__(self, session: ClientSession, x_token: str):
        self.sess = session

        if x_token:
            self.headers['X-Id-Token'] = x_token
        else:
            raise ValueError("X-Id-Token is required.")

    async def get_token(self) -> str:
        token = await MarketOaRequest.authorize(self.sess)
        self.headers['X-Id-Token'] = token
        return token

    async def get_self_info(self) -> MarketSelfInfoResponse:
        resp = await self.sess.get(
            MarketUrls.MARKET_SELF_INFO,
            headers=self.headers)

        return MarketSelfInfoResponse(**await resp.json())

    async def get_item_classification(self) -> MarketItemClassificationResponse:
        resp = await self.sess.get(
            MarketUrls.MARKET_ITEM_CLASSIFICATION,
            headers=self.headers)

        return MarketItemClassificationResponse(**await resp.json())

    async def get_complaint_type(self) -> MarketComplaintTypeResponse:
        resp = await self.sess.get(
            MarketUrls.MARKET_COMPLAINT_TYPE,
            headers=self.headers)

        return MarketComplaintTypeResponse(**await resp.json())

    async def get_campus_info(self) -> MarketCampusInfoResponse:
        resp = await self.sess.get(
            MarketUrls.MARKET_CAMPUS_INFO,
            headers=self.headers)

        return MarketCampusInfoResponse(**await resp.json())

    async def get_unread_message_count(self) -> MarketUnreadMessageCountResponse:
        resp = await self.sess.get(
            MarketUrls.MARKET_UNREAD_MSG_COUNT,
            headers=self.headers)

        return MarketUnreadMessageCountResponse(**await resp.json())

    async def get_message_list(self, request: MarketUserMessageRequest = MarketUserMessageRequest()) -> MarketUserMessageResponse:
        resp = await self.sess.get(
            MarketUrls.MARKET_MSG_LIST,
            headers=self.headers,
            json=request.model_dump())

        return MarketUserMessageResponse(**await resp.json())

    async def get_item_list(self, request: MarketItemListRequest = MarketItemListRequest()) -> MarketItemListResponse:
        resp = await self.sess.get(
            MarketUrls.MARKET_ITEM_LIST,
            headers=self.headers,
            params=request.model_dump(by_alias=True, exclude_none=True))

        return MarketItemListResponse(**await resp.json())

    async def get_item_detail(self, item_id: str | int) -> MarketItemDetailResponse:
        resp = await self.sess.get(
            concat_url(MarketUrls.MARKET_ITEM_DETAIL, str(item_id)),
            headers=self.headers)

        return MarketItemDetailResponse(**await resp.json())
